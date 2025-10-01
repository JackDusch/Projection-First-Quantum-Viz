# viewfinder_demo.py
# CPU demo: render a simple analytic ψ on a unit sphere with perspective lens,
# and compute sensitivities ∂I/∂yaw and ∂I/∂dolly. Saves PNGs.
import numpy as np
from PIL import Image

PI = np.pi

def Y00():
    return 0.5*np.sqrt(1.0/PI)
def Y10(th):
    return np.sqrt(3.0/(4.0*PI)) * np.cos(th)
def Y11c(th, ph):
    return -np.sqrt(3.0/(8.0*PI)) * np.sin(th) * np.cos(ph)
def Y11s(th, ph):
    return -np.sqrt(3.0/(8.0*PI)) * np.sin(th) * np.sin(ph)

def psi_analytic_dir(d, t):
    z = d[2]
    th = np.arccos(np.clip(z, -1, 1))
    ph = np.arctan2(d[1], d[0])
    if ph < 0: ph += 2*PI
    w0, w1, w2 = 1.0, 0.7, 0.6
    E0, E1, E2 = 1.0, 1.6, 2.3
    e0 = np.array([np.cos(-E0*t), np.sin(-E0*t)])
    e1 = np.array([np.cos(-E1*t), np.sin(-E1*t)])
    e2 = np.array([np.cos(-E2*t), np.sin(-E2*t)])
    zc = np.array([Y11c(th,ph), Y11s(th,ph)])
    out = e0 * (w0*Y00()) + e1 * (w1*Y10(th)) + np.array([
        e2[0]*zc[0] - e2[1]*zc[1],
        e2[0]*zc[1] + e2[1]*zc[0]
    ])
    return out

def rotz(a):
    c,s = np.cos(a), np.sin(a)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]], dtype=float)

def hit_unit_sphere(tc, d):
    b = np.dot(tc, d)
    c = np.dot(tc, tc) - 1.0
    disc = b*b - c
    if disc < 0: return None
    s = -b - np.sqrt(disc)
    if s < 0: s = -b + np.sqrt(disc)
    if s < 0: return None
    return tc + s*d

def render_frame(W=512, H=512, fov=np.deg2rad(60), R=np.eye(3), tc=np.array([0,0,-3.0]), t=0.0):
    s = np.tan(0.5*fov)
    I = np.zeros((H,W,2), dtype=float)
    for j in range(H):
        y = (2*(j+0.5)/H - 1)
        for i in range(W):
            x = (2*(i+0.5)/W - 1)
            d_cam = np.array([x*s, y*s, 1.0])
            d_cam = d_cam/np.linalg.norm(d_cam)
            d = R @ d_cam
            hit = hit_unit_sphere(tc, d)
            if hit is None:
                continue
            val = psi_analytic_dir(hit/np.linalg.norm(hit), t)
            I[j,i,:] = val
    return I

def to_img(z):
    mag = np.sum(z*z, axis=-1)  # |psi|^2 proxy
    mag = mag / (mag.max() + 1e-9)
    return (255.0*np.clip(mag,0,1)).astype(np.uint8)

if __name__ == "__main__":
    W=512; H=512
    R = np.eye(3)
    tc = np.array([0,0,-3.0])
    eps = 1e-3
    t = 0.0

    I0 = render_frame(W,H,np.deg2rad(60),R,tc,t)

    Rp = rotz(+eps) @ R
    Rm = rotz(-eps) @ R
    Iy_p = render_frame(W,H,np.deg2rad(60),Rp,tc,t)
    Iy_m = render_frame(W,H,np.deg2rad(60),Rm,tc,t)
    dYaw = (Iy_p - Iy_m) / (2*eps)

    fwd = R @ np.array([0,0,1.0])
    Id_p = render_frame(W,H,np.deg2rad(60),R,tc + eps*fwd,t)
    Id_m = render_frame(W,H,np.deg2rad(60),R,tc - eps*fwd,t)
    dDolly = (Id_p - Id_m) / (2*eps)

    Image.fromarray(to_img(I0)).save("viewfinder_I.png")
    Image.fromarray(to_img(dYaw)).save("viewfinder_dYaw.png")
    Image.fromarray(to_img(dDolly)).save("viewfinder_dDolly.png")
    print("Saved viewfinder_I.png, viewfinder_dYaw.png, viewfinder_dDolly.png")
