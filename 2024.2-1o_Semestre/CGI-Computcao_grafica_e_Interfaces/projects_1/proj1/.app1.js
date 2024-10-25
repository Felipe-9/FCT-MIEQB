
import { buildProgramFromSources, loadShadersFromURLS, setupWebGL } from "../../libs/utils.js";
import { vec4, vec2, flatten } from "../../libs/MV.js";

var gl;
var canvas;
var draw_program;

var curves = [];
var currentCurve = { points: [], velocities: [], color: null, opacity: null, size: null };
var tValues = [];
var tBuffer;

var numSegmentsPerSection = 8;
var animationVelocity = 1;
var minDistance = 0.1;

var isMoving = false;
var isMouseDown = false;
var showPoints = true;
var showCurves = true;
var isMouseOverSomething = false;
var bigCurve = false;

const MAX_TVALUES = 60000;
const u_fBSpline = 6.0;
const u_fCatmullRom = 2.0;
const u_fBezier = 1.0;

const coefficientsBSpline = [
  -1.0, 3.0, -3.0, 1.0,
  3.0, -6.0, 0.0, 4.0,
  -3.0, 3.0, 3.0, 1.0,
  1.0, 0.0, 0.0, 0.0
];

const coefficientsCatmullRom = [
  -1.0, 2.0, -1.0, 0.0,
  3.0, -5.0, 0.0, 2.0,
  -3.0, 4.0, 1.0, 0.0,
  1.0, -1.0, 0.0, 0.0
];

const coefficientsBezier = [
  -1.0, 3.0, -3.0, 1.0,
  3.0, -6.0, 3.0, 0.0,
  -3.0, 3.0, 0.0, 0.0,
  1.0, 0.0, 0.0, 0.0
];

var currentCoefficients = coefficientsBSpline;
var current_f = u_fBSpline;

const button1 = document.getElementById("buttonMatrix1");
const button2 = document.getElementById("buttonMatrix2");
const button3 = document.getElementById("buttonMatrix3");
const segmentSlider = document.getElementById('segmentSlider');
const speedSlider = document.getElementById('speedSlider');
const segmentValue = document.getElementById('segmentValue');
const speedValue = document.getElementById('speedValue');

button1.addEventListener("click", () => {
  currentCoefficients = coefficientsBSpline;
  current_f = u_fBSpline;
});

button2.addEventListener("click", () => {
  currentCoefficients = coefficientsCatmullRom;
  current_f = u_fCatmullRom;
});

button3.addEventListener("click", () => {
  currentCoefficients = coefficientsBezier;
  current_f = u_fBezier;
});

segmentSlider.addEventListener('input', function() {
  numSegmentsPerSection = parseInt(segmentSlider.value, 10);
  segmentValue.textContent = numSegmentsPerSection;
  initializeTValues();
});

speedSlider.addEventListener('input', function() {
  animationVelocity = parseFloat(speedSlider.value);
  speedValue.textContent = animationVelocity.toFixed(1);
});

function updateSlider(slider, value, parameter) {
  slider.value = parameter;
  value.textContent = parameter;
}

const elements = ['.sliders', '.legend', '.form'];

elements.forEach(selector => {
  const element = document.querySelector(selector);
  element.addEventListener('mouseover', () => {
    isMouseOverSomething = true;
  });
  element.addEventListener('mouseout', () => {
    isMouseOverSomething = false;
  });
});

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

function setup(shaders) {
  canvas = document.getElementById("gl-canvas");
  gl = setupWebGL(canvas, { alpha: true });

  draw_program = buildProgramFromSources(
    gl,
    shaders["shader.vert"],
    shaders["shader.frag"],
  );

  tBuffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, tBuffer);

  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);


  window.addEventListener("resize", (event) => {
    resize(event.target);
  });

  function get_pos_from_mouse_event(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const x = (event.clientX - rect.left) / canvas.width * 2 - 1;
    const y = -((event.clientY - rect.top) / canvas.height * 2 - 1);
    return vec2(x, y);
  }

  window.addEventListener("mousedown", (event) => {
    if (event.button === 0) {
      if (!isMouseOverSomething) {
        const pos = get_pos_from_mouse_event(canvas, event);
        addPointToCurve(pos);
        isMouseDown = true;
      }
    }
  });

  window.addEventListener("mousemove", (event) => {
    if (isMouseDown && !isMouseOverSomething) {
      const pos = get_pos_from_mouse_event(canvas, event);
      const lastPoint = currentCurve.points[currentCurve.points.length - 1];
      if (!lastPoint || distance(pos, lastPoint) > minDistance) {
        addPointToCurve(pos);
        bigCurve = true;
      }
    }
  });

  window.addEventListener("mouseup", (event) => {
    if (event.button === 0) {
      isMouseDown = false;
      if (bigCurve) {
        curves.push(currentCurve);
        cleanCurrentCurve();
      }
      bigCurve = false;
    }
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === " ") {
      isMoving = !isMoving;
    } else if (event.key === "z") {
      if (currentCurve.points.length >= 4) {
        curves.push(currentCurve);
        cleanCurrentCurve();
      }
    } else if (event.key === "c") {
      curves = [];
      cleanCurrentCurve();
    } else if (event.key === "p") {
      showPoints = !showPoints;
    } else if (event.key === "l") {
      showCurves = !showCurves;
    } else if (event.key === "+") {
      numSegmentsPerSection = Math.max(1, Math.min(numSegmentsPerSection + 1, 50))
      updateSlider(segmentSlider, segmentValue, numSegmentsPerSection,)
      initializeTValues();
    } else if (event.key === "-") {
      numSegmentsPerSection = Math.max(1, Math.min(numSegmentsPerSection - 1, 50))
      updateSlider(segmentSlider, segmentValue, numSegmentsPerSection,)
      initializeTValues();
    } else if (event.key === "<") {
      animationVelocity = Math.max(1, animationVelocity - 1);
      updateSlider(speedSlider, speedValue, animationVelocity,)
    } else if (event.key === ">") {
      animationVelocity = Math.min(20, animationVelocity + 1);
      updateSlider(speedSlider, speedValue, animationVelocity,)
    }
  });

  initializeTValues();

  resize(window);
  gl.clearColor(0.0, 0.0, 0.0, 1);
  window.requestAnimationFrame(animate);
}

function initializeTValues() {
  tValues = Array.from({ length: Math.min(numSegmentsPerSection, MAX_TVALUES) }, (_, i) => i);
  // tValues = [];
  // for (let j = 0; j <= numSegmentsPerSection && tValues.length <= MAX_TVALUES; j++) {
  //     tValues.push(j);
  // }
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(tValues), gl.STATIC_DRAW);
}

function addPointToCurve(pos) {
  currentCurve.points.push(pos);
  const v = vec2((Math.random() - 0.5) * 0.01, (Math.random() - 0.5) * 0.01);
  currentCurve.velocities.push(v);
  if (!currentCurve.color) {
    currentCurve.color = vec4(Math.random(), Math.random(), Math.random(), 1.0);
  }
  if (!currentCurve.opacity) {
    currentCurve.opacity = Math.random() * 0.4 + 0.4;
  }
  if (!currentCurve.size) {
    currentCurve.size = Math.random() * 25.0 + 25.0;
  }
}

function cleanCurrentCurve() {
  currentCurve = { points: [], velocities: [], color: null, opacity: null };
}

function distance(p1, p2) {
  return Math.sqrt(Math.pow(p1[0] - p2[0], 2) + Math.pow(p1[1] - p2[1], 2));
}

function updateControlPoints(curve, deltaTime) {
  for (let i = 0; i < curve.points.length; i++) {
    curve.points[i][0] += curve.velocities[i][0] * animationVelocity * deltaTime;
    curve.points[i][1] += curve.velocities[i][1] * animationVelocity * deltaTime;
    if (curve.points[i][0] > 1.0 || curve.points[i][0] < -1.0) {
      curve.velocities[i][0] *= -1;
    }
    if (curve.points[i][1] > 1.0 || curve.points[i][1] < -1.0) {
      curve.velocities[i][1] *= -1;
    }
  }
}

function drawBSplineCurve(curve, isPoint) {
  const colorLocation = gl.getUniformLocation(draw_program, "u_color");
  gl.uniform4fv(colorLocation, flatten(curve.color));

  const opacityLocation = gl.getUniformLocation(draw_program, "u_opacity");
  gl.uniform1f(opacityLocation, curve.opacity);

  const pointSizeLocation = gl.getUniformLocation(draw_program, "u_pointSize");
  gl.uniform1f(pointSizeLocation, curve.size);

  const segmentsLocation = gl.getUniformLocation(draw_program, "u_nSegments");
  gl.uniform1i(segmentsLocation, numSegmentsPerSection);

  const tLocation = gl.getAttribLocation(draw_program, "aT");
  gl.enableVertexAttribArray(tLocation);
  gl.vertexAttribPointer(tLocation, 1, gl.FLOAT, false, 0, 0);

  if (isPoint) {
    gl.drawArrays(gl.POINTS, 0, numSegmentsPerSection + 1);
  } else {
    gl.drawArrays(gl.LINE_STRIP, 0, numSegmentsPerSection + 1);
  }
}

function drawCurve(curve, int) {
  if (curve.points.length >= 4) {
    for (let i = 0; i <= curve.points.length - 4; i += int) {
      const controlPoints = curve.points.slice(i, i + 4);
      const controlPointsLocation = gl.getUniformLocation(draw_program, "u_controlPoints");
      gl.uniform2fv(controlPointsLocation, flatten(controlPoints));

      drawBSplineCurve(curve, !showCurves);
    }
  }
}

function drawCurveType(curve) {
  if (currentCoefficients == coefficientsBezier) {
    drawCurve(curve, 3)
  } else {
    drawCurve(curve, 1);
  }
}


let last_time;

function animate(timestamp) {
  window.requestAnimationFrame(animate);

  if (last_time === undefined) {
    last_time = timestamp;
  }

  const deltaTime = (timestamp - last_time) / 10;

  if (isMoving) {
    curves.forEach(curve => updateControlPoints(curve, deltaTime)); // Pass deltaTime to update function
  }

  const matrixLocation = gl.getUniformLocation(draw_program, "u_matrix");
  const fLocation = gl.getUniformLocation(draw_program, "u_coefficient");

  gl.clear(gl.COLOR_BUFFER_BIT);

  gl.useProgram(draw_program);

  gl.uniformMatrix4fv(matrixLocation, false, flatten(currentCoefficients));
  gl.uniform1f(fLocation, current_f);

  curves.forEach((curve) => {
    drawCurveType(curve);
  });

  drawCurveType(currentCurve);

  gl.useProgram(null);
  last_time = timestamp;
}

loadShadersFromURLS(["shader.vert", "shader.frag"]).then(shaders => setup(shaders));
