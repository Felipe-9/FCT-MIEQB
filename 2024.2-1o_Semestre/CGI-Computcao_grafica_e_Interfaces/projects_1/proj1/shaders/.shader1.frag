#version 300 es

precision mediump float;

in vec4 vColor;

out vec4 frag_color;

void main() {
    vec2 coord = gl_PointCoord;

    float dist = distance(coord, vec2(0.5f, 0.5f));

    if(dist < 0.5f) {
        float opacityFactor = smoothstep(0.6f, 0.0f, dist);
        frag_color = vec4(vColor.rgb, vColor.a * opacityFactor);
    } else {
        discard;
    }
}
