# LENSES: Formulas & Weights

Let image radius be R (pixels) for the dome.

## Hemispherical (azimuthal‑equidistant)
r = (2R/π) θ, φ = φ.

Weight:
w_hemi(r) = (π/(2R)) * sin(π r/(2R)) / r,  with center limit (π/(2R))^2.

## Orthographic
r = R sin θ.  Weight:  w_ortho(r) = 1 / (R^2 √(1 − (r/R)^2)).

## Stereographic
r = 2R tan(θ/2).  Weight:  w_stereo(r) = 1 / (R^2 (1 + (r/2R)^2)^2).

## Equirectangular (hemisphere)
x = α φ, y = β θ with θ∈[0, π/2]. 
Weight: w_eq(θ) ∝ sin θ  (constant scale can be dropped).
