---
type: concept
updated: 2026-06-14
---
# EDA & chip IP

Before a chip can be fabbed at [[Foundry process nodes|TSMC]], it must be *designed* — and
that design is gated by two upstream oligopolies most supply-chain maps skip. **EDA**
(electronic design automation) is the software used to design, simulate, verify and lay out
every modern chip; **Synopsys** and **Cadence** form a ~2-firm duopoly (Siemens EDA a distant
third), so essentially no AI chip — NVIDIA GPUs, Broadcom/Marvell ASICs, hyperscaler TPUs —
reaches tape-out without their tools. **Chip IP** is pre-designed, licensable building blocks:
**Arm** licenses the CPU cores in most SoCs (NVIDIA's Grace, hyperscaler server CPUs, nearly
all mobile), while Synopsys and Cadence also license interface IP (PCIe, HBM, USB, SerDes).

Why it's a chokepoint: switching EDA vendors mid-design is impractical, and re-architecting
off Arm is a multi-year cost — so the layer compounds pricing power and sits upstream of
*everyone* who designs silicon. The main escape valve is **RISC-V**, an open CPU instruction
set that lets designers avoid Arm royalties (and which Arm increasingly competes with); EDA
has no comparable open alternative, which is why the tool duopoly is the harder gate.

## In this vault
- [[SNPS]] · [[CDNS]] — the EDA software duopoly
- [[ARM]] — dominant CPU IP licensor
- Gates every chip designer: [[NVDA]], [[AVGO]], [[MRVL]], [[AMD]], [[INTC]] (all fabbed at [[TSM]])
- Related: [[Foundry process nodes]] · [[Custom AI silicon]] · [[Wafer-fab equipment]]

## Sources
- Synopsys, Cadence, and Arm investor materials and 10-K / 20-F segment disclosures
- Industry coverage of EDA market structure (Synopsys / Cadence / Siemens EDA shares) and the RISC-V vs Arm dynamic
