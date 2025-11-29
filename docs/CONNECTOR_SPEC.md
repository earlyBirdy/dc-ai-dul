
# CONNECTOR_SPEC.md — Telemetry Connector Specification

## 1. Overview
Connectors standardize ingestion of telemetry from Prometheus, SNMP, Redfish, IPMI, smartctl, and nvidia-smi.

## 2. Required Connectors

### PSU Connector
Sources: SNMP, IPMI, Redfish  
Metrics: temp_c, power_w, voltage_v, current_a, efficiency_pct

### SSD Connector
Source: smartctl  
Metrics: wear_pct, tbw, ssd_temp_c, ecc_count

### GPU Connector
Source: nvidia-smi  
Metrics: gpu_temp_c, gpu_util_pct, gpu_power_w, gpu_memory_mb

### Fan Connector
Source: Redfish/IPMI  
Metrics: fan_speed_rpm, fan_duty_pct, fan_health_pct

### Node Connector
Source: IPMI / OS telemetry  
Metrics: cpu_temp_c, vrm_temp_c, ecc_errors

### Rack Environment Connector
Source: Modbus/BMS  
Metrics: inlet_temp, humidity_pct, airflow_cfm

## 3. Output Schema
All connectors output TelemetryInput objects:
{
  "component_type": "...",
  "metrics": { ... },
  "timestamp": "..."
}

## 4. Conclusion
These connectors ensure uniform ingestion for ML pipelines.
