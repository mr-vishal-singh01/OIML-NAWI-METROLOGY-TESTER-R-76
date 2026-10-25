import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "/home/zeno/.agents/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "/home/zeno/.agents/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));

// Dimensions matching standard Anatomy figures (compact, crisp lines, perfect 0.6px weight)
const WIDTH = 680;
const HEIGHT = 460;

// Coordinate System
const BENCH = { x: -140, y: -90, w: 280, d: 180, r: 8 };
const BENCH_H = 10;
const FOOT_H = 6;

// Scale Base Frame (Cast Iron)
const SCALE_BASE = { x: -120, y: -70, w: 170, d: 140, r: 6 };
const SCALE_BASE_H = 16;

// Weighing Platter (The Pan)
const PLATTER = { x: -125, y: -75, w: 180, d: 150, r: 5 };
const PLATTER_Z = SCALE_BASE_H + 4;
const PLATTER_H = 6;

// Rear Guard Rail (Mandi kanta sack rest)
const GUARD_POST_L = [-120, -70];
const GUARD_POST_R = [45, -70];
const GUARD_H = 46;

// Column Post (rises from rear bracket of base)
const POLE = [35, -55];
const POLE_R = 4.5;
const POLE_H = 138;

// Digital Indicator Head
const HEAD = { x: 12, y: -68, w: 46, d: 28, r: 3 };
const HEAD_Z = POLE_H - 8;
const HEAD_H = 26;

// PrecisionX IoT Anti-Tamper Sentinel Dongle (attached directly behind indicator)
const DONGLE = { x: 18, y: -92, w: 34, d: 22, r: 2.5 };
const DONGLE_Z = HEAD_Z + 4;
const DONGLE_H = 14;

// Load Cell (Internal Cantilever Beam under platter)
const LOAD_CELL = { x: -55, y: -12, w: 60, d: 24, r: 2 };
const LOAD_CELL_Z = 4;
const LOAD_CELL_H = 12;

// Standard 20kg M1 Brass Test Weight
const WEIGHT_20KG = { x: -65, y: -20, r: 18, h: 22 };

// Standard 50kg Burlap Wheat Sacks
const SACK = { x: -95, y: -50, w: 105, d: 95, r: 22 };
const SACK_Z = PLATTER_Z + PLATTER_H;
const SACK_H = 30;

// Projection setup
const P = k.fitProjection(
  [
    ...k.boxCorners(BENCH, -BENCH_H - FOOT_H, 0),
    [POLE[0] + 25, POLE[1] - 40, POLE_H + HEAD_H + 15],
    [-135, -85, PLATTER_Z + PLATTER_H + SACK_H * 3 + 10],
    [135, 85, 0]
  ],
  WIDTH,
  HEIGHT,
  { pad: 24, azimuth: 42, elevation: 30 }
);

const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

// 1. Surface Bench Plate
function renderBench() {
  const out = [];
  out.push(`<path class="iso-halo" d="${k.haloOf(BENCH, -BENCH_H - FOOT_H, BENCH_H, P)}"/>`);

  for (const [x, y] of byDepth(k.corners(BENCH, 16))) {
    out.push(S(k.cylinder(x, y, 7, -BENCH_H - FOOT_H, 1.8, P, 24), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 5.2, -BENCH_H - FOOT_H + 1.8, FOOT_H - 1.8, P, 24), { tone: "mid" }));
    out.push(L(k.knurl(x, y, 5.2, -BENCH_H - FOOT_H + 1.8, -BENCH_H, 16, P), { tone: "lo" }));
  }

  out.push(S(k.slabOf(BENCH, -BENCH_H, BENCH_H, P, 6, 1.5), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(BENCH, 5), 0, P), { tone: "lo" }));

  const screws = k.corners(BENCH, 10);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 2, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.5 }));

  // Ruler Strip
  const strip = { x: -125, y: BENCH.y + BENCH.d - 14, w: 250, d: 7, r: 1.5 };
  out.push(S(k.slabOf(strip, 0, 0.6, P, 3), { tone: "lo", crease: "none" }));
  const ticks = k.topTicks(strip.x + 4, strip.x + strip.w - 4, 4, 5, strip.y + 0.8, 0.6, [2, 3.6], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));

  // Plaque
  const plaque = { x: -40, y: BENCH.y + BENCH.d - 18, w: 80, d: 11, r: 1.5 };
  out.push(S(k.slabOf(plaque, 0, 0.8, P, 2), { tone: "hi", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([plaque.x + 4, plaque.y + 7.5], 0.8, P, "x"), "INDIA LEGAL METROLOGY · OIML R-76.1", { size: 2.8, tone: "lo" }));

  return out.join("");
}

// 2. Scale Base Frame (Cast Iron Mandi Kanta Base)
function renderScaleBase() {
  const out = [];
  for (const [x, y] of byDepth(k.corners(SCALE_BASE, 14))) {
    out.push(S(k.cylinder(x, y, 6, 0, 3, P, 20), { tone: "lo" }));
  }
  out.push(S(k.slabOf(SCALE_BASE, 3, SCALE_BASE_H - 3, P, 6, 1.5), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(SCALE_BASE, 4), SCALE_BASE_H, P), { tone: "lo" }));

  // 4 Knurled leveling screw feet (standard Mandi kanta requirement)
  for (const [x, y] of k.corners(SCALE_BASE, 12)) {
    out.push(S(k.cylinder(x, y, 4, SCALE_BASE_H, 2.5, P, 18), { tone: "hi" }));
    out.push(L(k.knurl(x, y, 4, SCALE_BASE_H, SCALE_BASE_H + 2.5, 12, P), { tone: "lo" }));
  }

  // Circular Spirit Level (Bullseye bubble vial)
  const bubblePos = [-105, 52];
  out.push(S(k.cylinder(bubblePos[0], bubblePos[1], 4.5, SCALE_BASE_H, 1.5, P, 20), { tone: "lo" }));
  out.push(S(k.cylinder(bubblePos[0], bubblePos[1], 3.5, SCALE_BASE_H + 1.5, 0.8, P, 20), { tone: "hi", lit: true }));
  out.push(L(k.ring(bubblePos[0], bubblePos[1], 1.4, SCALE_BASE_H + 2.3, P, 16), { tone: "mid" }));
  out.push(D([at([bubblePos[0] + 0.2, bubblePos[1] - 0.2, SCALE_BASE_H + 2.3])], { size: 0.8, tone: "hi" }));

  return out.join("");
}

// 3. Internal Shear-Beam Load Cell (The heart of the NAWI scale)
function renderLoadCell() {
  const out = [];
  // Load cell mounting block
  out.push(S(k.slabOf(LOAD_CELL, LOAD_CELL_Z, LOAD_CELL_H, P, 2, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(LOAD_CELL, 1.5), LOAD_CELL_Z + LOAD_CELL_H, P), { tone: "lo" }));

  // Precision flexure circular cutouts (Shear beam double-hole pattern)
  const hole1 = [LOAD_CELL.x + 18, LOAD_CELL.y + LOAD_CELL.d / 2];
  const hole2 = [LOAD_CELL.x + 42, LOAD_CELL.y + LOAD_CELL.d / 2];
  out.push(L(k.ring(hole1[0], hole1[1], 3.5, LOAD_CELL_Z + LOAD_CELL_H, P, 20), { tone: "hi" }));
  out.push(L(k.ring(hole2[0], hole2[1], 3.5, LOAD_CELL_Z + LOAD_CELL_H, P, 20), { tone: "hi" }));

  // Strain Gauge wheatstone bridge foil patches
  const gauge1 = { x: LOAD_CELL.x + 14, y: LOAD_CELL.y + 4, w: 8, d: 4, r: 0.5 };
  const gauge2 = { x: LOAD_CELL.x + 38, y: LOAD_CELL.y + LOAD_CELL.d - 8, w: 8, d: 4, r: 0.5 };
  out.push(S(k.slabOf(gauge1, LOAD_CELL_Z + LOAD_CELL_H, 0.4, P, 1), { tone: "lo", crease: "none" }));
  out.push(S(k.slabOf(gauge2, LOAD_CELL_Z + LOAD_CELL_H, 0.4, P, 1), { tone: "lo", crease: "none" }));

  // Overload mechanical limit stop bolt with hex nut
  const stopBolt = [LOAD_CELL.x + LOAD_CELL.w + 14, LOAD_CELL.y + LOAD_CELL.d / 2];
  out.push(S(k.cylinder(stopBolt[0], stopBolt[1], 3, LOAD_CELL_Z, 14, P, 16), { tone: "mid" }));
  out.push(S(k.cylinder(stopBolt[0], stopBolt[1], 4.2, LOAD_CELL_Z + 10, 3, P, 16), { tone: "lo" }));

  // 4-wire shielded cable from load cell to indicator mast
  const cablePath = [
    [LOAD_CELL.x + LOAD_CELL.w, LOAD_CELL.y + 6, LOAD_CELL_Z + 4],
    [POLE[0] - 8, POLE[1] + 12, LOAD_CELL_Z + 4],
    [POLE[0], POLE[1], 18]
  ];
  const pts = cablePath.map(at);
  out.push(k.wireSvg(pts[0], pts[pts.length - 1], { via: pts.slice(1, -1), tone: "mid", size: 1.4 }));

  return `<g class="anatomy-assembly" id="assembly-loadcell">${out.join("")}</g>`;
}

// 4. Weighing Platter & Rear Sack Rest Guard
function renderPlatter() {
  const out = [];

  // 4 Shock-absorbing rubber suspension dampers under platter
  for (const [x, y] of k.corners(PLATTER, 16)) {
    out.push(S(k.cylinder(x, y, 4.5, SCALE_BASE_H, 4, P, 18), { tone: "lo" }));
    out.push(L(k.ring(x, y, 4.5, SCALE_BASE_H + 2, P, 18), { tone: "mid" }));
  }

  // Stainless Steel Platter Slab
  out.push(S(k.slabOf(PLATTER, PLATTER_Z, PLATTER_H, P, 5, 1.2), { tone: "hi" }));
  out.push(L(k.planOutline(k.insetPlan(PLATTER, 4), PLATTER_Z + PLATTER_H, P), { tone: "lo" }));

  // Anti-slip diamond checker tread ticks
  for (let px = PLATTER.x + 16; px <= PLATTER.x + PLATTER.w - 16; px += 24) {
    const ticks = k.topTicks(px, px + 12, 6, 4, PLATTER.y + 16, PLATTER_Z + PLATTER_H, [1.5, 2.5], P);
    out.push(L(ticks.minor, { tone: "lo" }));
  }

  // Rear Guard Rail (The Mandi Kanta Sack Rest)
  const railZ0 = PLATTER_Z + PLATTER_H;
  const railZ1 = railZ0 + GUARD_H;
  out.push(S(k.cylinder(GUARD_POST_L[0], GUARD_POST_L[1], 3, railZ0, GUARD_H, P, 16), { tone: "mid" }));
  out.push(S(k.cylinder(GUARD_POST_R[0], GUARD_POST_R[1], 3, railZ0, GUARD_H, P, 16), { tone: "mid" }));

  const midCross = { x: GUARD_POST_L[0], y: GUARD_POST_L[1] - 2.5, w: GUARD_POST_R[0] - GUARD_POST_L[0], d: 5, r: 2 };
  out.push(S(k.slabOf(midCross, railZ0 + 20, 4, P, 2, 0.6), { tone: "hi" }));

  const topCross = { x: GUARD_POST_L[0], y: GUARD_POST_L[1] - 3, w: GUARD_POST_R[0] - GUARD_POST_L[0], d: 6, r: 2.5 };
  out.push(S(k.slabOf(topCross, railZ1, 5, P, 3, 0.8), { tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-platter">${out.join("")}</g>`;
}

// 5. Column Post & Bracket
function renderColumn() {
  const out = [];
  // Base clamp collar
  out.push(S(k.cylinder(POLE[0], POLE[1], 7.5, 0, 14, P, 24), { tone: "lo" }));
  out.push(L(k.knurl(POLE[0], POLE[1], 7.5, 4, 12, 16, P), { tone: "mid" }));
  out.push(S(k.cylinder(POLE[0], POLE[1], 5.5, 14, 6, P, 20), { tone: "mid" }));

  // Main vertical tubular mast
  out.push(S(k.cylinder(POLE[0], POLE[1], POLE_R, 20, POLE_H - 20, P, 24), { tone: "hi" }));

  // Intermediate cable clip rings
  for (const z of [50, 95]) {
    out.push(S(k.cylinder(POLE[0], POLE[1], POLE_R + 1, z, 3, P, 20), { tone: "lo" }));
    out.push(D([at([POLE[0] + POLE_R + 1, POLE[1], z + 1.5])], { size: 0.4 }));
  }

  // Upper mounting swivel collar
  out.push(S(k.cylinder(POLE[0], POLE[1], 7, POLE_H - 12, 10, P, 24), { tone: "mid" }));
  out.push(S(k.cylinder(POLE[0] - 8, POLE[1], 3.5, POLE_H - 8, 8, P, 16), { tone: "lo" }));

  return out.join("");
}

// 6. Digital Indicator Head (Class III NAWI Terminal)
function renderIndicatorHead() {
  const out = [];
  // Indicator Housing
  out.push(S(k.slabOf(HEAD, HEAD_Z, HEAD_H, P, 4, 1.2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(HEAD, 2.5), HEAD_Z + HEAD_H, P), { tone: "lo" }));

  // Protective sun-visor brow overhang
  const visor = { x: HEAD.x - 1.5, y: HEAD.y - 1.5, w: HEAD.w + 3, d: 5, r: 1.5 };
  out.push(S(k.slabOf(visor, HEAD_Z + HEAD_H - 3, 3.5, P, 2, 0.5), { tone: "lo" }));

  // Front recessed display window (Bezel)
  const bezel = { x: HEAD.x + 4, y: HEAD.y + HEAD.d - 3, w: HEAD.w - 8, d: 2.5, r: 1.5 };
  out.push(S(k.slabOf(bezel, HEAD_Z + 7, 13, P, 2, 0.4), { tone: "lo", lit: true }));

  // 7-segment dynamic display readout inside bezel
  const matWeight = k.topMatrix([HEAD.x + 7, HEAD.y + HEAD.d - 1], HEAD_Z + 15, P, "x");
  out.push(`<g id="indicator-display-text">${k.faceTextSvg(matWeight, "50.00 kg", { size: 3.8, tone: "hi" })}</g>`);

  const matFlags = k.topMatrix([HEAD.x + 7, HEAD.y + HEAD.d - 1], HEAD_Z + 9, P, "x");
  out.push(`<g id="indicator-display-flags">${k.faceTextSvg(matFlags, "[STABLE] e=50g III", { size: 2.1, tone: "mid" })}</g>`);

  // Front tactile keypad buttons (ZERO, TARE, PRINT)
  for (let bx = HEAD.x + 8; bx <= HEAD.x + HEAD.w - 12; bx += 8) {
    out.push(S(k.cylinder(bx, HEAD.y + HEAD.d - 1, 1.8, HEAD_Z + 3, 0.8, P, 14), { tone: "hi" }));
  }

  // Official Legal Metrology Verification Lead Seal wire
  const sealWire = [
    [HEAD.x + HEAD.w - 1, HEAD.y + HEAD.d - 2, HEAD_Z + 10],
    [HEAD.x + HEAD.w + 3, HEAD.y + HEAD.d - 2, HEAD_Z - 6]
  ];
  const pts = sealWire.map(at);
  out.push(k.wireSvg(pts[0], pts[1], { tone: "lo", size: 0.7 }));
  out.push(S(k.cylinder(HEAD.x + HEAD.w + 3, HEAD.y + HEAD.d - 2, 3, HEAD_Z - 10, 3.5, P, 16), { tone: "hi" }));
  out.push(D([at([HEAD.x + HEAD.w + 3, HEAD.y + HEAD.d - 2, HEAD_Z - 6.5])], { size: 0.5, tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-indicator">${out.join("")}</g>`;
}

// 7. PrecisionX Anti-Tamper Sentinel IoT Dongle (Direct RS-232 Intercept)
function renderDongle() {
  const out = [];
  // DB9 connector housing mate
  const db9Mate = { x: HEAD.x + 12, y: HEAD.y - 4, w: 22, d: 4, r: 1 };
  out.push(S(k.slabOf(db9Mate, HEAD_Z + 8, 10, P, 1.5, 0.4), { tone: "lo" }));
  out.push(D([at([db9Mate.x + 3, db9Mate.y, HEAD_Z + 13]), at([db9Mate.x + db9Mate.w - 3, db9Mate.y, HEAD_Z + 13])], { size: 0.4 }));

  // Main Dongle Enclosure
  out.push(S(k.slabOf(DONGLE, DONGLE_Z, DONGLE_H, P, 3, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(DONGLE, 2), DONGLE_Z + DONGLE_H, P), { tone: "lo" }));

  // Holographic tamper-evident seal tape
  const tape = { x: DONGLE.x + 2, y: DONGLE.y + 7, w: DONGLE.w - 4, d: 5, r: 0.5 };
  out.push(S(k.slabOf(tape, DONGLE_Z + DONGLE_H, 0.3, P, 1), { tone: "lo", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([tape.x + 2, tape.y + 3.8], DONGLE_Z + DONGLE_H + 0.3, P, "x"), "SEALED · PRECISIONX", { size: 1.8, tone: "hi" }));

  // Dual Status LEDs (Heartbeat & RS-232 telemetry activity)
  out.push(S(k.cylinder(DONGLE.x + 7, DONGLE.y + 15, 1.6, DONGLE_Z + DONGLE_H, 1, P, 14), { tone: "hi", lit: true }));
  out.push(S(k.cylinder(DONGLE.x + 14, DONGLE.y + 15, 1.6, DONGLE_Z + DONGLE_H, 1, P, 14), { tone: "hi", lit: true }));

  // LoRa / 4G telemetry micro-stub antenna
  out.push(S(k.cylinder(DONGLE.x + DONGLE.w - 5, DONGLE.y + 5, 1.4, DONGLE_Z + DONGLE_H, 16, P, 14), { tone: "lo" }));
  out.push(D([at([DONGLE.x + DONGLE.w - 5, DONGLE.y + 5, DONGLE_Z + DONGLE_H + 16])], { size: 0.5, tone: "hi" }));

  // Animated Data Stream flow path (RS-232 direct serial proof uplink)
  const streamPath = [
    [DONGLE.x + DONGLE.w / 2, DONGLE.y + DONGLE.d, DONGLE_Z + 4],
    [POLE[0] + 16, POLE[1] - 8, DONGLE_Z - 10],
    [POLE[0] + 18, POLE[1] - 8, 40],
    [BENCH.x + BENCH.w - 20, BENCH.y + 20, 2]
  ];
  const pts = streamPath.map(at);
  out.push(`<path class="iso-line" data-tone="hi" data-flow d="${k.wireSvg(pts[0], pts[pts.length - 1], { via: pts.slice(1, -1), tone: "hi", size: 1.2 })}"/>`);

  return `<g class="anatomy-assembly" id="assembly-dongle">${out.join("")}</g>`;
}

// 8. 50 kg Mandi Wheat Grain Sack 1 (Base sack)
function renderSack1() {
  const out = [];
  out.push(S(k.slabOf(SACK, SACK_Z, 22, P, 7, 5), { tone: "mid" }));
  out.push(S(k.slabOf(k.insetPlan(SACK, 10), SACK_Z + 22, 8, P, 5, 4), { tone: "hi" }));

  // Cinched neck at top
  const neckPos = [SACK.x + SACK.w / 2, SACK.y + SACK.d / 2];
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 7, SACK_Z + 30, 6, P, 20), { tone: "lo" }));
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 10, SACK_Z + 36, 3.5, P, 20), { tone: "mid" }));
  out.push(L(k.ring(neckPos[0], neckPos[1], 7, SACK_Z + 33, P, 20), { tone: "hi" }));

  // Stenciled Mandi burlap label
  const sackLabel = { x: SACK.x + 14, y: SACK.y + 20, w: 55, d: 26, r: 2 };
  out.push(S(k.slabOf(sackLabel, SACK_Z + 30, 0.4, P, 1), { tone: "lo", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([sackLabel.x + 4, sackLabel.y + 16], SACK_Z + 30.4, P, "x"), "50 kg WHEAT", { size: 3.6, tone: "hi" }));
  out.push(k.faceTextSvg(k.topMatrix([sackLabel.x + 4, sackLabel.y + 8], SACK_Z + 30.4, P, "x"), "APMC · CLASS III", { size: 2.1, tone: "mid" }));

  return `<g class="anatomy-assembly" id="assembly-sack-1">${out.join("")}</g>`;
}

// 9. Second 50kg Sack (for 100kg & 150kg loads)
function renderSack2() {
  const out = [];
  const z2 = SACK_Z + 32;
  const sackPlan2 = { x: SACK.x + 4, y: SACK.y + 3, w: SACK.w - 8, d: SACK.d - 6, r: 18 };
  out.push(S(k.slabOf(sackPlan2, z2, 20, P, 6, 4), { tone: "mid" }));
  out.push(S(k.slabOf(k.insetPlan(sackPlan2, 8), z2 + 20, 8, P, 4, 3), { tone: "hi" }));

  const neckPos = [sackPlan2.x + sackPlan2.w / 2, sackPlan2.y + sackPlan2.d / 2];
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 6.5, z2 + 28, 5, P, 18), { tone: "lo" }));
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 9, z2 + 33, 3, P, 18), { tone: "mid" }));
  out.push(L(k.ring(neckPos[0], neckPos[1], 6.5, z2 + 30, P, 18), { tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-sack-2" style="display:none">${out.join("")}</g>`;
}

// 10. Third 50kg Sack (for 150kg max load)
function renderSack3() {
  const out = [];
  const z3 = SACK_Z + 60;
  const sackPlan3 = { x: SACK.x + 8, y: SACK.y + 6, w: SACK.w - 16, d: SACK.d - 12, r: 16 };
  out.push(S(k.slabOf(sackPlan3, z3, 18, P, 5, 4), { tone: "mid" }));
  out.push(S(k.slabOf(k.insetPlan(sackPlan3, 7), z3 + 18, 7, P, 4, 3), { tone: "hi" }));

  const neckPos = [sackPlan3.x + sackPlan3.w / 2, sackPlan3.y + sackPlan3.d / 2];
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 6, z3 + 25, 4.5, P, 16), { tone: "lo" }));
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 8, z3 + 29.5, 2.8, P, 16), { tone: "mid" }));

  return `<g class="anatomy-assembly" id="assembly-sack-3" style="display:none">${out.join("")}</g>`;
}

// 11. Standard 20kg M1 Class Calibration Test Weight (Alternative load)
function renderCalibrationWeight() {
  const out = [];
  const z0 = PLATTER_Z + PLATTER_H;
  // Polished cylindrical brass/cast iron weight
  out.push(S(k.cylinder(WEIGHT_20KG.x, WEIGHT_20KG.y, WEIGHT_20KG.r, z0, WEIGHT_20KG.h, P, 28), { tone: "mid" }));
  out.push(L(k.planOutline(k.cylinder(WEIGHT_20KG.x, WEIGHT_20KG.y, WEIGHT_20KG.r, z0, WEIGHT_20KG.h, P, 28).top, z0 + WEIGHT_20KG.h, P), { tone: "lo" }));

  // Recessed rim
  out.push(S(k.cylinder(WEIGHT_20KG.x, WEIGHT_20KG.y, WEIGHT_20KG.r - 2, z0 + WEIGHT_20KG.h, 1.2, P, 24), { tone: "lo" }));

  // Central lifting knob
  out.push(S(k.cylinder(WEIGHT_20KG.x, WEIGHT_20KG.y, 4, z0 + WEIGHT_20KG.h + 1.2, 5, P, 18), { tone: "lo" }));
  out.push(S(k.cylinder(WEIGHT_20KG.x, WEIGHT_20KG.y, 7, z0 + WEIGHT_20KG.h + 6.2, 4.5, P, 20), { tone: "hi" }));
  out.push(L(k.knurl(WEIGHT_20KG.x, WEIGHT_20KG.y, 7, z0 + WEIGHT_20KG.h + 6.2, z0 + WEIGHT_20KG.h + 10.7, 16, P), { tone: "lo" }));

  // Engraved stamp mark
  const matStamp = k.topMatrix([WEIGHT_20KG.x - 10, WEIGHT_20KG.y + 2], z0 + WEIGHT_20KG.h + 1.3, P, "x");
  out.push(k.faceTextSvg(matStamp, "M1 20kg", { size: 2.8, tone: "lo" }));

  return `<g class="anatomy-assembly" id="assembly-weight" style="display:none">${out.join("")}</g>`;
}

// Assemble Complete SVG
const svgParts = [
  renderBench(),
  renderScaleBase(),
  renderLoadCell(),
  renderPlatter(),
  renderColumn(),
  renderIndicatorHead(),
  renderDongle(),
  renderSack1(),
  renderSack2(),
  renderSack3(),
  renderCalibrationWeight()
];

const svg = `<svg xmlns="http://www.w3.org/2000/svg" class="iso-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" role="img" aria-label="Non-Automatic Weighing Instrument (NAWI) Mandi Platform Scale with direct hardware RS-232 telemetry intercept and PrecisionX zero-trust cryptographic verification.">${svgParts.join("")}</svg>`;

// Interactive Client-Side Script with Live Dynamic HUD & On-Screen Controls
const liveScript = `
let currentLoad = 50; // kg
let exploded = false;
let tamper = false;

const readoutEl = document.querySelector("[data-readout]");
const assemblyPlatter = document.getElementById("assembly-platter");
const assemblySack1 = document.getElementById("assembly-sack-1");
const assemblySack2 = document.getElementById("assembly-sack-2");
const assemblySack3 = document.getElementById("assembly-sack-3");
const assemblyWeight = document.getElementById("assembly-weight");

const hudGross = document.getElementById("hud-gross");
const hudNet = document.getElementById("hud-net");
const hudMpe = document.getElementById("hud-mpe");
const hudRs232 = document.getElementById("hud-rs232");
const hudHash = document.getElementById("hud-hash");
const hudStatus = document.getElementById("hud-status");

const LOADS = [
  { kg: 0, label: "0.00 kg", flag: "[ZERO] e=50g III", mpe: "±25.0g", status: "ZERO BALANCE", rs: "ST,GS,+0000.00,kg", hash: "4a9f...001a" },
  { kg: 20, label: "20.00 kg", flag: "[STABLE] e=50g III", mpe: "±25.0g", status: "M1 CALIBRATION", rs: "ST,GS,+0020.00,kg", hash: "8b12...c49e" },
  { kg: 50, label: "50.00 kg", flag: "[STABLE] e=50g III", mpe: "±50.0g", status: "WHEAT SACK", rs: "ST,GS,+0050.00,kg", hash: "7f3b...9a41" },
  { kg: 100, label: "100.00 kg", flag: "[STABLE] e=50g III", mpe: "±50.0g", status: "DOUBLE SACK", rs: "ST,GS,+0100.00,kg", hash: "d3e1...5f89" },
  { kg: 150, label: "150.00 kg", flag: "[STABLE] e=50g III", mpe: "±75.0g", status: "MAX CAPACITY", rs: "ST,GS,+0150.00,kg", hash: "99aa...22df" }
];

function updateLoad(kg) {
  currentLoad = kg;
  const item = LOADS.find(l => l.kg === kg) || LOADS[2];

  // Visual visibility of loads
  if (assemblySack1 && assemblySack2 && assemblySack3 && assemblyWeight) {
    if (kg === 0) {
      assemblySack1.style.display = "none";
      assemblySack2.style.display = "none";
      assemblySack3.style.display = "none";
      assemblyWeight.style.display = "none";
    } else if (kg === 20) {
      assemblySack1.style.display = "none";
      assemblySack2.style.display = "none";
      assemblySack3.style.display = "none";
      assemblyWeight.style.display = "";
    } else if (kg === 50) {
      assemblySack1.style.display = "";
      assemblySack2.style.display = "none";
      assemblySack3.style.display = "none";
      assemblyWeight.style.display = "none";
    } else if (kg === 100) {
      assemblySack1.style.display = "";
      assemblySack2.style.display = "";
      assemblySack3.style.display = "none";
      assemblyWeight.style.display = "none";
    } else if (kg === 150) {
      assemblySack1.style.display = "";
      assemblySack2.style.display = "";
      assemblySack3.style.display = "";
      assemblyWeight.style.display = "none";
    }
  }

  // Active button styling
  document.querySelectorAll(".load-btn").forEach(btn => {
    const bkg = parseInt(btn.getAttribute("data-kg"), 10);
    if (bkg === kg) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  // Platter deflection physics
  if (assemblyPlatter && !exploded) {
    const deflection = (kg / 150.0) * 1.6;
    assemblyPlatter.style.transform = \`translate(0, \${deflection}px)\`;
  }

  // HUD and Readout Update
  if (readoutEl) {
    if (tamper) {
      readoutEl.textContent = \`LOAD: \${item.label} · [TAMPER DETECTED: SKEW > MPE] · BLOCKED\`;
      readoutEl.style.color = "var(--anatomy-red)";
    } else {
      readoutEl.textContent = \`LOAD: \${item.label} · MPE \${item.mpe} · \${item.status} · Ed25519 [VALID]\`;
      readoutEl.style.color = "var(--anatomy-text)";
    }
  }

  if (hudGross) hudGross.textContent = item.label;
  if (hudNet) hudNet.textContent = item.label;
  if (hudMpe) hudMpe.textContent = item.mpe;
  if (hudRs232) hudRs232.textContent = item.rs;
  if (hudHash) hudHash.textContent = item.hash;
  if (hudStatus) {
    if (tamper) {
      hudStatus.textContent = "TAMPER DETECTED";
      hudStatus.style.color = "var(--anatomy-red)";
    } else {
      hudStatus.textContent = "STATUTORY PASS";
      hudStatus.style.color = "var(--anatomy-green)";
    }
  }
}

function toggleExploded() {
  exploded = !exploded;
  const shift = exploded ? "translate(0, -48px)" : "translate(0, 0)";
  [assemblyPlatter, assemblySack1, assemblySack2, assemblySack3, assemblyWeight].forEach(el => {
    if (el) {
      el.style.transform = shift;
      el.style.transition = "transform 400ms cubic-bezier(.32,.72,0,1)";
    }
  });
  const expBtn = document.getElementById("btn-explode");
  if (expBtn) {
    expBtn.classList.toggle("active", exploded);
  }
}

function toggleTamper() {
  tamper = !tamper;
  const tBtn = document.getElementById("btn-tamper");
  if (tBtn) {
    tBtn.classList.toggle("active", tamper);
  }
  updateLoad(currentLoad);
}

// Global button click binding
window.setLoad = updateLoad;
window.toggleExploded = toggleExploded;
window.toggleTamper = toggleTamper;

// Keyboard shortcuts
window.addEventListener("keydown", (e) => {
  const idx = LOADS.findIndex(l => l.kg === currentLoad);
  if (e.key === "ArrowRight" || e.key === "ArrowUp") {
    e.preventDefault();
    const next = Math.min(LOADS.length - 1, idx + 1);
    updateLoad(LOADS[next].kg);
  } else if (e.key === "ArrowLeft" || e.key === "ArrowDown") {
    e.preventDefault();
    const prev = Math.max(0, idx - 1);
    updateLoad(LOADS[prev].kg);
  } else if (e.key === " ") {
    e.preventDefault();
    toggleExploded();
  } else if (e.key.toLowerCase() === "t" || e.key.toLowerCase() === "m") {
    e.preventDefault();
    toggleTamper();
  }
});

updateLoad(50);
`;

// Additional CSS for Interactive Control Chips and Telemetry HUD
const extraStyles = `
.nawi-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin-top: 18px;
  padding: 10px 14px;
  background: var(--anatomy-card);
  border: 1px solid var(--anatomy-lo);
  border-radius: 4px;
}
.load-btn {
  background: transparent;
  color: var(--anatomy-text);
  border: 1px solid var(--anatomy-lo);
  padding: 5px 12px;
  font-family: var(--anatomy-mono);
  font-size: 11px;
  letter-spacing: .04em;
  border-radius: 3px;
  cursor: pointer;
  transition: all 150ms ease;
}
.load-btn:hover {
  background: var(--anatomy-shade-2);
  border-color: var(--anatomy-hi);
  color: var(--anatomy-strong);
}
.load-btn.active {
  background: var(--anatomy-hi);
  color: var(--anatomy-card);
  border-color: var(--anatomy-hi);
  font-weight: 600;
}
.nawi-hud {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 12px;
  margin-top: 14px;
  padding: 14px 18px;
  background: var(--anatomy-card);
  border: 1px solid var(--anatomy-lo);
  border-radius: 4px;
  font-family: var(--anatomy-mono);
  font-size: 11px;
}
.hud-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.hud-label {
  color: var(--anatomy-muted);
  font-size: 9.5px;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.hud-value {
  color: var(--anatomy-strong);
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}
`;

// Complete Anatomy Plate HTML Body
const body = `
${k.plateHtml({
  fig: "Fig 1 · NAWI OIML R-76",
  title: "Non-Automatic Weighing Instrument (Mandi Platform Scale)",
  hint: "Hover / Arrow Keys: Change Load · Space: Explode View · T: Tamper Test",
  readout: "LOAD: 50.00 kg · MPE ±50.0g · WHEAT SACK · Ed25519 [VALID]",
  keys: [
    { mark: "lit", label: "Floating Platter & Cantilever Shear-Beam Load Cell (Strain Wheatstone Bridge)" },
    { mark: "raised", label: "Class III NAWI Indicator Head (Manual Operator Equilibrium Determination)" },
    { mark: "dim", label: "PrecisionX Sentinel IoT Dongle (Zero-Trust RS-232 Intercept & Ed25519 Seal)" },
  ],
  caption:
    "A Non-Automatic Weighing Instrument (NAWI) requires operator action to deposit or remove loads and verify balance. In APMC mandis, manual recording and analog magnetic spoofing cause severe revenue leakage. PrecisionX eliminates fraud by intercepting raw RS-232 serial telemetry directly from the indicator head, enforcing statutory OIML R-76 Table 6 Maximum Permissible Error (MPE) thresholds, and sealing every transaction with an immutable Ed25519 cryptographic signature and offline QR token.",
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="NAWI Platform Scale: Arrow keys change load, Space explodes internal load cell view, T simulates magnetic tamper" aria-valuemin="0" aria-valuemax="150" aria-valuenow="50">${svg}</div>`,
})}

<!-- Interactive Load Control Chips -->
<div class="nawi-controls">
  <button class="load-btn" data-kg="0" onclick="setLoad(0)">0 kg (Zero Balance)</button>
  <button class="load-btn" data-kg="20" onclick="setLoad(20)">20 kg (M1 Cal Weight)</button>
  <button class="load-btn active" data-kg="50" onclick="setLoad(50)">50 kg (1 Burlap Sack)</button>
  <button class="load-btn" data-kg="100" onclick="setLoad(100)">100 kg (2 Sacks)</button>
  <button class="load-btn" data-kg="150" onclick="setLoad(150)">150 kg (Max 3 Sacks)</button>
  <button class="load-btn" id="btn-explode" onclick="toggleExploded()">⇪ Exploded Anatomy</button>
  <button class="load-btn" id="btn-tamper" onclick="toggleTamper()">⚡ Test Magnet Fraud</button>
</div>

<!-- Real-time Metrology Telemetry HUD -->
<div class="nawi-hud">
  <div class="hud-item">
    <span class="hud-label">Gross / Net Weight</span>
    <span class="hud-value" id="hud-gross">50.00 kg</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">OIML Table 6 MPE</span>
    <span class="hud-value" id="hud-mpe">±50.0 g</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">Raw RS-232 Stream</span>
    <span class="hud-value" id="hud-rs232">ST,GS,+0050.00,kg</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">PrecisionX Ed25519</span>
    <span class="hud-value" id="hud-hash">7f3b...9a41</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">Statutory Status</span>
    <span class="hud-value" id="hud-status" style="color:var(--anatomy-green)">STATUTORY PASS</span>
  </div>
</div>
`;

// Write to Desktop HTML file
const fullHtml = k.pageHtml({
  title: "Non-Automatic Weighing Instrument (NAWI) — PrecisionX Metrology Anatomy",
  theme: "light",
  body,
  script: kitScript() + liveScript
}).replace("</style>", `${extraStyles}</style>`);

const outputPath = "/home/zeno/Desktop/SIH_NAWI_Anatomy_BW.html";
writeFileSync(outputPath, fullHtml);
console.log("Compiled master Anatomy explainer to:", outputPath);

// Also write standalone SVG
writeFileSync("/home/zeno/Desktop/SIH_NAWI_Anatomy_BW.svg", svg);
console.log("Saved vector SVG to: /home/zeno/Desktop/SIH_NAWI_Anatomy_BW.svg");
