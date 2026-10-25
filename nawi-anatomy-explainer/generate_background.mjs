import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "/home/zeno/.agents/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "/home/zeno/.agents/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));

// 1920x1080 Full HD Viewport for high-end web background
const WIDTH = 1920;
const HEIGHT = 1080;

// Coordinate System tuned for a wide background perspective
const BENCH = { x: -260, y: -130, w: 520, d: 260, r: 12 };
const BENCH_H = 16;
const FOOT_H = 8;

// NAWI Weighing Unit (Center-Left)
const NAWI_BASE = { x: -220, y: -90, w: 180, d: 180, r: 8 };
const NAWI_BASE_H = 22;

const PLATTER = { x: -210, y: -80, w: 160, d: 160, r: 5 };
const PLATTER_Z = NAWI_BASE_H + 5;
const PLATTER_H = 6;

const CENTER_X = -130;
const CENTER_Y = 0;
const ECC_OFFSET = 45;
const TEST_POSITIONS = [
  { id: "center", name: "Center (0)", x: CENTER_X, y: CENTER_Y },
  { id: "front-left", name: "Front-Left (1)", x: CENTER_X - ECC_OFFSET, y: CENTER_Y - ECC_OFFSET },
  { id: "front-right", name: "Front-Right (2)", x: CENTER_X + ECC_OFFSET, y: CENTER_Y - ECC_OFFSET },
  { id: "rear-right", name: "Rear-Right (3)", x: CENTER_X + ECC_OFFSET, y: CENTER_Y + ECC_OFFSET },
  { id: "rear-left", name: "Rear-Left (4)", x: CENTER_X - ECC_OFFSET, y: CENTER_Y + ECC_OFFSET },
];

// Test Weights
const WEIGHTS = [
  { mass: 500, label: "500g", r: 10, h: 18, restX: -220, restY: 105 },
  { mass: 1000, label: "1kg", r: 13, h: 22, restX: -185, restY: 105 },
  { mass: 2000, label: "2kg", r: 16, h: 28, restX: -145, restY: 105 },
  { mass: 5000, label: "5kg", r: 20, h: 36, restX: -95, restY: 105 },
];

// PrecisionX Terminal (Center-Right)
const TERMINAL = { x: 40, y: -90, w: 180, d: 190, r: 10 };
const TERMINAL_H = 30;
const SCREEN_Z = TERMINAL_H + 2;

const P = k.fitProjection(
  [
    ...k.boxCorners(BENCH, -BENCH_H - FOOT_H, 0),
    [NAWI_BASE.x, NAWI_BASE.y, NAWI_BASE_H + 50],
    [TERMINAL.x + TERMINAL.w, TERMINAL.y + TERMINAL.d, TERMINAL_H + 60],
  ],
  WIDTH,
  HEIGHT,
  { pad: 120, azimuth: 44, elevation: 30 }
);

const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

function renderBench() {
  const out = [];
  out.push(`<path class="iso-halo" d="${k.haloOf(BENCH, -BENCH_H - FOOT_H, BENCH_H, P)}" style="opacity:0.35; filter:blur(10px)"/>`);

  for (const [x, y] of byDepth(k.corners(BENCH, 36))) {
    out.push(S(k.cylinder(x, y, 16, -BENCH_H - FOOT_H, 3.5, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 12, -BENCH_H - FOOT_H + 3.5, FOOT_H - 3.5, P, 28), { tone: "mid" }));
    out.push(L(k.knurl(x, y, 12, -BENCH_H - FOOT_H + 3.5, -BENCH_H, 28, P, 0.4), { tone: "lo" }));
  }

  out.push(S(k.slabOf(BENCH, -BENCH_H, BENCH_H, P, 12, 2.5), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(BENCH, 8), 0, P), { tone: "lo" }));

  const screws = k.corners(BENCH, 18);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 4, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 1.0, tone: "raised" }));

  // Metrology Scale Ruler
  const ruler = { x: BENCH.x + 30, y: BENCH.y + BENCH.d - 16, w: BENCH.w - 60, d: 10, r: 2 };
  out.push(S(k.slabOf(ruler, 0, 1.0, P, 4), { tone: "lo", crease: "none" }));
  const ticks = k.topTicks(ruler.x + 10, ruler.x + ruler.w - 10, 5, 8, ruler.y + 1.2, 1.0, [2.5, 6], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));

  // Spirit Level
  const bx = BENCH.x + 30;
  const by = BENCH.y + 30;
  out.push(S(k.cylinder(bx, by, 11, 0, 4, P, 28), { tone: "lo" }));
  out.push(L(k.ring(bx, by, 9, 4, P, 24), { tone: "hi" }));
  out.push(L(k.ring(bx, by, 3.5, 4, P, 16), { tone: "lit" }));
  out.push(D([at([bx, by, 4])], { size: 1.5, tone: "lit" }));

  return out.join("");
}

function renderNawiStation() {
  const out = [];
  out.push(S(k.slabOf(NAWI_BASE, 0, NAWI_BASE_H, P, 10, 2.2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(NAWI_BASE, 6), NAWI_BASE_H, P), { tone: "lo" }));

  for (const [x, y] of k.corners(NAWI_BASE, 16)) {
    out.push(S(k.cylinder(x, y, 6.5, 0, NAWI_BASE_H - 1, P, 20), { tone: "lo" }));
    out.push(L(k.knurl(x, y, 6.5, 3, NAWI_BASE_H - 4, 20, P, 0.4), { tone: "faint" }));
  }

  // Load Cell Bending Beam
  const beam = { x: CENTER_X - 24, y: CENTER_Y - 10, w: 48, d: 20, r: 2 };
  out.push(S(k.slabOf(beam, NAWI_BASE_H + 2, 7, P, 3), { tone: "hi" }));
  out.push(L(k.planOutline(k.insetPlan(beam, 4), NAWI_BASE_H + 9, P), { tone: "lit" }));

  // Suspension Flexures
  for (const [x, y] of k.corners(PLATTER, 22)) {
    out.push(S(k.cylinder(x, y, 3.8, NAWI_BASE_H, PLATTER_Z - NAWI_BASE_H, P, 18), { tone: "hi", crease: "none" }));
    out.push(L(k.coil(x, y, 5.2, NAWI_BASE_H + 0.5, PLATTER_Z - 0.5, 5.5, 24, P), { tone: "mid" }));
  }

  // Front Local LCD
  const localScreen = { x: NAWI_BASE.x + 30, y: NAWI_BASE.y + NAWI_BASE.d - 1, w: 65, d: 2, r: 1.5 };
  out.push(S(k.slabOf(localScreen, 6, 10, P, 2), { tone: "raised" }));
  out.push(k.faceTextSvg(k.sideMatrix([localScreen.x + 32, localScreen.y + 1], 11, P, "x"), "2000.00 g", { size: 5.5, tone: "lit", anchor: "middle" }));

  // Buttons
  const b1 = [NAWI_BASE.x + 115, NAWI_BASE.y + NAWI_BASE.d + 1];
  const b2 = [NAWI_BASE.x + 140, NAWI_BASE.y + NAWI_BASE.d + 1];
  out.push(S(k.cylinder(b1[0], b1[1], 5, 7, 5, P, 16), { tone: "hi" }));
  out.push(S(k.cylinder(b2[0], b2[1], 5, 7, 5, P, 16), { tone: "mid" }));

  return out.join("");
}

function renderPlatter() {
  const out = [];
  out.push(S(k.slabOf(PLATTER, 0, PLATTER_H, P, 8, 1.5), { tone: "hi", crease: "lo", lit: true }));
  out.push(L(k.planOutline(k.insetPlan(PLATTER, 4), PLATTER_H, P), { tone: "mid" }));

  out.push(L(k.lineOnTop([PLATTER.x + 10, CENTER_Y], [PLATTER.x + PLATTER.w - 10, CENTER_Y], PLATTER_H + 0.1, P), { tone: "faint" }));
  out.push(L(k.lineOnTop([CENTER_X, PLATTER.y + 10], [CENTER_X, PLATTER.y + PLATTER.d - 10], PLATTER_H + 0.1, P), { tone: "faint" }));

  for (const pos of TEST_POSITIONS) {
    out.push(L(k.ring(pos.x, pos.y, 13, PLATTER_H + 0.1, P, 24), { tone: pos.id === "center" ? "lit" : "mid" }));
    out.push(L(k.ring(pos.x, pos.y, 5, PLATTER_H + 0.1, P, 16), { tone: "lo" }));
    out.push(D([at([pos.x, pos.y, PLATTER_H + 0.1])], { size: 1.1, tone: pos.id === "center" ? "lit" : "hi" }));
    out.push(k.faceTextSvg(k.topMatrix([pos.x, pos.y - 8], PLATTER_H + 0.15, P, "x"), pos.id === "center" ? "CTR" : pos.name.split(" ")[1], { size: 3.8, tone: "mid", anchor: "middle" }));
  }

  return out.join("");
}

function renderWeightsRack() {
  const out = [];
  const RACK = { x: -240, y: 92, w: 180, d: 26, r: 4 };
  out.push(S(k.slabOf(RACK, 0, 5, P, 4, 1.0), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(RACK, 3), 5, P), { tone: "lo" }));
  for (const w of WEIGHTS) {
    out.push(L(k.ring(w.restX, w.restY, w.r + 1.5, 5, P, 24), { tone: "lo" }));
  }
  return out.join("");
}

function renderWeightSolid(w) {
  const out = [];
  out.push(S(k.cylinder(0, 0, w.r, 0, w.h, P, 32, 1.0), { tone: "hi", crease: "lo", lit: true }));
  out.push(L(k.knurl(0, 0, w.r, w.h - 4, w.h, 36, P, 0.4), { tone: "mid" }));
  out.push(S(k.cylinder(0, 0, w.r * 0.45, w.h, 5, P, 20), { tone: "mid" }));
  out.push(S(k.cylinder(0, 0, w.r * 0.72, w.h + 5, 6, P, 24, 0.8), { tone: "hi" }));
  out.push(L(k.knurl(0, 0, w.r * 0.72, w.h + 5, w.h + 11, 28, P, 0.4), { tone: "lo" }));
  out.push(D([at([0, 0, w.h + 11])], { size: 1.2, tone: "lit" }));
  out.push(k.faceTextSvg(k.topMatrix([0, w.r * 0.4], w.h, P, "x"), w.label, { size: 3.6, tone: "lo", anchor: "middle" }));
  return out.join("");
}

function renderDataLink() {
  const out = [];
  const db9 = { x: -38, y: -10, w: 8, d: 10, r: 1.5 };
  out.push(S(k.slabOf(db9, 8, 10, P, 2), { tone: "lo" }));
  out.push(D([at([-34, -5, 13])], { size: 1.0, tone: "lit" }));

  const cablePoints = [
    [-34, -5, 8],
    [-10, -5, 1.5],
    [10, -12, 1.5],
    [25, -20, 1.5],
    [40, -20, 15],
  ];
  const cablePath = cablePoints.map((pt, i) => `${i === 0 ? "M" : "L"} ${at(pt)[0]} ${at(pt)[1]}`).join(" ");
  out.push(`<path class="iso-line" data-tone="mid" d="${cablePath}" style="stroke-width:3.2; stroke-linecap:round"/>`);
  out.push(`<path id="bg-data-pulse" class="iso-line" data-tone="lit" d="${cablePath}" style="stroke-width:2.0; stroke-dasharray:8 22; stroke-linecap:round"/>`);
  return out.join("");
}

function renderTerminal() {
  const out = [];
  out.push(S(k.slabOf(TERMINAL, 0, TERMINAL_H, P, 10, 2.2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(TERMINAL, 4), TERMINAL_H, P), { tone: "lo" }));

  const consoleFace = k.insetPlan(TERMINAL, 8);
  out.push(S(k.slabOf(consoleFace, TERMINAL_H, 4, P, 8, 1.0), { tone: "hi", crease: "lo" }));

  const screenArea = { x: TERMINAL.x + 16, y: TERMINAL.y + 16, w: TERMINAL.w - 32, d: 85, r: 4 };
  out.push(S(k.slabOf(screenArea, SCREEN_Z, 1.5, P, 4), { tone: "lo", crease: "none" }));
  out.push(L(k.planOutline(k.insetPlan(screenArea, 3), SCREEN_Z + 1.5, P), { tone: "lit" }));

  const sx = screenArea.x;
  const sy = screenArea.y;
  const sz = SCREEN_Z + 1.6;

  out.push(k.faceTextSvg(k.topMatrix([sx + 10, sy + 14], sz, P, "x"), "🇮🇳 PRECISIONX • OIML R-76 SOVEREIGN GATE", { size: 4.2, tone: "lit" }));
  out.push(k.faceTextSvg(k.topMatrix([sx + 10, sy + 28], sz, P, "x"), "LEGAL METROLOGY DIVISION • CLASS III", { size: 3.4, tone: "mid" }));
  out.push(k.faceTextSvg(k.topMatrix([sx + 10, sy + 48], sz, P, "x"), "NET: 2000.00 g · TARE: 0.00 g", { size: 6.8, tone: "lit" }));
  out.push(k.faceTextSvg(k.topMatrix([sx + 10, sy + 65], sz, P, "x"), "TELEMETRY: ACTIVE STREAM · 100 Hz", { size: 3.8, tone: "mid" }));
  out.push(k.faceTextSvg(k.topMatrix([sx + 10, sy + 78], sz, P, "x"), "OIML R-76 MPE VERIFICATION: PASS", { size: 4.0, tone: "lit" }));

  // LEDs
  const led1 = [TERMINAL.x + 30, TERMINAL.y + TERMINAL.d - 28];
  const led2 = [TERMINAL.x + 56, TERMINAL.y + TERMINAL.d - 28];
  const led3 = [TERMINAL.x + 82, TERMINAL.y + TERMINAL.d - 28];

  out.push(S(k.cylinder(led1[0], led1[1], 4.2, SCREEN_Z, 2.5, P, 16), { tone: "lo" }));
  out.push(S(k.cylinder(led2[0], led2[1], 4.2, SCREEN_Z, 2.5, P, 16), { tone: "lo" }));
  out.push(S(k.cylinder(led3[0], led3[1], 4.2, SCREEN_Z, 2.5, P, 16), { tone: "lo" }));

  out.push(D([at([led1[0], led1[1], SCREEN_Z + 2.5])], { size: 1.6, tone: "lit" }));
  out.push(D([at([led2[0], led2[1], SCREEN_Z + 2.5])], { size: 1.6, tone: "hi" }));
  out.push(D([at([led3[0], led3[1], SCREEN_Z + 2.5])], { size: 1.6, tone: "lit" }));

  return out.join("");
}

const activeWeight = WEIGHTS[2]; // 2kg
const activePos = TEST_POSITIONS[0]; // Center

// Ambient Background Grid & Vignette
const bgSvgContent = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" width="100%" height="100%" class="iso-svg iso" style="background:#030712; display:block;">
  <defs>
    <radialGradient id="nawiGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.12"/>
      <stop offset="60%" stop-color="#020617" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="0.95"/>
    </radialGradient>
    <pattern id="isoBenchGrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M 48 0 L 0 48 M 0 0 L 48 48" fill="none" stroke="rgba(255,255,255,0.02)" stroke-width="1"/>
    </pattern>
  </defs>
  <style>
    ${k.ISO_CSS}
    @keyframes dataPulseAnim {
      from { stroke-dashoffset: 0; }
      to { stroke-dashoffset: -30px; }
    }
    #bg-data-pulse {
      animation: dataPulseAnim 0.75s linear infinite;
    }
  </style>

  <!-- Dark Deep Metrology Canvas Background -->
  <rect width="${WIDTH}" height="${HEIGHT}" fill="#030712"/>
  <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#isoBenchGrid)"/>
  <rect width="${WIDTH}" height="${HEIGHT}" fill="url(#nawiGlow)"/>

  <!-- Subtle Metrological Coordinate Markings -->
  <g opacity="0.18">
    <circle cx="960" cy="540" r="480" fill="none" stroke="#22d3ee" stroke-dasharray="3 9" stroke-width="1.2"/>
    <circle cx="960" cy="540" r="320" fill="none" stroke="#22d3ee" stroke-dasharray="2 6" stroke-width="1"/>
    <line x1="160" y1="540" x2="1760" y2="540" stroke="#22d3ee" stroke-width="0.8" stroke-dasharray="4 8"/>
    <line x1="960" y1="80" x2="960" y2="1000" stroke="#22d3ee" stroke-width="0.8" stroke-dasharray="4 8"/>
  </g>

  <!-- 3D Isometric Metrology Instrument Rig -->
  <g id="iso-rig-group" transform="translate(0, 20)">
    ${renderBench()}
    ${renderNawiStation()}
    <g id="bg-platter" transform="${k.translateAlong(P, [0, 0, PLATTER_Z])}">
      ${renderPlatter()}
    </g>
    ${renderWeightsRack()}
    ${renderDataLink()}
    ${renderTerminal()}
    <g id="bg-weight" transform="${k.translateAlong(P, [activePos.x, activePos.y, PLATTER_Z + PLATTER_H])}">
      ${renderWeightSolid(activeWeight)}
    </g>
  </g>
</svg>
`;

// Save SVG Background
const svgOutPath = "/home/zeno/Desktop/SIH_NAWI_Login_Background.svg";
writeFileSync(svgOutPath, bgSvgContent);
console.log("Wrote SVG background to:", svgOutPath);
