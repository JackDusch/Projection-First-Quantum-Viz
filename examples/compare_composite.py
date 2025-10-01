# compare_composite.py
import argparse, os, glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--frames", required=True, help="Folder containing extracted frames (PNGs)")
parser.add_argument("--out", required=True, help="Output composite image path")
args = parser.parse_args()

frame_paths = sorted(glob.glob(os.path.join(args.frames, "*.png")))
if not frame_paths:
    raise SystemExit("No frames found.")

# Mock traditional spherical harmonic magnitude (Y_3^2-like) for comparison
theta = np.linspace(0, np.pi, 256)
phi = np.linspace(0, 2*np.pi, 512)
TH, PH = np.meshgrid(theta, phi, indexing="ij")
Y = np.abs((np.sin(TH)**2) * np.cos(TH) * np.exp(2j*PH))
Y = (Y - Y.min()) / (Y.max() - Y.min())

rows = len(frame_paths)
fig, axes = plt.subplots(rows, 2, figsize=(10, 4*rows))

for i, fp in enumerate(frame_paths):
    img = Image.open(fp).convert("RGB")
    axes[i,0].imshow(img)
    axes[i,0].set_title(f"Projection‑first Frame {i+1}")
    axes[i,0].axis("off")

    axes[i,1].imshow(Y, cmap="inferno", aspect="auto")
    axes[i,1].set_title("Traditional Orbital (mock Y₃²)")
    axes[i,1].axis("off")

plt.tight_layout()
plt.savefig(args.out, dpi=200)
print("wrote", args.out)
