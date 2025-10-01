# THEORY: Projection‑First Physics (Concise)

**Isometry.** A projection (lens) \(\phi: \Omega \to \Pi\) induces a pullback \(\tilde f=f\circ \phi^{-1}\) and weight \(w=|\det D\phi^{-1}|\) so that
\[
\langle f,g\rangle_{\Omega}=\int_{\Pi} \tilde f\,\overline{\tilde g}\,w\,dx.
\]
Thus rendering on \(\Pi\) can preserve norms and inner products faithfully (with the correct Jacobian).

**Unitary shuttle.** For lenses \(\phi_1,\phi_2\), \(\mathcal U_{2\leftarrow1}=\mathcal P_{\phi_2}\mathcal P_{\phi_1}^{-1}\) is unitary: compute where cheap, render where pedagogically useful.

**Operator transport.** Linear operator \(Tf=\int K f\) maps to the screen as
\[
(\tilde T\tilde f)(x)=\int_\Pi K(\phi^{-1}(x),\phi^{-1}(y))\,\tilde f(y)\,w(y)\,dy.
\]
On GPUs this is a weighted texture gather.

**Boundary topology.** Equirectangular identifies left/right edges (cylinder); a mirrored identification gives a Möbius seam. Hemispherical maps a hemisphere to a disk; rims show cusp‑like caustics where magnification spikes.

**Wheeler–Feynman on screens.** Choice of advanced/retarded kernels only changes screen **phases**; two‑sided boundary consistency is implemented by the projector kernel.

**Geometric DL.** Lenses are gauges; \(\mathcal U\)-consistency losses enforce equivariance across lenses. Graphs over pixels can carry geodesic distances via back‑maps.
