---
type: concept
updated: 2026-06-13
---
# CUDA (software moat)

CUDA is NVIDIA's proprietary software platform for running general-purpose work on its GPUs — the compilers, libraries (cuDNN, cuBLAS and the rest) and tools that AI frameworks like PyTorch are built and tuned against. It has been compounding since the mid-2000s, so in practice nearly every AI model, and the people who write them, assume NVIDIA hardware underneath.

That is the real lock-in: a rival can match the raw silicon, but moving a codebase off CUDA means rewriting and re-optimizing against a less mature stack. AMD's ROCm is the main open alternative, and hyperscalers route around CUDA with their own software for their in-house chips — but for the merchant market, CUDA is why [[NVDA]]'s moat is software, not just the chip. It's a commercial/ecosystem gate rather than a physical one, which is why NVDA rates High and not Extreme.

## In this vault
- Owned by: [[NVDA]] · alternatives: AMD ROCm, hyperscaler custom stacks (external)
- Map: [[AI Supply Chain]] → Chip design

## Sources
- [NVIDIA — CUDA Zone (canonical reference)](https://developer.nvidia.com/cuda-zone)
