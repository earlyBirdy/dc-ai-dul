
# DUL_MODEL_THEORY.md — GBR, CoxPH, LSTM Modeling Theory

## 1. Overview
This document explains the mathematical and engineering basis behind the three core ML models used in dc-ai-dul.

---

## 2. Gradient Boosting Regressor (GBR)
Used for: **Per‑component DUL prediction**

GBR advantages:
- Handles nonlinear relationships (temp + power + wear)
- Strong performance with tabular sensor data
- Resistant to noise

Formula:
DUL = Σ wᵢ · fᵢ(x)

Most important features:
- PSU temperature slope
- SSD wear-rate acceleration
- GPU EM stress index

---

## 3. Cox Proportional Hazards (CoxPH)
Used for: **Fleet‑level hazard curves**

Hazard function:
h(t | x) = h₀(t) · exp(βᵀx)

Interpretation:
- β shows which features increase failure risk
- Allows predicting time-to-failure distributions

Outputs:
- Relative risk score
- Survival probability curve
- Mean Time To Failure (MTTF)

---

## 4. LSTM (Long Short-Term Memory Networks)
Used for: **Temporal degradation forecasting**

Why LSTM?
- Degradation is time‑dependent
- Captures long‑term memory (thermal cycles, wear trends)
- Great for GPUs, SSDs, fans, and power supply traces

Typical inputs:
- Temp sequence  
- Power sequence  
- Utilization sequence  

Outputs:
- Next-step degradation estimate  
- Full-sequence DUL forecast  

