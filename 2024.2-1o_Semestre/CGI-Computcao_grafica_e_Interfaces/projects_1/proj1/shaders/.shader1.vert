#version 300 es

in float aT;

uniform vec2 u_controlPoints[4];

uniform mat4 u_matrix;

uniform float u_coefficient;

uniform vec4 u_color;

uniform float u_opacity;

uniform float u_pointSize;

uniform int u_nSegments;

out vec4 vColor;

void main() {
    float t = aT / float(u_nSegments);
    float t2 = t * t;
    float t3 = t2 * t;

    vec4 b = vec4(t3, t2, t, 1) * (u_matrix / u_coefficient);
 
    vec2 position = b[0] * u_controlPoints[0] +
        b[1] * u_controlPoints[1] +
        b[2] * u_controlPoints[2] +
        b[3] * u_controlPoints[3];

    gl_Position = vec4(position, 0.0f, 1.0f);

    gl_PointSize = u_pointSize;

    vColor = vec4(u_color.rgb, u_opacity);
}
