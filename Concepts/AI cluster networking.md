---
type: concept
updated: 2026-06-14
---
# AI cluster networking

Training a frontier model means wiring tens of thousands of GPUs into one machine, and the
network is as much a bottleneck as the chips. Two domains: **scale-up** — the tight, ultra-
high-bandwidth fabric *inside* a rack/pod ([[GPU interconnect|NVLink]], and the open **UALink**
consortium as the would-be alternative) — and **scale-out** — the data-center fabric *between*
racks. Scale-out is a contest between NVIDIA's **InfiniBand**/Spectrum-X and merchant
**Ethernet** (the **Ultra Ethernet Consortium**), where **Arista** is the leading switch vendor,
running Broadcom ([[AVGO]]) Tomahawk/Jericho silicon.

Underneath sits a quieter **connectivity-silicon** layer that keeps those links reliable as
speeds hit 224G/lane: **retimers** (re-clock PCIe/CXL/Ethernet signals so they survive across a
board or cable — [[ALAB]], [[AVGO]], [[MRVL]]), **active electrical cables (AECs)** (powered
copper for short rack-to-rack reaches, cheaper/cooler than optics — [[CRDO]], Amphenol), and the
[[Optical interconnect|optical transceivers]] for longer reaches. As clusters scale, signal
integrity becomes a gating problem — which is why these once-obscure component vendors now grow
fastest.

## In this vault
- Switching: [[ANET]] (merchant AI Ethernet) — on [[AVGO]] silicon
- Connectivity silicon: [[ALAB]] (PCIe/CXL retimers) · [[CRDO]] (AECs)
- Sits between [[Optical interconnect]] (transceivers) and [[GPU interconnect]] (NVLink scale-up)
- Wires the clusters built by [[NVDA]] · [[SMCI]] for hyperscalers ([[MSFT]] et al.)

## Sources
- Ultra Ethernet Consortium and UALink consortium materials
- Arista, Astera Labs, Credo, Broadcom investor disclosures and product documentation
