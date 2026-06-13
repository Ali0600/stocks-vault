---
type: concept
updated: 2026-06-13
---
# CoWoS (advanced packaging)

CoWoS (Chip-on-Wafer-on-Substrate) is TSMC's advanced packaging step: it sets the GPU logic die and the [[HBM]] memory stacks side-by-side on a silicon interposer — a tiny high-density circuit board that wires them together with far more connections than a normal package allows. A modern AI accelerator physically can't exist without it; the compute die and its memory have to be co-packaged this tightly to hit their bandwidth.

It is the single tightest link in the AI stack. TSMC has called CoWoS sold out through 2026, NVIDIA alone has reportedly booked over half of 2026 capacity, and TSMC is racing to double output and push interposers toward ~9.5× reticle size by 2027. The newer CoWoS-L variant adds manufacturing headaches like warpage on huge packages. Intel's EMIB/Foveros are the main alternative, but TSMC dominates — a big reason [[TSM]] rates Extreme.

## In this vault
- Done by: [[TSM]] (near-sole supplier) · Intel EMIB/Foveros (external alternative)
- Packages together: [[NVDA]] GPU dies + [[HBM]] stacks
- Map: [[AI Supply Chain]] → Foundry / packaging · Related: [[HBM]], [[Foundry process nodes]]

## Sources
- [Tom's Hardware — CoWoS capacity stretched](https://www.tomshardware.com/tech-industry/semiconductors/intel-gains-ground-in-ai-packaging-as-cowos-capacity-remains-stretched)
- [FinancialContent — the great packaging pivot](https://markets.financialcontent.com/wral/article/tokenring-2026-1-1-the-great-packaging-pivot-how-tsmc-is-doubling-cowos-capacity-to-break-the-ai-supply-bottleneck-through-2026)
- [Fusion — CoWoS, HBM, 2–3nm constraints through 2027](https://info.fusionww.com/blog/inside-the-ai-bottleneck-cowos-hbm-and-2-3nm-capacity-constraints-through-2027)
