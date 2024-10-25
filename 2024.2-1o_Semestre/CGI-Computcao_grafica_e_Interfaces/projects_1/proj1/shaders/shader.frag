#version 300 es

precision mediump float;

out vec4 frag_color;

uniform vec3 u_color; // drawing color
uniform float u_alpha; // drawing opacity

void main() {
  frag_color = vec4(u_color.rgb,u_alpha);
}
