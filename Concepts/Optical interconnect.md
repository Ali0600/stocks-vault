---
type: concept
updated: 2026-06-13
---
# Optical interconnect (transceivers)

Inside an AI cluster, tens of thousands of GPUs have to talk to each other, and past roughly a meter copper can't carry the data fast enough — so the signal is turned into light and sent over fiber by pluggable optical transceivers. Each generation doubles the rate (400G → 800G → 1.6T), and a single large training cluster needs hundreds of thousands of modules, so optics demand scales with GPU count rather than with floor space.

2026 is the "800G everywhere, 1.6T arriving" year: 800G is the largest transceiver deployment in history (>60% of shipments) while 1.6T enters volume (millions of units), and the transceiver market is ~$26B, up ~60% year over year. The emerging next step is co-packaged optics (CPO), which moves the optics onto the switch silicon itself — entering volume in 2026 but coexisting with pluggables for years. This is the layer [[AAOI]], [[COHR]], [[LITE]], [[POET]] and [[NOK]] sell into, with [[MRVL]] supplying the DSP that drives the modules.

## In this vault
- Makers: [[AAOI]], [[COHR]], [[LITE]], [[POET]], [[NOK]] · DSP/silicon: [[MRVL]]
- Used by: [[NVDA]] clusters · Map: [[AI Supply Chain]] → Optical interconnect

## Sources
- [TSPA Semiconductor — 800G today, 1.6T tomorrow](https://tspasemiconductor.substack.com/p/ai-networking-arms-race-heats-up)
- [SemiAnalysis — co-packaged optics (CPO)](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling)
