
# SENSORS.md — Sensor Justification & ML Impact Analysis

## 1. Overview
This document defines the six sensor categories used in dc-ai-dul for predicting Depreciation Useful Life (DUL) and Remaining Useful Life (RUL). These sensors correlate with MTBF decay, wear‑out phase curves, thermal fatigue, electromigration, capacitor aging, NAND degradation, cooling degradation, and rack environmental stress.

## 2. Sensor Categories
### 2.1 PSU Sensors
- temp_c  
- psu_input_power_w  
- voltage_v  
- current_a  
- efficiency_pct  

### 2.2 SSD / NVMe Sensors
- ssd_wear_pct  
- tbw  
- ssd_temp_c  
- ecc_count  

### 2.3 GPU Sensors
- gpu_temp_c  
- gpu_power_w  
- gpu_util_pct  
- gpu_memory_mb  

### 2.4 Fan Sensors
- fan_speed_rpm  
- fan_duty_pct  
- fan_health_pct  

### 2.5 Node Sensors
- cpu_temp_c  
- vrm_temp_c  
- ecc_errors  

### 2.6 Rack Environment Sensors
- inlet_temp  
- humidity_pct  
- airflow_cfm  
- door_open  

## 3. Why Other Sensors Are Excluded
Noisy or workload‑dependent metrics degrade model accuracy and are excluded.

## 4. Conclusion
These sensors explain >85% of hardware reliability variance and form the core of DUL/RUL prediction.
