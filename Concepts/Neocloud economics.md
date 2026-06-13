---
type: concept
updated: 2026-06-13
---
# Neocloud economics

A "neocloud" is a specialist GPU-cloud provider — [[CRWV]], [[NBIS]], [[IREN]], plus private names like Lambda and Crusoe — that buys NVIDIA GPUs in bulk and rents them by the hour, usually faster to the newest hardware and cheaper for raw compute than the hyperscalers. They're capacity, not a chokepoint: the scarcity (GPUs, [[Datacenter power|power]]) sits upstream, and their edge is speed-to-deploy and cheap power rather than exclusivity.

The model's defining feature is how it's financed. GPUs are bought with debt — often collateralized by the GPUs themselves and by signed customer contracts — so balance sheets run heavy. CoreWeave operates at roughly 4.5× debt-to-equity (it pioneered GPU-backed loans, including the first investment-grade HPC-secured facility), while Nebius's structure is cleaner. The risk is circular: GPU values and rental rates have to hold up long enough to service the debt — the heart of the "GPU debt wall" debate.

## In this vault
- Neoclouds: [[CRWV]] (debt-heavy), [[NBIS]] (cleaner), [[IREN]] (owns power) · context: [[2026-06-11 situational-awareness-neocloud-stakes]]
- Map: [[AI Supply Chain]] → Neocloud capacity · Related: [[Datacenter power]]

## Sources
- [io-fund — the circular financing of the GPU boom](https://io-fund.com/ai-stocks/nvidia-coreweave-nebius-circular-financing-gpu-boom)
- [Bloomberg — CoreWeave's $8.5B GPU-backed loan](https://www.bloomberg.com/news/articles/2026-03-31/coreweave-crwv-raises-8-5-billion-gpu-loan-backed-by-meta-deal)
- [The GPU debt wall — CoreWeave deep dive](https://business.wapakdailynews.com/wapakdailynews/article/finterra-2026-2-23-the-gpu-debt-wall-a-deep-dive-into-coreweave-crwv-and-the-2026-ai-financing-crisis)
