import {
  buildProgramFromSources,
  loadShadersFromURLS,
  setupWebGL,
} from "./libs/utils.js";
import { vec2, flatten } from "./libs/MV.js";

const MAX_SEGMENTS_QTY = 60000;

let gl;
let canvas;
// let aspect;
let draw_program;

const uniforms = {
  loc: [],
  keys: [
    "u_segmentsPerCurve",
    "u_controlPoints",
    "u_color",
    "u_alpha",
    "u_pointSize",
    "u_curveType",
  ],
};

let is_moving    = false; // curves are moving condition
let is_mousedown = false; // mousedown toggle (for tracing line)


let animationVelocity = 1; // time multiplier
let segmentsPerCurve  = 10; // number of segments for each curve
let mouseDragDistance = 0.1; // distance between points when draggin with mouse
let selectedCurveType = 0b00; // current cubic curve matrix
let displayPoints     = true; // display points
let displayCurves     = false;// display curves

class Curve {
  #velocity; // curve base velocity
  #p_pos; // points position
  #p_vel; // points velocity
  #color; // curve color
  #alpha; // curve opacity
  #pointSize; // curve point size
  #curveType; // 0,1,2
  // 0b00 => bsplines
  // 0b01 => catmullrom
  // 0b10 => bezier

  constructor(pos=[],curveType=0b00) {
    if ( !Array.isArray(pos)){
      throw new TypeError("invalid type points",{cause:pos})
    }
    // Points must be array
    // if points are array of pos, convert to array of CurvePoints
    this.#color     = Array.from({ length: 3 }, _ => Math.random());
    this.#alpha     = Math.random() * 0.7 + 0.3;
    this.#velocity  = [Curve.#random_vel(0.2),Curve.#random_vel(0.2)];
    this.#pointSize = Math.random() * 20 + 5;
    this.#curveType = curveType;

    this.#p_pos = pos;
    this.#p_vel = Array.from({ length: pos.length }, _ => this.#genPointVelocity);

    return this;
  };

  static #random_vel = (v) => (Math.random() - 0.5) * v / 50;
  get #genPointVelocity() {
    return [
      this.#velocity[0] + Curve.#random_vel(0.05),
      this.#velocity[1] + Curve.#random_vel(0.05),
    ]
  }

  get length() {return this.#p_pos.length};

  // get positions in a flat array
  get pos() { return this.#p_pos };
  get last_point() {return this.#p_pos.at(-1)}

  set velocity(vel = [0.0, 0.0]) {
    this.#velocity = vel;
    this.#p_vel = Array.from({ length: this.#p_pos.length }, _ => this.#genPointVelocity)
  };

  set type(type) {this.#curveType = type};

  // add new point
  push(pos) {
    this.#p_pos.push(pos),
    this.#p_vel.push(this.#genPointVelocity)
    return this
  }
  // when animated move points position by elapsed time
  movePoints(elapsed) {
    this.#p_pos = this.#p_pos.map(
      (pos,i) => [
        pos[0]+this.#p_vel[i][0]*elapsed,
        pos[1]+this.#p_vel[i][1]*elapsed
      ]
    )
    this.#p_vel = this.#p_vel.map(
      (vel,i) => { 
        const pos=this.#p_pos[i];
        return [
          Math.abs(pos[0]) < 1.0 ? vel[0] : -1*Math.sign(pos[0])*Math.abs(vel[0]),
          Math.abs(pos[1]) < 1.0 ? vel[1] : -1*Math.sign(pos[1])*Math.abs(vel[1]),
      ] }
    )
    return this;
  };
  // clean curve data
  clear() {
    this.#p_pos=[];
    this.#p_vel=[];
    this.#velocity = null;
    this.#color = null;
    this.#alpha = null;
    this.#pointSize = null;
    this.#curveType = null;
    return this;
  }

  draw(drawingObjects,segmentsPerCurve) {
    if (this.length === 0 || this.length < 4) return;

    gl.uniform1i( uniforms.loc[0], segmentsPerCurve);
    gl.uniform2fv(uniforms.loc[1], flatten(this.#p_pos));
    gl.uniform3fv(uniforms.loc[2], this.#color);
    gl.uniform1f( uniforms.loc[3], this.#alpha);
    gl.uniform1f( uniforms.loc[4], this.#pointSize);
    gl.uniform1i( uniforms.loc[5], this.#curveType);

    // // 0b01: draw points
    // // 0b10: draw lines
    
    const segmentsQuantity = (this.#p_pos.length-3)*segmentsPerCurve+1;
    if (drawingObjects & 0b01) {
      gl.drawArrays(gl.POINTS, 0, segmentsQuantity);
    };
    if (drawingObjects & 0b10) {
      gl.drawArrays(gl.LINE_STRIP, 0, segmentsQuantity);
    };

    return this;
  }
}

let inputCurve = new Curve() // array of positions 2f
let curves     = []; // array of Curves

// Get distance between two positions in 2d
function distance2d(p1, p2){
  return Math.sqrt(
    Math.pow(p1[0]-p2[0],2)
    + Math.pow(p1[1]-p2[1],2)
  )
};

/**
 * Resize event handler
 *
 * @param {*} target - The window that has resized
 */
function resize(target) {
  // Aquire the new window dimensions
  const width = target.innerWidth;
  const height = target.innerHeight;

  // Set canvas size to occupy the entire window
  canvas.width = width;
  canvas.height = height;

  // Set the WebGL viewport to fill the canvas completely
  gl.viewport(0, 0, width, height);
  console.debug("resizing done");
}

function handle_keydown(event) {
  switch (event.key) {
    case "z": // push curve
      if (inputCurve.length >= 4) {
        curves.push(inputCurve);
        // createBezierCurve();
        // reset control points
        inputCurve = new Curve();
      }
      break;
    case "c": // clear curves
      inputCurve = new Curve();
      //
      break;
    case "C": // clear curves
      curves = [];
      //
      break;
    case "=": // increase segments without pressing shift
    case "+": // increase segments
      segmentsPerCurve++;
      //
      break;
    case "-": // decrease segments
      segmentsPerCurve=Math.max(0,segmentsPerCurve-1);
      break;
    case " ": // Toggle movement
      is_moving = !is_moving;
      break;
    case ">": // increase velocity
      animationVelocity = animationVelocity + 1;
      //
      break;
    case "<": // decrease velocity
      animationVelocity = Math.max(1, animationVelocity - 1);
      //
      break;
    case "p": // toggle visibility points
    case "P": // toggle visibility points
      displayPoints = !displayPoints;
      //
      break;
    case "l": // toggle visibility segments
    case "L": // toggle visibility segments
      displayCurves = !displayCurves;
      //
      break;
    case "1": // set curve bspline
    case "2": // set curve catmullrom
    case "3": // set curve bezier
      selectedCurveType = Number(event.key);
      inputCurve.type = selectedCurveType;
      console.debug("selected curve:", selectedCurveType)
      break;
    case "4": // change all current curves
      curves.forEach((c) => (c.type = selectedCurveType));
      break;

    default:
      console.debug("pressed key does nothing:", event.key);
      break;
  }
  return event
}

function setup(shaders) {
  canvas = document.getElementById("gl-canvas");
  gl = setupWebGL(canvas, { alpha: true });

  // Create WebGL programs
  draw_program = buildProgramFromSources(
    gl,
    shaders["shader.vert"],
    shaders["shader.frag"]
  );
  // console.debug(draw_program)
  
  // Enable Alpha blending
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  
  const tArray = Array.from({ length: MAX_SEGMENTS_QTY }, (_, i) => i);
  const buffer_index = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer_index);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Uint32Array(tArray),
    gl.STATIC_DRAW,
  );

  // console.log(
  //   gl.getUniformLocation(draw_program, "u_controlPointsQuantity")
  // )
  
  const loc_index = gl.getAttribLocation(draw_program, "a_index")
  gl.vertexAttribIPointer(loc_index, 1, gl.INT, 0, 0);
  gl.enableVertexAttribArray(loc_index);

  uniforms.keys.forEach(key=>uniforms.loc.push(
    gl.getUniformLocation(draw_program,key)
  ));

  console.debug(uniforms.keys)
  console.debug(uniforms.loc)


  gl.clearColor(0.0, 0.0, 0.0, 1);


  // const u_controlPoints = gl.getUniformLocation(
  //   draw_program,
  //   "u_controlPoints",
  // );
  // const u_sampleSize = gl.getUniformLocation(draw_program, "u_sampleSize");

  // gl.uniform1f(u_sampleSize, 5.0); // Set size of the points

  // Handle resize events
  window.addEventListener("resize", (event) => {
    resize(event.target);
  });

  function get_pos_from_mouse_event(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const x = -1 + (2 * (event.clientX - rect.left)) / canvas.width;
    const y = +1 - (2 * (event.clientY - rect.top)) / canvas.height;

    return vec2(x, y);
  }

  //
  // MOUSE
  //
  // Handle mouse down events
  window.addEventListener("mousedown", (event) => {
    inputCurve.push(get_pos_from_mouse_event(canvas, event));
    console.debug(inputCurve.last_point);
  });
  // Handle mouse move events
  window.addEventListener("mousemove", (event) => {});
  // Handle mouse up events
  window.addEventListener("mouseup", (event) => {});
  //
  // KEYBOARD
  //
  window.addEventListener("keydown", event => handle_keydown(event));
  console.debug("add event listeners done");

  resize(window);
  window.requestAnimationFrame(animate);
  console.debug("setup done");
}

function createBezierCurve() {
  const segments = 30; // number of divisions for t from 0->1
  const random_vel = (v) => ((Math.random() - 0.5) * v) / 50; // random velocity, v is speed in percentage of space
  const curve_velocity = Array.from({ length: 2 }, (_) => random_vel(0.2));

  const points = Array.from({ length: inputCurve.length - 3 }, (_, i) =>
    Array.from({ length: segments }, (_, t) => {
      // division fraction
      const t_ = [ 1,(t+1)/segments ];
      t_.push(t_[1]*t_[1]);
      t_.push(t_[2]*t_[1]);

      const basis = [
        (-t_[3] + 3 * t_[2] - 3 * t_[1] + t_[0]) / 6,
        (3 * t_[3] - 6 * t_[2] + 4) / 6,
        (-3 * t_[3] + 3 * t_[2] + 3 * t_[1] + t_[0]) / 6,
        t_[3] / 6,
      ];
      return {
        pos: inputCurve
          // get points i->i+3
          .slice(i, i + 4)
          // map to values modified by basis
          .map((cp, j) => cp.map((x) => x * basis[j]))
          // reduce into a vec2
          .reduce(
            (v, p) => {
              v[0] += p[0];
              v[1] += p[1];
              return v;
            },
            [0, 0],
          ),
        vel: Array.from(curve_velocity, (v) => v + random_vel(0.1)),
      };
    }),
  ).flat();

  console.debug("bezier points:", points);
  // console.debug("bezier points pos:", points.map(p=>p.pos));

  // Generate points, vel and color for curve
  curves.push({
    points: points,
    // Velocity for reference purposes (used velocity is inside points)
    velocity: curve_velocity,
    // Set random colors for rgb with colors that arent black or white
    color: Array.from({ length: 3 }, (_) => Math.random() * 0.8 + 0.1),
  });
  console.debug("bezierCurve done");
}

let last_time;

function animate(timestamp) {
  window.requestAnimationFrame(animate);

  if (last_time === undefined) {
    last_time = timestamp;
  }
  // Elapsed time (in miliseconds) since last time here
  const elapsed = timestamp - last_time;
  // elapsed with animation velocity modification
  const elapsed_ = elapsed*animationVelocity

  gl.clear(gl.COLOR_BUFFER_BIT);
  
  gl.useProgram(draw_program);

  //update curves
  if (is_moving) {
    curves.forEach(curve=>curve.movePoints(elapsed_))
  }
  // Draw curves
  curves.forEach(curve => curve.draw(displayCurves+displayPoints,segmentsPerCurve))

  // INPUT_POINTS
  inputCurve.draw((displayPoints + displayCurves) ,segmentsPerCurve);

  gl.useProgram(null);
  last_time = timestamp;
}

loadShadersFromURLS(["shader.vert", "shader.frag"]).then((shaders) =>
  setup(shaders),
);
