# FraudGuard AI

FraudGuard AI is a final-year project focused on applying Artificial Intelligence to banking fraud detection. The project aims to design a platform capable of assigning a risk score to each financial transaction using the XGBoost machine learning algorithm, generating alerts when the risk exceeds a predefined threshold, and assisting analysts during investigations through a dedicated OpenClaw agent configured for banking environments.

The value of the project lies in the combination of two complementary approaches. XGBoost processes structured transaction data and produces robust, measurable, and explainable probabilistic predictions. OpenClaw orchestrates a conversational AI agent capable of invoking controlled internal tools, retrieving relevant information, presenting the key factors that influenced the risk score, comparing the case with similar historical incidents, and generating a draft investigation report.

The AI agent is designed to support analysts rather than replace them. It does not make irreversible decisions and always keeps the human analyst in control of the final assessment and action process.
