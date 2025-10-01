# Projection‑First Quantum Visualization Kit

A minimal, **unitary & measure‑correct** framework to render and manipulate quantum wavefields through **projection-first** lenses (hemispherical / equirectangular), outsource integrals to the GPU, and shuttle results consistently between lenses.

## Features
- **Python bakers** for back‑maps and Jacobian **weights** for hemispherical and equirectangular projections.
- **GLSL shaders** for (a) hemispherical superposition rendering, (b) equirectangular → hemispherical resampling (unitary shuttle), and (c) a parameter‑driven **viewfinder** that emits sensitivities ∂I/∂(yaw,dolly).
- **Examples** to extract frames from a video and generate a side‑by‑side **composite** figure.
- **Docs** explaining the math: lens weights, operator transport, boundary topology (cylinder/Möbius), and how to use this as a domain for geometric neural nets.

## Quick Start
```bash
pip install -r requirements.txt

# Bake projection assets (hemi + eq), and optional Y_{ℓm} layers
python src/bake_textures.py

# CPU reference demo (perspective lens on unit sphere)
python src/viewfinder_demo.py

# Optional: Extract frames from a video and build a comparison composite
python examples/extract_frames.py --video "/path/to/video.mp4" --out examples/frames
python examples/compare_composite.py --frames examples/frames --out examples/composite.png
```
