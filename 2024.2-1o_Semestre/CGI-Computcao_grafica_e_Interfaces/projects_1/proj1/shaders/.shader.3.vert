#version 300 es
#define MAX_POINTS 256

in int a_index; // index inside controlPoints
// drawing settings
uniform int u_segmentsPerCurve; // segments to draw curve
uniform vec2 u_controlPoints[MAX_POINTS]; // control points positions
// curve uniforms
uniform float u_pointSize; // point sizes
uniform uint u_matrix; // M selector for cubic curve

const mat4 bsplines= (1. / 6.) * mat4(
    -1, 3, -3, 1,
    3, -6, 3, 0,
    -3, 0, 3, 0,
    1, 4, 1, 0
);
const mat4 catmullrom= mat4(
  -0.5, +1.0, -0.5, +0.0,
  +1.5, -2.5, +0.0, +1.0,
  -1.5, +2.0, +0.5, +0.0,
  +0.5, -0.5, +0.0, +0.0
);
const mat4 bezier= mat4(
  -1.0, +3.0, -3.0, +1.0,
  +3.0, -6.0, +3.0, +0.0,
  -3.0, +3.0, +0.0, +0.0,
  +1.0, +0.0, +0.0, +0.0
);

void main() {
  float t 
    = float(a_index % u_segmentsPerCurve)
    / float(u_segmentsPerCurve);

  vec4 T = vec4(t*t*t, t*t, t, 1);

  int cpIndex = a_index/u_segmentsPerCurve;

  vec4 Px = vec4(
    u_controlPoints[cpIndex].x,
    u_controlPoints[cpIndex+1].x,
    u_controlPoints[cpIndex+2].x,
    u_controlPoints[cpIndex+3].x
  );
  vec4 Py = vec4(
    u_controlPoints[cpIndex].y,
    u_controlPoints[cpIndex+1].y,
    u_controlPoints[cpIndex+2].y,
    u_controlPoints[cpIndex+3].y
  );

  mat4 M;
  switch (u_matrix) {
    case 1u: M=catmullrom; break;
    case 2u: M=bezier; break;
    default: M=bsplines; break;
  };

  M = transpose(M);
  vec4 tmp = T * M;
  float pos_x = dot(tmp, Px);
  float pos_y = dot(tmp, Py);

  gl_Position = vec4(pos_x, pos_y, 0.0, 1.0);
  // gl_Position = vec4(0.5, 0.5, 0.0, 1.0);

  if(int(a_index)%u_segmentsPerCurve == 0)
    gl_PointSize = u_pointSize;
}
