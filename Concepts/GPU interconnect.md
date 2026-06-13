---
type: concept
updated: 2026-06-13
---
# GPU interconnect (scale-up vs scale-out)

Training a model splits it across thousands of GPUs that must constantly swap data, so how they're wired together is its own bottleneck — and it splits into two regimes. **Scale-up** links the GPUs inside a rack so they act like one giant chip: NVIDIA's proprietary NVLink does this at ~1.8 TB/s per GPU (NVLink 5), fast enough that any GPU in a 72-GPU GB200 rack reaches any other without touching the network. **Scale-out** connects rack to rack across the building, where the signal goes optical — Ethernet (NVIDIA's Spectrum-X) or InfiniBand — which is the layer [[Optical interconnect]] serves.

The split is competitive, not just technical: scale-up (NVLink) is a closed NVIDIA moat that ships with the GPU, while scale-out is a more open fight (the Ethernet ecosystem, [[MRVL]] and Broadcom silicon, the optical names). Each NVIDIA generation widens the scale-up domain — GB200 binds 72 GPUs, Vera Rubin's NVL144 binds 144 — pulling more of the interconnect inside NVIDIA's proprietary fabric.

## In this vault
- Scale-up: [[NVDA]] (NVLink/NVSwitch, proprietary)
- Scale-out: [[Optical interconnect]] makers + [[MRVL]] DSP/SerDes; Ethernet vs InfiniBand
- Map: [[AI Supply Chain]] → between Chip design and Optical · Related: [[CUDA]], [[Custom AI silicon]]

## Sources
- [Introl — NVLink & scale-up networking](https://introl.com/blog/nvlink-scale-up-networking-gpu-interconnect-infrastructure-2025)
- [Converge Digest — NVLink 6 in Rubin rack-scale](https://convergedigest.com/nvlink-6-becomes-the-backbone-of-rubin-rack-scale-ai-architecture/)
- [Network World — NVIDIA networking roadmap](https://www.networkworld.com/article/4050881/nvidia-networking-roadmap-ethernet-infiniband-co-packaged-optics-will-shape-data-center-of-the-future.html)
