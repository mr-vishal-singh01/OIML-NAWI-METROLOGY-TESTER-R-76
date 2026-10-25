import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "/home/zeno/.agents/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "/home/zeno/.agents/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const theme = process.argv.includes("--light") ? "light" : "dark";

const WIDTH = 920;
const HEIGHT = 580;

// Coordinate System & Dimensions
// Metrology Granite Bench Plate
const BENCH = { x: -180, y: -100, w: 360, d: 190, r: 10 };
const BENCH_H = 14;
const FOOT_H = 6;

// NAWI Instrument Chassis (Left side of bench)
const NAWI_BASE = { x: -160, y: -75, w: 140, d: 140, r: 6 };
const NAWI_BASE_H = 18;

// Weighing Platter (Suspended on load cell flexures)
const PLATTER = { x: -152, y: -67, w: 124, d: 124, r: 4 };
const PLATTER_Z = NAWI_BASE_H + 4;
const PLATTER_H = 5;

// Platter Test Quadrants (OIML R-76 Eccentricity Testing Positions)
const CENTER_X = -90;
const CENTER_Y = -5;
const ECC_OFFSET = 36;
const TEST_POSITIONS = [
  { id: "center", name: "Center (0)", x: CENTER_X, y: CENTER_Y },
  { id: "front-left", name: "Front-Left (1)", x: CENTER_X - ECC_OFFSET, y: CENTER_Y - ECC_OFFSET },
  { id: "front-right", name: "Front-Right (2)", x: CENTER_X + ECC_OFFSET, y: CENTER_Y - ECC_OFFSET },
  { id: "rear-right", name: "Rear-Right (3)", x: CENTER_X + ECC_OFFSET, y: CENTER_Y + ECC_OFFSET },
  { id: "rear-left", name: "Rear-Left (4)", x: CENTER_X - ECC_OFFSET, y: CENTER_Y + ECC_OFFSET },
];

// Precision Standard Test Weights Rack & Weights
const RACK = { x: -170, y: 72, w: 140, d: 20, r: 3 };
const WEIGHTS = [
  { mass: 500, label: "500g", r: 8, h: 14, restX: -150, restY: 82, color: "hi" },
  { mass: 1000, label: "1kg", r: 10, h: 18, restX: -125, restY: 82, color: "hi" },
  { mass: 2000, label: "2kg", r: 12, h: 22, restX: -95, restY: 82, color: "hi" },
  { mass: 5000, label: "5kg", r: 15, h: 28, restX: -60, restY: 82, color: "hi" },
];

// Direct Digital Acquisition Link / Armored RS232 Cable
const CABLE_START = [-20, -5, NAWI_BASE_H - 4];
const CABLE_MID1 = [5, -5, 1];
const CABLE_MID2 = [20, -10, 1];
const CABLE_END = [35, -15, 10];

// PrecisionX Sovereign Edge Metrology Computer (Right side of bench)
const TERMINAL = { x: 35, y: -75, w: 135, d: 145, r: 8 };
const TERMINAL_H = 24;
const SCREEN_Z = TERMINAL_H + 2;

// Camera projection setup
const P = k.fitProjection(
  [
    ...k.boxCorners(BENCH, -BENCH_H - FOOT_H, 0),
    [NAWI_BASE.x, NAWI_BASE.y, NAWI_BASE_H + 40],
    [TERMINAL.x + TERMINAL.w, TERMINAL.y + TERMINAL.d, TERMINAL_H + 50],
  ],
  WIDTH,
  HEIGHT,
  { pad: 36, azimuth: 44, elevation: 32 }
);

const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

// 1. Granite Surface Plate & Leveling Base
function renderBench() {
  const out = [];
  // Ambient drop halo
  out.push(`<path class="iso-halo" d="${k.haloOf(BENCH, -BENCH_H - FOOT_H, BENCH_H, P)}" style="opacity:0.45; filter:blur(6px)"/>`);

  // Heavy anti-vibration leveling feet
  for (const [x, y] of byDepth(k.corners(BENCH, 28))) {
    out.push(S(k.cylinder(x, y, 12, -BENCH_H - FOOT_H, 2.5, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 9, -BENCH_H - FOOT_H + 2.5, FOOT_H - 2.5, P, 28), { tone: "mid" }));
    out.push(L(k.knurl(x, y, 9, -BENCH_H - FOOT_H + 2.5, -BENCH_H, 24, P, 0.4), { tone: "lo" }));
  }

  // Polished granite slab
  out.push(S(k.slabOf(BENCH, -BENCH_H, BENCH_H, P, 10, 2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(BENCH, 6), 0, P), { tone: "lo" }));

  // Corner ground screws & brass registration marks
  const screws = k.corners(BENCH, 14);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 3.2, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.8, tone: "raised" }));

  // Front stainless steel metrology ruler bar
  const ruler = { x: BENCH.x + 20, y: BENCH.y + BENCH.d - 12, w: BENCH.w - 40, d: 8, r: 1.5 };
  out.push(S(k.slabOf(ruler, 0, 0.8, P, 4), { tone: "lo", crease: "none" }));
  const ticks = k.topTicks(ruler.x + 8, ruler.x + ruler.w - 8, 4, 6, ruler.y + 1, 0.8, [2, 4.5], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));

  // Metrology Spirit Bubble Level (Precision leveling indicator on bench)
  const bubbleX = BENCH.x + 22;
  const bubbleY = BENCH.y + 22;
  out.push(S(k.cylinder(bubbleX, bubbleY, 8, 0, 3, P, 28), { tone: "lo" }));
  out.push(L(k.ring(bubbleX, bubbleY, 6.5, 3, P, 24), { tone: "hi" }));
  out.push(L(k.ring(bubbleX, bubbleY, 2.5, 3, P, 16), { tone: "lit" }));
  out.push(D([at([bubbleX, bubbleY, 3])], { size: 1.2, tone: "lit" }));

  return out.join("");
}

// 2. NAWI (Non-Automatic Weighing Instrument) Main Station
function renderNawiStation() {
  const out = [];

  // Instrument Main Housing
  out.push(S(k.slabOf(NAWI_BASE, 0, NAWI_BASE_H, P, 8, 1.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(NAWI_BASE, 4), NAWI_BASE_H, P), { tone: "lo" }));

  // 4 Corner Knurled Leveling Screws of the Scale
  for (const [x, y] of k.corners(NAWI_BASE, 12)) {
    out.push(S(k.cylinder(x, y, 5, 0, NAWI_BASE_H - 1, P, 20), { tone: "lo" }));
    out.push(L(k.knurl(x, y, 5, 2, NAWI_BASE_H - 4, 20, P, 0.4), { tone: "faint" }));
  }

  // Load Cell Assembly Bed (Cutaway internal mechanism representation)
  const loadCellBed = { x: CENTER_X - 25, y: CENTER_Y - 20, w: 50, d: 40, r: 2 };
  out.push(S(k.slabOf(loadCellBed, NAWI_BASE_H, 2, P, 4), { tone: "lo" }));
  // Aluminum Strain-Gauge Bending Beam Load Cell
  const beam = { x: CENTER_X - 18, y: CENTER_Y - 8, w: 36, d: 16, r: 1.5 };
  out.push(S(k.slabOf(beam, NAWI_BASE_H + 2, 6, P, 3), { tone: "hi" }));
  // Strain gauge foil rosette representation
  out.push(L(k.planOutline(k.insetPlan(beam, 3), NAWI_BASE_H + 8, P), { tone: "lit" }));
  out.push(L(k.lineOnTop([beam.x + 6, CENTER_Y], [beam.x + beam.w - 6, CENTER_Y], NAWI_BASE_H + 8.1, P), { tone: "lo" }));

  // 4 Vertical Suspension Flexure Columns supporting the platter
  for (const [x, y] of k.corners(PLATTER, 16)) {
    out.push(S(k.cylinder(x, y, 3, NAWI_BASE_H, PLATTER_Z - NAWI_BASE_H, P, 18), { tone: "hi", crease: "none" }));
    // Coil spring around each suspension post
    out.push(L(k.coil(x, y, 4.2, NAWI_BASE_H + 0.5, PLATTER_Z - 0.5, 4.5, 24, P), { tone: "mid" }));
  }

  // Front Control Panel on NAWI chassis (Local Tare / Zero / Calibration seal)
  const nawiFrontPanel = { x: NAWI_BASE.x + 12, y: NAWI_BASE.y + NAWI_BASE.d - 2, w: NAWI_BASE.w - 24, d: 3, r: 1 };
  out.push(S(k.slabOf(nawiFrontPanel, 3, NAWI_BASE_H - 6, P, 2), { tone: "lo" }));

  // Local 7-segment LCD / VFD bezel
  const localScreen = { x: NAWI_BASE.x + 22, y: NAWI_BASE.y + NAWI_BASE.d - 1, w: 50, d: 2, r: 1 };
  out.push(S(k.slabOf(localScreen, 5, 8, P, 2), { tone: "raised" }));
  out.push(k.faceTextSvg(k.sideMatrix([localScreen.x + 25, localScreen.y + 1], 9, P, "x"), "0.00 g", { size: 4.2, tone: "lit", anchor: "middle" }));

  // Local Tare and Zero Push-buttons
  const tareBtn = [NAWI_BASE.x + 85, NAWI_BASE.y + NAWI_BASE.d + 1];
  const zeroBtn = [NAWI_BASE.x + 105, NAWI_BASE.y + NAWI_BASE.d + 1];
  out.push(S(k.cylinder(tareBtn[0], tareBtn[1], 4, 6, 4, P, 16), { tone: "hi" }));
  out.push(S(k.cylinder(zeroBtn[0], zeroBtn[1], 4, 6, 4, P, 16), { tone: "mid" }));
  out.push(D([at([tareBtn[0], tareBtn[1], 10]), at([zeroBtn[0], zeroBtn[1], 10])], { size: 0.6, tone: "lo" }));

  // Government Legal Metrology Physical Tamper Lead Seal
  const leadSeal = [NAWI_BASE.x + NAWI_BASE.w - 10, NAWI_BASE.y + 12];
  out.push(S(k.cylinder(leadSeal[0], leadSeal[1], 5, NAWI_BASE_H, 4, P, 20), { tone: "hi" }));
  out.push(L(k.ring(leadSeal[0], leadSeal[1], 4, NAWI_BASE_H + 4, P, 16), { tone: "lo" }));
  out.push(D([at([leadSeal[0], leadSeal[1], NAWI_BASE_H + 4])], { size: 1.0, tone: "lit" }));

  return out.join("");
}

// 3. Dynamic Weighing Platter with OIML R-76 Marked Quadrants
function renderPlatter() {
  const out = [];

  // Suspended Stainless Steel Platter
  out.push(S(k.slabOf(PLATTER, 0, PLATTER_H, P, 6, 1.2), { tone: "hi", crease: "lo", lit: true }));
  out.push(L(k.planOutline(k.insetPlan(PLATTER, 3), PLATTER_H, P), { tone: "mid" }));

  // OIML R-76 Quadrant Cross-hair Grid
  out.push(L(k.lineOnTop([PLATTER.x + 8, CENTER_Y], [PLATTER.x + PLATTER.w - 8, CENTER_Y], PLATTER_H + 0.1, P), { tone: "faint" }));
  out.push(L(k.lineOnTop([CENTER_X, PLATTER.y + 8], [CENTER_X, PLATTER.y + PLATTER.d - 8], PLATTER_H + 0.1, P), { tone: "faint" }));

  // 5 Eccentricity Test Target Rings on Platter
  for (const pos of TEST_POSITIONS) {
    out.push(L(k.ring(pos.x, pos.y, 10, PLATTER_H + 0.1, P, 24), { tone: pos.id === "center" ? "lit" : "mid" }));
    out.push(L(k.ring(pos.x, pos.y, 4, PLATTER_H + 0.1, P, 16), { tone: "lo" }));
    out.push(D([at([pos.x, pos.y, PLATTER_H + 0.1])], { size: 0.8, tone: pos.id === "center" ? "lit" : "hi" }));
    // Position label stamped on pan
    out.push(k.faceTextSvg(k.topMatrix([pos.x, pos.y - 6], PLATTER_H + 0.15, P, "x"), pos.id === "center" ? "CTR" : pos.name.split(" ")[1], { size: 3.0, tone: "mid", anchor: "middle" }));
  }

  return out.join("");
}

// 4. Test Weights Rack & Individual F1/M1 Precision Calibrated Weights
function renderRackAndWeights() {
  const out = [];

  // Machined brass / wood rack bar on bench
  out.push(S(k.slabOf(RACK, 0, 4, P, 4, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(RACK, 2), 4, P), { tone: "lo" }));

  // Test weights at rest
  for (const w of WEIGHTS) {
    // Recess well
    out.push(L(k.ring(w.restX, w.restY, w.r + 1, 4, P, 24), { tone: "lo" }));
  }

  return out.join("");
}

// Helper to render an individual precision knobbed test weight
function renderWeightSolid(w, isMoved = false) {
  const out = [];
  const wx = 0;
  const wy = 0;
  // Weight main cylindrical body
  out.push(S(k.cylinder(wx, wy, w.r, 0, w.h, P, 32, 0.8), { tone: "hi", crease: "lo", lit: true }));
  // Chamfered shoulder
  out.push(L(k.knurl(wx, wy, w.r, w.h - 3, w.h, 36, P, 0.3), { tone: "mid" }));
  out.push(L(k.sideArc(wx, wy, w.r, w.h - 3, P, 24), { tone: "faint" }));
  // Knob neck
  out.push(S(k.cylinder(wx, wy, w.r * 0.45, w.h, 4, P, 20), { tone: "mid" }));
  // Knurled knob handle
  out.push(S(k.cylinder(wx, wy, w.r * 0.7, w.h + 4, 5, P, 24, 0.6), { tone: "hi" }));
  out.push(L(k.knurl(wx, wy, w.r * 0.7, w.h + 4, w.h + 9, 28, P, 0.4), { tone: "lo" }));
  // Government verification punch dot on top knob
  out.push(D([at([wx, wy, w.h + 9])], { size: 0.9, tone: "lit" }));
  // Stamped Weight Label
  out.push(k.faceTextSvg(k.topMatrix([wx, wy + w.r * 0.4], w.h, P, "x"), w.label, { size: 2.8, tone: "lo", anchor: "middle" }));
  return out.join("");
}

// 5. Direct RS232 / Optical Sensor Interface Cable
function renderDataLink() {
  const out = [];
  // DB9 Industrial Connector on NAWI Port
  const db9 = { x: -22, y: -9, w: 6, d: 8, r: 1 };
  out.push(S(k.slabOf(db9, 6, 8, P, 2), { tone: "lo" }));
  out.push(D([at([-19, -5, 10])], { size: 0.8, tone: "lit" }));

  // Shielded data cable run across the bench surface
  const cablePoints = [
    [-19, -5, 6],
    [-5, -5, 1.2],
    [10, -10, 1.2],
    [22, -15, 1.2],
    [35, -15, 12],
  ];
  const cablePath = cablePoints.map((pt, i) => `${i === 0 ? "M" : "L"} ${at(pt)[0]} ${at(pt)[1]}`).join(" ");
  out.push(`<path class="iso-line" data-tone="mid" d="${cablePath}" style="stroke-width:2.4; stroke-linecap:round"/>`);
  // Glowing data stream packets along cable (animated via CSS & JS)
  out.push(`<path id="data-pulse-wire" class="iso-line" data-tone="lit" d="${cablePath}" style="stroke-width:1.6; stroke-dasharray:6 18; stroke-linecap:round"/>`);

  // DB9 input port on PrecisionX Terminal
  const termPort = { x: 33, y: -19, w: 4, d: 8, r: 1 };
  out.push(S(k.slabOf(termPort, 8, 8, P, 2), { tone: "lo" }));

  return out.join("");
}

// 6. PrecisionX Sovereign Edge Computer & Metrology Terminal
function renderTerminal() {
  const out = [];

  // Heavy aluminum terminal enclosure
  out.push(S(k.slabOf(TERMINAL, 0, TERMINAL_H, P, 8, 1.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(TERMINAL, 3), TERMINAL_H, P), { tone: "lo" }));

  // Tilted Console Top Face
  const consoleFace = k.insetPlan(TERMINAL, 6);
  out.push(S(k.slabOf(consoleFace, TERMINAL_H, 3, P, 6, 0.8), { tone: "hi", crease: "lo" }));

  // Digital High-Contrast OLED / VFD Inspection Matrix Display
  const screenArea = { x: TERMINAL.x + 12, y: TERMINAL.y + 12, w: TERMINAL.w - 24, d: 65, r: 3 };
  out.push(S(k.slabOf(screenArea, SCREEN_Z, 1.2, P, 3), { tone: "lo", crease: "none" }));
  out.push(L(k.planOutline(k.insetPlan(screenArea, 2), SCREEN_Z + 1.2, P), { tone: "lit" }));

  // Screen Headers & Status Badges
  const sx = screenArea.x;
  const sy = screenArea.y;
  const sz = SCREEN_Z + 1.3;

  out.push(k.faceTextSvg(k.topMatrix([sx + 8, sy + 10], sz, P, "x"), "🇮🇳 PRECISIONX • OIML R-76 NAWI ENGINE", { size: 3.2, tone: "lit" }));
  out.push(k.faceTextSvg(k.topMatrix([sx + 8, sy + 20], sz, P, "x"), "CLASS III • MAX 15kg • e = 0.5g", { size: 2.7, tone: "mid" }));

  // Dynamic Live Display Elements (Placeholder for client updates)
  out.push(`<g id="terminal-live-display">
    ${k.faceTextSvg(k.topMatrix([sx + 8, sy + 36], sz, P, "x"), "MASS:  2000.00 g", { size: 5.6, tone: "lit", id: "screen-mass" })}
    ${k.faceTextSvg(k.topMatrix([sx + 8, sy + 48], sz, P, "x"), "TEST:  ECCENTRICITY [POS 0: CTR]", { size: 3.0, tone: "mid", id: "screen-mode" })}
    ${k.faceTextSvg(k.topMatrix([sx + 8, sy + 58], sz, P, "x"), "MPE:   Δ=+0.02g (TOL ±0.50g) PASS", { size: 3.2, tone: "lit", id: "screen-mpe" })}
  </g>`);

  // Sovereign Cryptographic Status Seal & Indicator LEDs
  const led1 = [TERMINAL.x + 22, TERMINAL.y + TERMINAL.d - 22];
  const led2 = [TERMINAL.x + 42, TERMINAL.y + TERMINAL.d - 22];
  const led3 = [TERMINAL.x + 62, TERMINAL.y + TERMINAL.d - 22];

  out.push(S(k.cylinder(led1[0], led1[1], 3.2, SCREEN_Z, 2, P, 16), { tone: "lo" }));
  out.push(S(k.cylinder(led2[0], led2[1], 3.2, SCREEN_Z, 2, P, 16), { tone: "lo" }));
  out.push(S(k.cylinder(led3[0], led3[1], 3.2, SCREEN_Z, 2, P, 16), { tone: "lo" }));

  out.push(D([at([led1[0], led1[1], SCREEN_Z + 2])], { size: 1.2, tone: "lit" }));
  out.push(D([at([led2[0], led2[1], SCREEN_Z + 2])], { size: 1.2, tone: "hi" }));
  out.push(D([at([led3[0], led3[1], SCREEN_Z + 2])], { size: 1.2, tone: "lit" }));

  out.push(k.faceTextSvg(k.topMatrix([led1[0], led1[1] + 6], SCREEN_Z + 2.1, P, "x"), "DIRECT STREAM", { size: 2.2, tone: "mid", anchor: "middle" }));
  out.push(k.faceTextSvg(k.topMatrix([led2[0], led2[1] + 6], SCREEN_Z + 2.1, P, "x"), "R-76 VERIFIED", { size: 2.2, tone: "lit", anchor: "middle" }));
  out.push(k.faceTextSvg(k.topMatrix([led3[0], led3[1] + 6], SCREEN_Z + 2.1, P, "x"), "SHA256 SEAL", { size: 2.2, tone: "mid", anchor: "middle" }));

  // Interactive Touch / Physical Keypad on terminal
  const keys = [
    { label: "TARE", x: TERMINAL.x + 85, y: TERMINAL.y + 85 },
    { label: "ZERO", x: TERMINAL.x + 105, y: TERMINAL.y + 85 },
    { label: "ECC", x: TERMINAL.x + 85, y: TERMINAL.y + 102 },
    { label: "SEAL", x: TERMINAL.x + 105, y: TERMINAL.y + 102 },
  ];
  for (const key of keys) {
    const kPlan = { x: key.x - 7, y: key.y - 6, w: 14, d: 12, r: 1.5 };
    out.push(S(k.slabOf(kPlan, SCREEN_Z, 2.5, P, 2), { tone: "mid" }));
    out.push(k.faceTextSvg(k.topMatrix([key.x, key.y], SCREEN_Z + 2.6, P, "x"), key.label, { size: 2.4, tone: "lo", anchor: "middle" }));
  }

  // Engraved Model Spec Plate
  out.push(k.faceTextSvg(k.topMatrix([TERMINAL.x + TERMINAL.w - 18, TERMINAL.y + 12], SCREEN_Z + 1, P, "x"), "SIH26035", { size: 3.2, tone: "mid", anchor: "end" }));

  return out.join("");
}

// Initial placement of active test weight (2kg placed on Center quadrant)
const initialWeight = WEIGHTS[2];
const initialPos = TEST_POSITIONS[0];

const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label:
    "Anatomy of the SIH26035 Legal Metrology OIML R-76 NAWI Verification Station. Demonstrates direct real-time data streaming from a Non-Automatic Weighing Instrument (NAWI) to the PrecisionX sovereign edge computer, eliminating manual transcription errors, delays, and tampering.",
  body: [
    renderBench(),
    renderNawiStation(),
    `<g id="part-platter" transform="${k.translateAlong(P, [0, 0, PLATTER_Z])}">
      ${renderPlatter()}
    </g>`,
    renderRackAndWeights(),
    renderDataLink(),
    renderTerminal(),
    // Active Test Weight on Platter
    `<g id="active-weight" transform="${k.translateAlong(P, [initialPos.x, initialPos.y, PLATTER_Z + PLATTER_H])}">
      ${renderWeightSolid(initialWeight, true)}
    </g>`,
  ],
});

// Interactive Client-Side Logic & Animation Loop
const liveScript = `
const P = ${JSON.stringify(P)};
const TEST_POSITIONS = ${JSON.stringify(TEST_POSITIONS)};
const WEIGHTS = ${JSON.stringify(WEIGHTS)};
const PLATTER_Z = ${PLATTER_Z};
const PLATTER_H = ${PLATTER_H};

const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const platter = svg.querySelector("#part-platter");
const activeWeight = svg.querySelector("#active-weight");
const pulseWire = svg.querySelector("#data-pulse-wire");
const readout = document.querySelector("[data-readout]");

let currentPosIndex = 0;
let currentWeightIndex = 2; // 2kg
let activeMode = "solution"; // "solution" (PrecisionX Direct Stream) or "problem" (Manual Wait / Paper)
let tareOffset = 0;
let platterDip = 0;
let targetDip = 1.4;
let pulseOffset = 0;
let clock = 0;
let touring = true;
let visible = true;

// Metrological OIML R-76 Constants for Class III NAWI
const CLASS_E = 0.5; // verification scale interval e = 0.5g
const MAX_CAPACITY = 15000;

function calculateMPE(mass) {
  // OIML R-76 Table 6 Maximum Permissible Errors on initial verification
  const mInE = mass / CLASS_E;
  if (mInE <= 500) return 0.5 * CLASS_E;
  if (mInE <= 2000) return 1.0 * CLASS_E;
  return 1.5 * CLASS_E;
}

function getEccentricityError(posIndex, mass) {
  // Physics of load cell off-center corner loading (eccentricity)
  if (posIndex === 0) return 0.02; // Center
  if (posIndex === 1) return -0.06; // Front-Left
  if (posIndex === 2) return +0.08; // Front-Right
  if (posIndex === 3) return -0.04; // Rear-Right
  if (posIndex === 4) return +0.05; // Rear-Left
  return 0.0;
}

function updateScreen(displayedMass, pos, mpeLimit, error) {
  const massElem = document.getElementById("screen-mass");
  const modeElem = document.getElementById("screen-mode");
  const mpeElem = document.getElementById("screen-mpe");

  if (activeMode === "problem") {
    // Problem mode: fluctuating manual reading, high lag, unverified paper flow
    const jitter = (Math.random() - 0.5) * 1.5;
    const noisyMass = Math.max(0, displayedMass + jitter);
    if (massElem) massElem.textContent = "MASS:  " + noisyMass.toFixed(2) + " g [UNSEALED]";
    if (modeElem) modeElem.textContent = "FLOW:  MANUAL LOGBOOK (WAITING...)";
    if (mpeElem) mpeElem.textContent = "ALERT: NO DIGITAL LINK • RISK OF TAMPERING";
    if (readout) readout.textContent = "UNVERIFIED · MANUAL LAG · TAMPER RISK";
  } else {
    // Solution mode: PrecisionX Instant Sovereign Stream & OIML R-76 Auto-Audit
    const isPass = Math.abs(error) <= mpeLimit;
    const sign = error >= 0 ? "+" : "";
    if (massElem) massElem.textContent = "MASS:  " + displayedMass.toFixed(2) + " g";
    if (modeElem) modeElem.textContent = "OIML:  " + pos.name.toUpperCase();
    if (mpeElem) mpeElem.textContent = "MPE:   Δ=" + sign + error.toFixed(2) + "g (TOL ±" + mpeLimit.toFixed(2) + "g) " + (isPass ? "PASS" : "FAIL");
    if (readout) readout.textContent = "Δ = " + sign + error.toFixed(2) + " g · " + (isPass ? "PASS" : "FAIL") + " (MPE: ±" + mpeLimit.toFixed(2) + "g)";
  }
}

function draw() {
  const curPos = TEST_POSITIONS[currentPosIndex];
  const curWeight = WEIGHTS[currentWeightIndex];
  const nominalMass = curWeight.mass;
  const error = getEccentricityError(currentPosIndex, nominalMass);
  const mpeLimit = calculateMPE(nominalMass);
  const netMass = Math.max(0, nominalMass - tareOffset);

  // Animate platter spring depression
  const currentZ = PLATTER_Z - platterDip;
  platter.setAttribute("transform", translateAlong(P, [0, 0, currentZ]));
  activeWeight.setAttribute("transform", translateAlong(P, [curPos.x, curPos.y, currentZ + PLATTER_H]));

  // Animate optical data stream pulses along cable
  if (pulseWire) {
    pulseOffset = (pulseOffset + (activeMode === "solution" ? 1.2 : 0.2)) % 24;
    pulseWire.style.strokeDashoffset = -pulseOffset + "px";
  }

  updateScreen(netMass, curPos, mpeLimit, error);
}

function tick(now) {
  // Smooth spring motion for platter depression under load
  targetDip = (WEIGHTS[currentWeightIndex].mass / 5000) * 2.8;
  platterDip += (targetDip - platterDip) * 0.12;

  // Auto-tour across eccentricity quadrants if user isn't interacting
  if (touring) {
    clock += 0.016;
    if (clock > 3.2) {
      clock = 0;
      currentPosIndex = (currentPosIndex + 1) % TEST_POSITIONS.length;
    }
  }

  draw();
  requestAnimationFrame(tick);
}

requestAnimationFrame(tick);

// Interactive Click Handlers & Test Point Selection
stage.addEventListener("click", (e) => {
  touring = false;
  // Cycle through eccentricity test quadrants on click
  currentPosIndex = (currentPosIndex + 1) % TEST_POSITIONS.length;
});

// Expose controls to global UI buttons
window.setTestQuadrant = (idx) => {
  touring = false;
  currentPosIndex = idx % TEST_POSITIONS.length;
};

window.setTestWeight = (idx) => {
  touring = false;
  currentWeightIndex = idx % WEIGHTS.length;
};

window.triggerTare = () => {
  touring = false;
  tareOffset = tareOffset === 0 ? WEIGHTS[currentWeightIndex].mass : 0;
};

window.toggleMode = (mode) => {
  touring = false;
  activeMode = mode;
  const btnSol = document.getElementById("btn-solution");
  const btnProb = document.getElementById("btn-problem");
  if (mode === "solution") {
    btnSol.classList.add("active");
    btnProb.classList.remove("active");
  } else {
    btnProb.classList.add("active");
    btnSol.classList.remove("active");
  }
};
`;

const body = k.plateHtml({
  fig: "Fig 1",
  title: "PrecisionX NAWI OIML R-76 Testing Bench & Edge Telemetry Terminal",
  hint: "Click stage to cycle 5-point Eccentricity positions",
  readout: "Δ = +0.02 g · PASS (MPE: ±0.50g)",
  keys: [
    { mark: "lit", label: "Direct digital RS-232 telemetry stream (Zero-wait data acquisition)" },
    { mark: "raised", label: "OIML R-76 Class III Weighing Platter with 5 Eccentricity Test Points" },
    { mark: "mid", label: "Calibrated F1/M1 Standard Test Weights (500g, 1kg, 2kg, 5kg)" },
    { mark: "lo", label: "Granite metrology bench with precision vibration isolation & spirit level" },
  ],
  caption:
    "Smart India Hackathon SIH26035 Solution Architecture: Demonstrating how PrecisionX solves the traditional problem of manual data collection from Non-Automatic Weighing Instruments (NAWI). By intercepting raw load-cell metrics directly via shielded serial bus and executing real-time OIML R-76 MPE error calculations, the system eliminates waiting time, manual transcription errors, and legal metrology tampering.",
  body: `
  <div style="margin-bottom: 14px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 6px; border: 1px solid var(--iso-card-border);">
    <div style="display: flex; gap: 8px;">
      <button id="btn-solution" class="iso-btn active" onclick="toggleMode('solution')">⚡ PrecisionX Sovereign Stream (Zero-Wait)</button>
      <button id="btn-problem" class="iso-btn" onclick="toggleMode('problem')">⚠️ Traditional Manual Log (Waiting)</button>
    </div>
    <div style="display: flex; gap: 6px; align-items: center;">
      <span style="font-size: 11px; color: var(--iso-ink-mid); font-weight: 500; margin-right: 2px;">Load:</span>
      <button class="iso-btn" onclick="setTestWeight(0)">500g</button>
      <button class="iso-btn" onclick="setTestWeight(1)">1kg</button>
      <button class="iso-btn" onclick="setTestWeight(2)">2kg</button>
      <button class="iso-btn" onclick="setTestWeight(3)">5kg</button>
      <button class="iso-btn" style="margin-left: 4px;" onclick="triggerTare()">Zero / Tare</button>
    </div>
  </div>
  <div class="iso-stage" tabindex="0" role="region" aria-label="Interactive OIML R-76 NAWI Verification Test Rig">${svg}</div>
  <div style="margin-top: 14px; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
    <div class="iso-card-panel">
      <h4 style="margin: 0 0 6px 0; font-size: 13px; color: var(--iso-ink-lit);">⚠️ The Traditional Problem: Why It Fails</h4>
      <p style="margin: 0; font-size: 12px; line-height: 1.5; color: var(--iso-ink-mid);">
        1. <strong>Manual Waiting & Observation:</strong> Inspectors wait for unstable pan oscillation and manually write weights on paper inspection records.<br>
        2. <strong>Transcription & Human Error:</strong> Manual data transcription leads to misrecorded divisions and arithmetic errors in MPE limits.<br>
        3. <strong>Tampering & Fraud:</strong> Paper sheets lack cryptographic provenance, allowing backdated certificates or unverified scales to pass.
      </p>
    </div>
    <div class="iso-card-panel">
      <h4 style="margin: 0 0 6px 0; font-size: 13px; color: var(--iso-ink-lit);">⚡ PrecisionX Sovereign Solution (SIH26035)</h4>
      <p style="margin: 0; font-size: 12px; line-height: 1.5; color: var(--iso-ink-mid);">
        1. <strong>Direct Digital Intercept:</strong> Intercepts raw serial RS-232 / USB / BLE telemetry directly from the NAWI load cell without waiting.<br>
        2. <strong>Automated OIML R-76 Engine:</strong> Computes Eccentricity, Repeatability, and Tare MPE compliance in sub-milliseconds.<br>
        3. <strong>Cryptographic Sovereign Seal:</strong> Automatically stamps certificates with SHA-256 digital seals and QR verification for Legal Metrology officers.
      </p>
    </div>
  </div>
  `,
});

// Custom CSS additions for interactive buttons and panels
const customStyles = `
<style>
.iso-btn {
  background: var(--iso-slab-mid);
  color: var(--iso-ink-mid);
  border: 1px solid var(--iso-line-lo);
  border-radius: 4px;
  padding: 6px 12px;
  font-family: inherit;
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}
.iso-btn:hover {
  background: var(--iso-slab-hi);
  color: var(--iso-ink-lit);
  border-color: var(--iso-line-hi);
}
.iso-btn.active {
  background: var(--iso-slab-hi);
  color: var(--iso-ink-lit);
  border-color: var(--iso-line-lit);
  box-shadow: 0 0 8px rgba(0, 220, 255, 0.25);
}
.iso-card-panel {
  background: var(--iso-card-bg);
  border: 1px solid var(--iso-card-border);
  border-radius: 6px;
  padding: 12px 14px;
}
</style>
`;

const htmlDark = k.pageHtml({
  title: "SIH26035 NAWI Legal Metrology Explainer",
  theme: "dark",
  body: customStyles + body,
  script: kitScript() + liveScript,
});

const htmlLight = k.pageHtml({
  title: "SIH26035 NAWI Legal Metrology Explainer",
  theme: "light",
  body: customStyles + body,
  script: kitScript() + liveScript,
});

const outPathDark = join(HERE, "nawi-explainer.html");
const outPathLight = join(HERE, "nawi-explainer-light.html");
writeFileSync(outPathDark, htmlDark);
writeFileSync(outPathLight, htmlLight);

// Also write a direct copy to the user's Desktop for instant access!
const desktopPath = "/home/zeno/Desktop/SIH_NAWI_Isometric_Explainer.html";
writeFileSync(desktopPath, htmlDark);

console.log("Successfully generated:");
console.log("- " + outPathDark);
console.log("- " + outPathLight);
console.log("- " + desktopPath);
