---
type: concept
updated: 2026-06-13
---
# Liquid cooling

Once a rack draws ~120 kW (a GB200 NVL72), air can't carry the heat away fast enough — so coolant is piped directly to cold plates on the chips (direct-to-chip, DLC), or in some designs the hardware is submerged entirely (immersion). Liquid moves heat far more efficiently than air, and at Blackwell-class densities it stopped being optional: the GB200 NVL72 ships liquid-cooled by default.

That reshapes datacenter design — plumbing, manifolds, coolant-distribution units — and rewards vendors who can deliver cooling at rack scale. It's the edge [[SMCI]] leans on (rack-scale DLC and speed to ship liquid-cooled systems around the newest GPUs), and a transition established server vendors like [[HPE]] are racing to match. It's tightly coupled to [[Datacenter power]]: denser racks need both more power in and more heat out.

## In this vault
- Rack-scale DLC edge: [[SMCI]] · established vendors: [[HPE]]
- Map: [[AI Supply Chain]] → Servers · Related: [[Datacenter power]]

## Sources
- [Introl — GB200 NVL72 liquid-cooled deployment](https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled)
- [Sunbird DCIM — GB200 NVL72 readiness](https://www.sunbirddcim.com/blog/your-data-center-ready-nvidia-gb200-nvl72)
