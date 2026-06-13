---
type: concept
updated: 2026-06-13
---
# Datacenter power

An AI datacenter's hard limit increasingly isn't chips — it's electricity. A single NVIDIA GB200 NVL72 rack draws ~120–140 kW, roughly 16× a normal server rack five years ago, and the next generation (Vera Rubin NVL144) pushes toward ~600 kW; racks are expected to reach ~1 MW by 2028. A 1-gigawatt campus runs on the order of ~470,000 GPUs.

The catch is the grid. Interconnection queues for large loads now exceed 1,500 GW nationally with 4–7-year waits, and substations often cap delivery at 250–500 MW regardless of available generation. That's why power and grid-connected land have become a binding constraint — and why operators chase behind-the-meter generation (gas, nuclear, geothermal). It's the moat [[IREN]] leans on (it owns powered sites) and the whole bet behind [[OKLO]] (sell the power itself).

## In this vault
- Owns power + land: [[IREN]] · Sells power (nuclear): [[OKLO]]
- Map: [[AI Supply Chain]] → Power & land (the rising chokepoint) · Related: [[Liquid cooling]]

## Sources
- [Sunbird DCIM — GB200 NVL72 power readiness](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72)
- [techplustrends — 1 GW datacenter power](https://techplustrends.com/1gw-data-center-power-consumption-guide/)
- [backuppower.ai — AI datacenter power requirements 2026](https://backuppower.ai/data-centers/ai-data-center-power-requirements/)
