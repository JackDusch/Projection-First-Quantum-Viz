#version 330 core
uniform sampler2D uBackmapRG;   // hemi_backmap_rg.png (theta01, phi01)
uniform sampler2D uWeight;      // hemi_weight.png (scalar)
uniform sampler2DArray uBasis;  // array of (Re,Im) basis layers packed in RG
uniform int uK;                 // number of active layers
uniform float uOmega[128];      // angular frequencies per layer
uniform float uAlphaRe[128];    // coefficients Re
uniform float uAlphaIm[128];    // coefficients Im
uniform float uTime;

in vec2 vTex;
out vec4 fragColor;

vec2 cmul(vec2 a, vec2 b){ return vec2(a.x*b.x - a.y*b.y, a.x*b.y + a.y*b.x); }

void main(){
    vec2 tp = texture(uBackmapRG, vTex).rg; // theta01, phi01 in [0,1]
    float w  = texture(uWeight,     vTex).r; // normalized weight for integrals
    if (tp == vec2(0.0)) { fragColor = vec4(0); return; } // outside dome

    vec2 acc = vec2(0.0); // complex accumulator
    for(int k=0;k<uK;k++){
        vec2 bk = texture(uBasis, vec3(vTex, float(k))).rg; // (Re,Im) in [0,1]
        bk = (bk - 0.5) * 2.0; // back to [-1,1]
        float ph = -uOmega[k]*uTime;
        vec2 phase = vec2(cos(ph), sin(ph));
        vec2 coeff = vec2(uAlphaRe[k], uAlphaIm[k]);
        acc += cmul(cmul(bk, phase), coeff);
    }
    float intensity = dot(acc, acc); // |psi|^2
    fragColor = vec4(vec3(intensity), 1.0);
}
