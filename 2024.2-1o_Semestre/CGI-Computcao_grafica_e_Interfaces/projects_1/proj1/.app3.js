
import { buildProgramFromSources, loadShadersFromURLS, setupWebGL } from "../../libs/utils.js";
import { vec2, flatten } from "../../libs/MV.js";

class Curve {
    constructor() {
        this.controlPoints = [];
        this.directions = [];
        this.globalCurveDirection = vec2(Math.round(Math.random()), Math.round(Math.random()));
        this.color = [Math.random(), Math.random(), Math.random()];
        this.opacity = 0.5 + Math.random() * 0.5;//[.5, 1]
        this.pointSize = 5 + Math.random() * 15;//[5, 20]
        this.finishedSetup = false;
    }

    addControlPoint(point) {
        this.controlPoints.push(point);
        //random direction, essentially normalized vectors.
        const direction = vec2(Math.random(), Math.random());
        console.log("direction is " + direction);
        this.directions.push(direction);
        showControlPoints();
    }

    update(speed) {
        for (let i = 0; i < this.controlPoints.length; i++) {

            //apply individual point movement (slight jerk)
            this.controlPoints[i][0] = this.controlPoints[i][0] + this.directions[i][0] * speed;
            this.controlPoints[i][1] = this.controlPoints[i][1] + this.directions[i][1] * speed;

            //apply global curve movement (has more impact)
            this.controlPoints[i][0] = this.controlPoints[i][0] + this.globalCurveDirection[0] * speed * 0.02;
            this.controlPoints[i][1] = this.controlPoints[i][1] + this.globalCurveDirection[1] * speed * 0.02;

            //reverse velocity component if hitting an edge (bounce)
            if (this.controlPoints[i][0] > 1 || this.controlPoints[i][0] < -1) {
                this.directions[i][0] *= -1;
            }
            if (this.controlPoints[i][1] > 1 || this.controlPoints[i][1] < -1) {
                this.directions[i][1] *= -1;
            }
        }
    }
}

var gl;
var canvas;

var draw_program;

var segmentsPerCurveLocation;
var pointsLocation;
var curveColorLocation;
var pointSizeLocation;
var curveIndexLocation;
var timeLocation;
var glowIntensityLocation;

var curves = [new Curve()];
var currentCurveIndex = 0;

var segmentsPerCurve = 25;
var controlPoints = true;
var segmentLines = true;
var doTimeSpeedIncrease = false;
var timeSpeedIncreaseModifier = 1000000;
var starMode = false;
var speed = 0.005;
var tmpSpeed = 0;
var shadowIntensity = 0.0;


var curveIndex = 0;

/**
 * Resize event handler
 * 
 * @param {*} target - The window that has resized
 */
function resize(target) {
    const width = target.innerWidth;
    const height = target.innerHeight;
    canvas.width = width;
    canvas.height = height;
    gl.viewport(0, 0, width, height);
}

function handleKeyInput(event) {
    switch (event.key) {
        case 'z':
        case 'Z':
            curves[currentCurveIndex].finishedSetup = true;
            curves.push(new Curve());
            currentCurveIndex++;
            break;

        case 'c':
        case 'C':
            curves = [new Curve()];
            currentCurveIndex = 0;
            break;

        case '+':
            if (segmentsPerCurve + 1 <= 50) segmentsPerCurve++;
            console.log(`segmentsPerCurve: ${segmentsPerCurve}`);
            break;

        case '-':
            if (segmentsPerCurve - 1 >= 1) segmentsPerCurve--;
            console.log(`segmentsPerCurve: ${segmentsPerCurve}`);
            break;

        case 'p':
        case 'P':
            controlPoints = !controlPoints;
            break;

        case 'L':
        case 'l':
            segmentLines = !segmentLines;
            break;

        case ' ':
            if (tmpSpeed === 0) {
                tmpSpeed = speed;
                speed = 0;
            }
            else {
                speed = tmpSpeed;
                tmpSpeed = 0;
            }
            break;

        case '>':
            speed += 0.001;
            break;

        case '<':
            speed -= 0.001;
            break;

        case 'm':
        case 'M':
            curveIndex = (curveIndex + 1) % 3;
            break;

        case 't':
        case 'T':
            doTimeSpeedIncrease = !doTimeSpeedIncrease;

        case 'h':
            console.log("speed increased")
            timeSpeedIncreaseModifier -= 100000;
            break;

        case 'j':
            timeSpeedIncreaseModifier += 100000;
            break;

        case 'r':
        case 'R':
            starMode = !starMode;
            break;

        case 'g':
        case 'G':
            if (shadowIntensity === 0.) {
                shadowIntensity = 5.; 
            } else {
                shadowIntensity = 0.;
            }
            break;
    }
}

function setup(shaders) {
    canvas = document.getElementById("gl-canvas");
    gl = setupWebGL(canvas, { alpha: true });

    draw_program = buildProgramFromSources(gl, shaders["shader.vert"], shaders["shader.frag"]);

    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

    window.addEventListener("resize", (event) => resize(event.target));

    function get_pos_from_mouse_event(canvas, event) {
        const rect = canvas.getBoundingClientRect();
        const x = (event.clientX - rect.left) / canvas.width * 2 - 1;
        const y = -((event.clientY - rect.top) / canvas.height * 2 - 1);
        return vec2(x, y);
    }

    window.addEventListener("mousedown", (event) => {
        curves[currentCurveIndex].addControlPoint(get_pos_from_mouse_event(canvas, event));
        //showControlPoints();
    });

    window.addEventListener("keydown", (event) => handleKeyInput(event));

    resize(window);

    var indxArr = Array.from(Array(60000).keys());

    const aBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, aBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Uint32Array(indxArr), gl.STATIC_DRAW);

    const index = gl.getAttribLocation(draw_program, "index");
    gl.vertexAttribIPointer(index, 1, gl.UNSIGNED_INT, 0, 0);
    gl.enableVertexAttribArray(index);

    gl.clearColor(0.0, 0.0, 0.0, 1);

    segmentsPerCurveLocation = gl.getUniformLocation(draw_program, "segmentsPerCurve");
    console.log("loc: " + segmentsPerCurveLocation);
    pointsLocation = gl.getUniformLocation(draw_program, "points");
    curveColorLocation = gl.getUniformLocation(draw_program, "curveColor");
    pointSizeLocation = gl.getUniformLocation(draw_program, "pointSize");
    curveIndexLocation = gl.getUniformLocation(draw_program, "curveIndex");
    timeLocation = gl.getUniformLocation(draw_program, "time");
    glowIntensityLocation = gl.getUniformLocation(draw_program, "glowIntensity");

    window.requestAnimationFrame(animate);
}

let last_time;

/**
 * Animation function
 */
function animate(timestamp) {
    window.requestAnimationFrame(animate);

    if (last_time === undefined) {
        last_time = timestamp;
    }

    if (doTimeSpeedIncrease) {
        const elapsed = timestamp - last_time;
        speed = speed + elapsed / timeSpeedIncreaseModifier; //VERY slow speed increase.
    }

    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(draw_program);
    gl.uniform1i(segmentsPerCurveLocation, segmentsPerCurve);
    gl.uniform1i(curveIndexLocation, curveIndex);
    gl.uniform1f(glowIntensityLocation, shadowIntensity); 
    if (starMode)
        gl.uniform1f(timeLocation, timestamp / 100.);
    else
        gl.uniform1f(timeLocation, 0.);

    for (let curve of curves) {
        //only start moving curves after z is pressed.
        if (curve.finishedSetup)
            curve.update(speed);

        if (curve.controlPoints.length >= 4) {
            gl.uniform2fv(pointsLocation, flatten(curve.controlPoints));
            gl.uniform3fv(curveColorLocation, curve.color);
            gl.uniform1f(pointSizeLocation, curve.pointSize);

            const numSegments = (curve.controlPoints.length - 3) * segmentsPerCurve + 1;
            if (segmentLines)
                gl.drawArrays(gl.LINE_STRIP, 0, numSegments);
            if (controlPoints) {
                gl.drawArrays(gl.POINTS, 0, numSegments);
            }
        }
    }

    gl.useProgram(null);
    last_time = timestamp;
}

/**
 * Display registered control points
 */
function showControlPoints() {
    if (currentCurveIndex >= 0) {
        console.log("Registered control points:");
        curves[currentCurveIndex].controlPoints.forEach((point) => console.log(`${point[0]} ${point[1]}`));
    }
}

loadShadersFromURLS(["shader.vert", "shader.frag"]).then(shaders => setup(shaders));
