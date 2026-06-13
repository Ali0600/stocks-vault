---
type: concept
updated: 2026-06-13
---
# Custom AI silicon (ASIC / XPU)

Most AI training runs on NVIDIA's merchant GPUs, but the big hyperscalers also design their own accelerators — Google's TPU, Amazon's Trainium, Microsoft's Maia, Meta's MTIA — to cut cost and reduce NVIDIA dependence. They don't build them alone: [[MRVL]] and Broadcom together do roughly 95% of the custom-ASIC co-design work that turns a hyperscaler's spec into manufacturable silicon (Broadcom alone is cited near 70% of the custom-accelerator market).

In 2026 NVIDIA still holds ~70–75% of datacenter AI-accelerator revenue, AMD ~6–8%, and custom silicon ~15–20% — but custom is growing far faster (ASIC shipments ~45% vs ~16% for GPUs). The divide is by workload: custom chips win in **inference** (predictable, high-volume, now ~two-thirds of AI compute spend), while NVIDIA keeps **training**, where [[CUDA]] flexibility and [[GPU interconnect|NVLink]] scaling are hardest to replicate. It's the main long-term check on [[NVDA]].

## In this vault
- Co-designers: [[MRVL]] · Broadcom (external) · Merchant GPU: [[NVDA]], AMD (external)
- Buyers: hyperscaler in-house chips — TPU, Trainium, Maia, MTIA (external)
- Map: [[AI Supply Chain]] → Chip design · Related: [[CUDA]], [[GPU interconnect]]

## Sources
- [Tom's Hardware — custom AI ASIC state of play](https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia)
- [TechTimes — ASIC shipments outpace GPU growth](https://www.techtimes.com/articles/317225/20260526/custom-ai-chips-outpace-nvidia-gpu-growth-2026-asic-shipments-set-triple-gpu-rate.htm)
- [Introl — the custom-silicon inflection](https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu)
