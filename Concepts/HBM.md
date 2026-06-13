---
type: concept
updated: 2026-06-13
---
# HBM (high-bandwidth memory)

High-bandwidth memory is DRAM stacked into vertical cubes and placed micrometers from the GPU, wired to it by an extremely wide bus — so it feeds the processor far faster than ordinary memory. HBM3E moves ~1.2 TB/s per stack, and that bandwidth is what decides whether an AI accelerator runs at full speed; without enough HBM next to the compute die, the GPU starves.

Only three companies on Earth can make it — SK Hynix (~55–60% share), Micron (~20%), and Samsung — and it has been sold out through 2026 with no spot market. The barrier is brutal: multi-billion-dollar fabs and 18–36-month capacity cycles, so supply can't flex to demand. HBM3E runs ~$300/stack; HBM4 (validating through 2026) ~$500. It rides onto the GPU package via [[CoWoS]], which makes the two the tightest pair of gates in the whole chain.

## In this vault
- Makers: [[MU]] (the only US-based one) · SK Hynix, Samsung (external)
- Used by: [[NVDA]] accelerators; co-packaged via [[CoWoS]] at [[TSM]]
- Map: [[AI Supply Chain]] → Memory layer (rated High)

## Sources
- [Astute Group — HBM share & HBM4 pivot](https://www.astutegroup.com/news/general/sk-hynix-holds-62-of-hbm-micron-overtakes-samsung-2026-battle-pivots-to-hbm4/)
- [Barrack AI — the 2026 GPU memory crisis](https://blog.barrack.ai/2026-gpu-memory-crisis/)
- [TechPowerUp — HBM4 validation, three suppliers](https://www.techpowerup.com/346343/hbm4-validation-expected-in-2q26-three-major-suppliers-poised-to-shape-nvidia-supply-landscape)
