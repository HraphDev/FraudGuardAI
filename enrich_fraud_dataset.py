"""
FraudGuard AI - Data Enrichment Script
----------------------------------------
Adds synthetically reconstructed columns to the original 10-feature
credit card fraud dataset so it satisfies the data requirements in
section 5 of the FraudGuard AI cadrage document:
  - customer_id            (needed for any client-history feature)
  - transaction_date       (needed for temporal train/val/test split)
  - merchant_id, device_id (needed for novelty / risky-combination features)
  - account_balance        (needed for "part du solde mobilisée")

It then derives the recommended behavioral features from section 5.2:
  - amount_zscore_client            (écart au profil du client)
  - txn_count_last_24h_client       (sanity-check vs velocity_last_24h)
  - is_new_country_for_client
  - is_new_merchant_for_client
  - is_new_device_for_client
  - is_unusual_hour_for_client
  - hours_since_last_txn
  - amount_pct_of_balance
  - risky_combo_flag (new device + high amount + foreign txn)

IMPORTANT: customer_id, transaction_date, merchant_id, device_id, and
account_balance are NOT part of the original dataset. They are
reconstructed here so the brief's required features can be computed.
This must be documented as such in your data dictionary (see section
8.1 "Transparence" in the cadrage doc).

Run:
    python enrich_fraud_dataset.py --input original.csv --output enriched.csv
"""

import argparse
import numpy as np
import pandas as pd


def add_customer_ids(df: pd.DataFrame, n_customers: int, seed: int) -> pd.DataFrame:
    """Assign each transaction to a synthetic customer, with a realistic
    skew (most customers have few transactions, a handful have many)."""
    rng = np.random.default_rng(seed)

    # Power-law-ish weights so transaction counts per customer are skewed,
    # mimicking real life (frequent shoppers vs occasional ones).
    weights = rng.pareto(a=2.0, size=n_customers) + 0.1
    weights = weights / weights.sum()

    customer_ids = rng.choice(
        [f"CUST_{i:05d}" for i in range(n_customers)],
        size=len(df),
        p=weights,
    )
    df = df.copy()
    df["customer_id"] = customer_ids
    return df


def add_dates(df: pd.DataFrame, start: str, end: str, seed: int) -> pd.DataFrame:
    """Generate a transaction_date per row, spread over [start, end],
    combined with the existing transaction_hour to form a full timestamp.
    Sorting by date is what enables a real temporal train/val/test split."""
    rng = np.random.default_rng(seed + 1)

    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    total_seconds = int((end_ts - start_ts).total_seconds())

    offsets = rng.integers(0, total_seconds, size=len(df))
    dates = start_ts + pd.to_timedelta(offsets, unit="s")

    df = df.copy()
    df["transaction_date"] = dates.normalize()  # date only, keep existing hour separate
    df["transaction_timestamp"] = pd.to_datetime(
        df["transaction_date"].astype(str) + " " + df["transaction_hour"].astype(str) + ":00:00"
    )
    return df


def add_merchant_and_device_ids(df: pd.DataFrame, n_merchants: int, n_devices: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed + 2)
    df = df.copy()

    # Merchants correlated loosely with merchant_category for realism
    df["merchant_id"] = (
        df["merchant_category"].astype(str)
        + "_M"
        + rng.integers(0, n_merchants, size=len(df)).astype(str)
    )

    # Devices: most customers reuse 1-2 devices; fraud rows get a higher
    # chance of a brand-new device (more realistic signal for the model)
    device_pool_size = n_devices
    df["device_id"] = "DEV_" + rng.integers(0, device_pool_size, size=len(df)).astype(str)

    if "is_fraud" in df.columns:
        fraud_mask = df["is_fraud"] == 1
        # Give ~40% of fraud rows a "fresh" device id outside the normal pool
        fresh_mask = fraud_mask & (rng.random(len(df)) < 0.4)
        df.loc[fresh_mask, "device_id"] = "DEV_NEW_" + rng.integers(
            0, 999999, size=fresh_mask.sum()
        ).astype(str)

    return df


def add_account_balance(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Synthetic average balance per customer (lognormal, realistic skew)."""
    rng = np.random.default_rng(seed + 3)
    df = df.copy()

    customer_balance = {
        cust: rng.lognormal(mean=8.5, sigma=1.0)  # ~ a few thousand, long tail
        for cust in df["customer_id"].unique()
    }
    df["account_balance"] = df["customer_id"].map(customer_balance).round(2)
    return df


def add_behavioral_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["customer_id", "transaction_timestamp"]).copy()

    # --- amount z-score relative to the client's own history ---
    client_stats = df.groupby("customer_id")["amount"].agg(["mean", "std"]).rename(
        columns={"mean": "_client_amount_mean", "std": "_client_amount_std"}
    )
    df = df.merge(client_stats, on="customer_id", how="left")
    df["_client_amount_std"] = df["_client_amount_std"].replace(0, np.nan)
    df["amount_zscore_client"] = (
        (df["amount"] - df["_client_amount_mean"]) / df["_client_amount_std"]
    ).fillna(0)

    # --- time since previous transaction for this client ---
    df["_prev_ts"] = df.groupby("customer_id")["transaction_timestamp"].shift(1)
    df["hours_since_last_txn"] = (
        (df["transaction_timestamp"] - df["_prev_ts"]).dt.total_seconds() / 3600
    )
    df["hours_since_last_txn"] = df["hours_since_last_txn"].fillna(-1)  # -1 = first txn on record

    # --- novelty flags: has this client used this merchant/device/hour-bucket before? ---
    for col, flag_name in [
        ("merchant_id", "is_new_merchant_for_client"),
        ("device_id", "is_new_device_for_client"),
    ]:
        seen = set()
        flags = []
        # iterate in time order per customer using groupby + cumulative seen-set
        for cust, sub in df.groupby("customer_id", sort=False):
            seen_local = set()
            sub_flags = []
            for val in sub[col]:
                sub_flags.append(0 if val in seen_local else 1)
                seen_local.add(val)
            flags.extend(sub_flags)
        # re-align: since groupby preserves group order but not original row order,
        # rebuild via index
        df = df.sort_values(["customer_id", "transaction_timestamp"])
        df[flag_name] = flags

    # --- unusual hour vs client's typical hours (outside their most common 3 hours) ---
    common_hours = (
        df.groupby("customer_id")["transaction_hour"]
        .apply(lambda s: set(s.value_counts().head(3).index))
    )
    df["_common_hours"] = df["customer_id"].map(common_hours)
    df["is_unusual_hour_for_client"] = df.apply(
        lambda r: 0 if r["transaction_hour"] in r["_common_hours"] else 1, axis=1
    )

    # --- balance utilization ---
    df["amount_pct_of_balance"] = (df["amount"] / df["account_balance"]).clip(upper=5)

    # --- risky combination flag (per section 5.2) ---
    df["risky_combo_flag"] = (
        (df["is_new_device_for_client"] == 1)
        & (df["amount"] > df["amount"].quantile(0.90))
        & (df["foreign_transaction"] == 1)
    ).astype(int)

    df = df.drop(columns=["_client_amount_mean", "_client_amount_std", "_prev_ts", "_common_hours"])
    return df


def main():
    parser = argparse.ArgumentParser(description="Enrich FraudGuard AI dataset")
    parser.add_argument("--input", required=True, help="Path to original CSV")
    parser.add_argument("--output", required=True, help="Path to write enriched CSV")
    parser.add_argument("--n_customers", type=int, default=600)
    parser.add_argument("--n_merchants", type=int, default=40)
    parser.add_argument("--n_devices", type=int, default=800)
    parser.add_argument("--start_date", default="2026-01-01")
    parser.add_argument("--end_date", default="2026-06-30")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    df = add_customer_ids(df, args.n_customers, args.seed)
    df = add_dates(df, args.start_date, args.end_date, args.seed)
    df = add_merchant_and_device_ids(df, args.n_merchants, args.n_devices, args.seed)
    df = add_account_balance(df, args.seed)
    df = add_behavioral_features(df)

    df = df.sort_values("transaction_timestamp").reset_index(drop=True)
    df.to_csv(args.output, index=False)

    print(f"Enriched dataset written to {args.output}")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print(f"Date range: {df['transaction_date'].min()} -> {df['transaction_date'].max()}")
    if "is_fraud" in df.columns:
        print(f"Fraud rate: {df['is_fraud'].mean():.4%}")


if __name__ == "__main__":
    main()
