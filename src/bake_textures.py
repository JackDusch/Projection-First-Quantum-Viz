# bake_textures.py
# Python 3.x. Requires: numpy, pillow, scipy
import numpy as np
from PIL import Image
from scipy.special import sph_harm

def to_u8(img):
    img = np.clip(img, 0.0, 1.0)
    return (img * 255.0 + 0.5).astype(np.uint8)

def save_gray(path, arr):
    Image.fromarray(to_u8(arr)).save(path)

def save_rg(path, rg):
    # rg in [0,1], 2 channels packed into RG of an RGBA PNG
    h, w, _ = rg.shape
    out = np.zeros((h, w, 4), dtype=np.uint8)
    out[...,0:2] = to_u8(rg)
    out[...,3] = 255
    Image.fromarray(out, mode='RGBA').save(path)

def save_complex_as_rg(path, z):
    # map complex to (re, im) in [0,1] via 0.5+0.5*x (assuming |z|<=1)
    re = 0.5 + 0.5 * np.real(z)
    im = 0.5 + 0.5 * np.imag(z)
    save_rg(path, np.stack([re, im], axis=-1))

def bake_hemi_backmap_and_weight(R):
    """
    Hemispherical (azimuthal-equidistant): r = (2R/pi)*theta
    Weight: w(r) = (pi/(2R)) * sin(pi*r/(2R)) / r, with center limit (pi/(2R))^2
    Returns:
      backmap (H=W=2R,2): channels = (theta01, phi01)
      w (H=W): raw weight (not normalized)
      mask (H=W): inside-disk boolean mask
    """
    S = 2*R
    y, x = np.mgrid[0:S, 0:S].astype(np.float64)
    cx, cy = R, R
    dx = x - cx
    dy = y - cy
    r = np.sqrt(dx*dx + dy*dy)
    inside = (r <= R)

    theta = (np.pi * 0.5) * (r / R)
    phi = np.arctan2(dy, dx) % (2*np.pi)

    w = np.zeros_like(r)
    eps = 1e-12
    r_safe = np.maximum(r, eps)
    w_val = (np.pi / (2.0 * R)) * np.sin((np.pi * r_safe) / (2.0 * R)) / r_safe
    w[...] = w_val
    w[r < eps] = (np.pi/(2.0*R))**2

    theta01 = np.clip(theta / (np.pi * 0.5), 0.0, 1.0)
    phi01   = phi / (2.0 * np.pi)

    backmap = np.zeros((S, S, 2), dtype=np.float64)
    backmap[...,0] = theta01
    backmap[...,1] = phi01
    backmap[~inside,:] = 0.0

    w_img = np.zeros_like(r)
    scale = np.max(w[inside])
    if scale > 0:
        w_img[inside] = w[inside] / scale

    return backmap, w, inside

def bake_eq_backmap_and_weight(W, H):
    """
    Equirectangular (hemisphere): x=phi, y=theta, with theta in [0,pi/2]
    Weight: w(theta) = sin(theta) / (alpha*beta)  (constant scale omitted)
    Returns:
      backmap (H,W,2): (theta01, phi01)
      w (H,W): raw sin(theta)
      mask: ones
    """
    y, x = np.mgrid[0:H, 0:W].astype(np.float64)
    phi = (x / W) * 2.0 * np.pi
    theta = (y / H) * (np.pi * 0.5)

    w = np.sin(theta)

    theta01 = theta / (np.pi * 0.5)
    phi01   = phi / (2.0 * np.pi)
    backmap = np.stack([theta01, phi01], axis=-1)

    return backmap, w, np.ones((H, W), dtype=bool)

def bake_Ylm_layers(theta, phi, Lmax):
    layers = []
    for l in range(Lmax+1):
        for m in range(-l, l+1):
            Y = sph_harm(m, l, phi, theta)  # complex
            layers.append(Y)
    return layers

if __name__ == '__main__':
    # Hemispherical assets
    R = 512
    back_hemi, w_hemi, mask_hemi = bake_hemi_backmap_and_weight(R)
    Image.fromarray((back_hemi[...,0]*255).astype(np.uint8)).save('hemi_theta.png')
    Image.fromarray((back_hemi[...,1]*255).astype(np.uint8)).save('hemi_phi.png')
    save_rg('hemi_backmap_rg.png', back_hemi)
    w_norm = np.zeros_like(w_hemi)
    w_norm[mask_hemi] = w_hemi[mask_hemi] / w_hemi[mask_hemi].max()
    save_gray('hemi_weight.png', w_norm)

    theta = back_hemi[...,0] * (np.pi * 0.5)
    phi   = back_hemi[...,1] * (2.0 * np.pi)
    Lmax = 6
    layers = bake_Ylm_layers(theta, phi, Lmax)
    idx = 0
    for l in range(Lmax+1):
        for m in range(-l, l+1):
            Z = layers[idx] * mask_hemi
            save_complex_as_rg(f'Y_{l}_{m}_hemi.png', Z)
            idx += 1

    # Equirectangular assets
    W, H = 2048, 1024
    back_eq, w_eq, _ = bake_eq_backmap_and_weight(W, H)
    save_rg('eq_backmap_rg.png', back_eq)
    save_gray('eq_weight.png', w_eq / w_eq.max())

    theta_eq = back_eq[...,0] * (np.pi * 0.5)
    phi_eq   = back_eq[...,1] * (2.0 * np.pi)
    layers_eq = bake_Ylm_layers(theta_eq, phi_eq, Lmax)
    idx = 0
    for l in range(Lmax+1):
        for m in range(-l, l+1):
            Z = layers_eq[idx]
            save_complex_as_rg(f'Y_{l}_{m}_eq.png', Z)
            idx += 1

    print('Baking complete.')
