
# FEATURE_ENGINEERING.md — ML Feature Engineering

## 1. Purpose
Feature engineering transforms raw sensor metrics into stable inputs for ML models (GBR, LSTM, CoxPH) used in dc-ai-dul.

## 2. Engineered Features Table

| Category | Raw Metrics | Engineered Features | Purpose |
|---------|-------------|---------------------|---------|
| PSU | temp_c, power_w | temp slope, efficiency drift, thermal cycles | Predict capacitor aging |
| SSD | wear_pct, TBW | wear-rate acceleration, ECC slope | NAND degradation modeling |
| GPU | temp, power, util | EM stress index, power-temp ratio | Predict electromigration |
| Fan | RPM, duty | instability index, bearing wear score | Cooling degradation |
| Node | cpu/vmr temp, ecc | thermal headroom, ecc acceleration | CPU/VRM silicon aging |
| Rack | temp, humidity | thermal delta, humidity stress | Rack-level stress |

## 3. Notes
Engineered features improve prediction stability and reduce noise.

## 4. Conclusion
These features are used in all dc-ai-dul model pipelines.
