#version 300 es

const int MAX_CONTROL_POINTS = 256;

const mat4 B_SPLINE_MATRIX = (1. / 6.) * mat4(
    -1, 3, -3, 1,
    3, -6, 3, 0,
    -3, 0, 3, 0,
    1, 4, 1, 0
);

const mat4 CATMULL_ROM_MATRIX = (1. / 2.) * mat4(
    -1,  3, -3,  1,
     2, -5,  4, -1,
    -1,  0,  1,  0,
     0,  2,  0,  0
);

const mat4 BEZIER_MATRIX = mat4(
    -1,  3, -3,  1,
     3, -6,  3,  0,
    -3,  3,  0,  0,
     1,  0,  0,  0
);


//smaple point index, 0 is the start of the entire line.
//sample points are the points that determines the ends of each segment.
//its value equals n*segmentsPerCurve at the end of curve n (starting at 1).
in uint index;
uniform int segmentsPerCurve;
uniform vec2 points[MAX_CONTROL_POINTS];
uniform float pointSize;
uniform int curveIndex;

mat4 getMatrix(int matrixIndex){
    switch (matrixIndex){
        case 0: return B_SPLINE_MATRIX;
        case 1: return CATMULL_ROM_MATRIX;
        case 2: return BEZIER_MATRIX;
    }
}

vec2 cubicCurve(float t, vec2 ctrlPts[4]) {
    /* float x = B0(t)*controlPoints[0].x + B1(t)*controlPoints[1].x +
     B2(t)*controlPoints[2].x + B3(t)*controlPoints[3].x;

    float y = B0(t)*controlPoints[0].y + B1(t)*controlPoints[1].y +
     B2(t)*controlPoints[2].y + B3(t)*controlPoints[3].y; */

    vec4 tVec = vec4(t * t * t, t * t, t, 1);

    vec4 PointsX = vec4(ctrlPts[0].x, ctrlPts[1].x, ctrlPts[2].x, ctrlPts[3].x);
    vec4 PointsY = vec4(ctrlPts[0].y, ctrlPts[1].y, ctrlPts[2].y, ctrlPts[3].y);

    vec4 tmp = tVec * transpose(getMatrix(curveIndex)); //row vector multiplication
    float x = dot(tmp, PointsX);
    float y = dot(tmp, PointsY);

    return vec2(x, y);
}

vec2[4] getControlPoints() {
    int curveNum = int(index) / segmentsPerCurve;

    vec2 chosenPoints[4];

    for(int i = 0; i < 4; i++) {
        chosenPoints[i] = points[curveNum + i];
    }

    return chosenPoints;
}

void main() {
    float t = fract(float(index) / float(segmentsPerCurve));

    vec2 controlPoints[4] = getControlPoints();
    vec2 position = cubicCurve(t, controlPoints);

    gl_Position = vec4(position, 0.0f, 1.0f);
    
    //determines if the current point is the end of a curve.
    if(int(index)%segmentsPerCurve == 0)
        gl_PointSize = pointSize;
}
