import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "/home/zeno/.agents/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "/home/zeno/.agents/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));

// Dimensions: balanced 820x480 for instrument + laptop side-by-side
const WIDTH = 820;
const HEIGHT = 480;

// Bench Plate (Ground surface for both scale and laptop)
const BENCH = { x: -245, y: -90, w: 490, d: 180, r: 10 };
const BENCH_H = 10;
const FOOT_H = 6;

// Left Side: Mandi Platform Scale
const SCALE_BASE = { x: -225, y: -70, w: 155, d: 140, r: 6 };
const SCALE_BASE_H = 16;

const PLATTER = { x: -230, y: -75, w: 165, d: 150, r: 5 };
const PLATTER_Z = SCALE_BASE_H + 4;
const PLATTER_H = 6;

const GUARD_POST_L = [-225, -70];
const GUARD_POST_R = [-75, -70];
const GUARD_H = 46;

const POLE = [-80, -55];
const POLE_R = 4.2;
const POLE_H = 135;

const HEAD = [-102, -68, 44, 28, 3]; // x, y, w, d, r
const HEAD_PLAN = { x: HEAD[0], y: HEAD[1], w: HEAD[2], d: HEAD[3], r: HEAD[4] };
const HEAD_Z = POLE_H - 8;
const HEAD_H = 26;

const DONGLE_PLAN = { x: HEAD_PLAN.x + 6, y: HEAD_PLAN.y - 20, w: 32, d: 20, r: 2.5 };
const DONGLE_Z = HEAD_Z + 4;
const DONGLE_H = 14;

const LOAD_CELL = { x: -160, y: -12, w: 55, d: 24, r: 2 };
const LOAD_CELL_Z = 4;
const LOAD_CELL_H = 12;

const SACK = { x: -205, y: -50, w: 100, d: 95, r: 20 };
const SACK_Z = PLATTER_Z + PLATTER_H;
const SACK_H = 30;

// Right Side: Modern PrecisionX Laptop
const LAPTOP = { x: 35, y: -40, w: 175, d: 120, r: 5 };
const LAPTOP_H = 5.5;

// Projection setup: captures both the scale on the left and laptop on the right
const P = k.fitProjection(
  [
    ...k.boxCorners(BENCH, -BENCH_H - FOOT_H, 0),
    [POLE[0] + 15, POLE[1] - 30, POLE_H + HEAD_H + 15],
    [-230, -75, PLATTER_Z + PLATTER_H + SACK_H + 10],
    [LAPTOP.x, LAPTOP.y - 30, 115], // Laptop screen top corner
    [LAPTOP.x + LAPTOP.w, LAPTOP.y - 30, 115],
    [LAPTOP.x + LAPTOP.w, LAPTOP.y + LAPTOP.d, 0]
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

  for (const [x, y] of byDepth(k.corners(BENCH, 18))) {
    out.push(S(k.cylinder(x, y, 8, -BENCH_H - FOOT_H, 2, P, 24), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 6, -BENCH_H - FOOT_H + 2, FOOT_H - 2, P, 24), { tone: "mid" }));
    out.push(L(k.knurl(x, y, 6, -BENCH_H - FOOT_H + 2, -BENCH_H, 16, P), { tone: "lo" }));
  }

  out.push(S(k.slabOf(BENCH, -BENCH_H, BENCH_H, P, 6, 1.5), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(BENCH, 6), 0, P), { tone: "lo" }));

  // Ticks along the bench
  const strip = { x: -225, y: BENCH.y + BENCH.d - 14, w: 450, d: 7, r: 1.5 };
  out.push(S(k.slabOf(strip, 0, 0.6, P, 3), { tone: "lo", crease: "none" }));
  const ticks = k.topTicks(strip.x + 6, strip.x + strip.w - 6, 6, 5, strip.y + 0.8, 0.6, [2.5, 4.2], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));

  // Plaque in center
  const plaque = { x: -35, y: BENCH.y + BENCH.d - 18, w: 70, d: 11, r: 1.5 };
  out.push(S(k.slabOf(plaque, 0, 0.8, P, 2), { tone: "hi", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([plaque.x + 4, plaque.y + 7.5], 0.8, P, "x"), "LEGAL METROLOGY · OIML R-76.1", { size: 2.6, tone: "lo" }));

  return out.join("");
}

// 2. Mandi Platform Scale Base
function renderScaleBase() {
  const out = [];
  for (const [x, y] of byDepth(k.corners(SCALE_BASE, 14))) {
    out.push(S(k.cylinder(x, y, 5.5, 0, 3, P, 20), { tone: "lo" }));
  }
  out.push(S(k.slabOf(SCALE_BASE, 3, SCALE_BASE_H - 3, P, 6, 1.5), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(SCALE_BASE, 4), SCALE_BASE_H, P), { tone: "lo" }));

  // 4 Knurled leveling screw feet
  for (const [x, y] of k.corners(SCALE_BASE, 12)) {
    out.push(S(k.cylinder(x, y, 3.8, SCALE_BASE_H, 2.5, P, 18), { tone: "hi" }));
    out.push(L(k.knurl(x, y, 3.8, SCALE_BASE_H, SCALE_BASE_H + 2.5, 12, P), { tone: "lo" }));
  }

  // Circular Spirit Level (Bullseye bubble vial)
  const bubblePos = [-210, 50];
  out.push(S(k.cylinder(bubblePos[0], bubblePos[1], 4.2, SCALE_BASE_H, 1.5, P, 20), { tone: "lo" }));
  out.push(S(k.cylinder(bubblePos[0], bubblePos[1], 3.2, SCALE_BASE_H + 1.5, 0.8, P, 20), { tone: "hi", lit: true }));
  out.push(L(k.ring(bubblePos[0], bubblePos[1], 1.2, SCALE_BASE_H + 2.3, P, 16), { tone: "mid" }));
  out.push(D([at([bubblePos[0] + 0.2, bubblePos[1] - 0.2, SCALE_BASE_H + 2.3])], { size: 0.7, tone: "hi" }));

  return out.join("");
}

// 3. Internal Shear-Beam Load Cell
function renderLoadCell() {
  const out = [];
  out.push(S(k.slabOf(LOAD_CELL, LOAD_CELL_Z, LOAD_CELL_H, P, 2, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(LOAD_CELL, 1.5), LOAD_CELL_Z + LOAD_CELL_H, P), { tone: "lo" }));

  const hole1 = [LOAD_CELL.x + 16, LOAD_CELL.y + LOAD_CELL.d / 2];
  const hole2 = [LOAD_CELL.x + 39, LOAD_CELL.y + LOAD_CELL.d / 2];
  out.push(L(k.ring(hole1[0], hole1[1], 3.2, LOAD_CELL_Z + LOAD_CELL_H, P, 20), { tone: "hi" }));
  out.push(L(k.ring(hole2[0], hole2[1], 3.2, LOAD_CELL_Z + LOAD_CELL_H, P, 20), { tone: "hi" }));

  const gauge1 = { x: LOAD_CELL.x + 12, y: LOAD_CELL.y + 3.5, w: 7, d: 3.5, r: 0.5 };
  const gauge2 = { x: LOAD_CELL.x + 35, y: LOAD_CELL.y + LOAD_CELL.d - 7, w: 7, d: 3.5, r: 0.5 };
  out.push(S(k.slabOf(gauge1, LOAD_CELL_Z + LOAD_CELL_H, 0.4, P, 1), { tone: "lo", crease: "none" }));
  out.push(S(k.slabOf(gauge2, LOAD_CELL_Z + LOAD_CELL_H, 0.4, P, 1), { tone: "lo", crease: "none" }));

  const stopBolt = [LOAD_CELL.x + LOAD_CELL.w + 12, LOAD_CELL.y + LOAD_CELL.d / 2];
  out.push(S(k.cylinder(stopBolt[0], stopBolt[1], 2.8, LOAD_CELL_Z, 14, P, 16), { tone: "mid" }));
  out.push(S(k.cylinder(stopBolt[0], stopBolt[1], 4, LOAD_CELL_Z + 10, 3, P, 16), { tone: "lo" }));

  return `<g class="anatomy-assembly" id="assembly-loadcell">${out.join("")}</g>`;
}

// 4. Weighing Platter & Rear Sack Rest Guard
function renderPlatter() {
  const out = [];
  for (const [x, y] of k.corners(PLATTER, 16)) {
    out.push(S(k.cylinder(x, y, 4, SCALE_BASE_H, 4, P, 18), { tone: "lo" }));
  }

  out.push(S(k.slabOf(PLATTER, PLATTER_Z, PLATTER_H, P, 5, 1.2), { tone: "hi" }));
  out.push(L(k.planOutline(k.insetPlan(PLATTER, 4), PLATTER_Z + PLATTER_H, P), { tone: "lo" }));

  // Non-slip diamond checker tread ticks
  for (let px = PLATTER.x + 14; px <= PLATTER.x + PLATTER.w - 14; px += 22) {
    const ticks = k.topTicks(px, px + 10, 5, 4, PLATTER.y + 14, PLATTER_Z + PLATTER_H, [1.5, 2.5], P);
    out.push(L(ticks.minor, { tone: "lo" }));
  }

  // Rear Guard Rail (The Mandi Kanta Sack Rest)
  const railZ0 = PLATTER_Z + PLATTER_H;
  const railZ1 = railZ0 + GUARD_H;
  out.push(S(k.cylinder(GUARD_POST_L[0], GUARD_POST_L[1], 2.8, railZ0, GUARD_H, P, 16), { tone: "mid" }));
  out.push(S(k.cylinder(GUARD_POST_R[0], GUARD_POST_R[1], 2.8, railZ0, GUARD_H, P, 16), { tone: "mid" }));

  const midCross = { x: GUARD_POST_L[0], y: GUARD_POST_L[1] - 2.2, w: GUARD_POST_R[0] - GUARD_POST_L[0], d: 4.5, r: 1.5 };
  out.push(S(k.slabOf(midCross, railZ0 + 20, 3.5, P, 2, 0.5), { tone: "hi" }));

  const topCross = { x: GUARD_POST_L[0], y: GUARD_POST_L[1] - 2.8, w: GUARD_POST_R[0] - GUARD_POST_L[0], d: 5.5, r: 2 };
  out.push(S(k.slabOf(topCross, railZ1, 4.5, P, 2.5, 0.6), { tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-platter">${out.join("")}</g>`;
}

// 5. Column Post
function renderColumn() {
  const out = [];
  out.push(S(k.cylinder(POLE[0], POLE[1], 6.5, 0, 14, P, 24), { tone: "lo" }));
  out.push(L(k.knurl(POLE[0], POLE[1], 6.5, 4, 12, 16, P), { tone: "mid" }));
  out.push(S(k.cylinder(POLE[0], POLE[1], POLE_R, 14, POLE_H - 14, P, 24), { tone: "hi" }));

  out.push(S(k.cylinder(POLE[0], POLE[1], POLE_R + 1, 60, 3, P, 20), { tone: "lo" }));
  out.push(S(k.cylinder(POLE[0], POLE[1], 6, POLE_H - 12, 10, P, 24), { tone: "mid" }));

  return out.join("");
}

// 6. Digital Indicator Head
function renderIndicatorHead() {
  const out = [];
  out.push(S(k.slabOf(HEAD_PLAN, HEAD_Z, HEAD_H, P, 4, 1.2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(HEAD_PLAN, 2.5), HEAD_Z + HEAD_H, P), { tone: "lo" }));

  const visor = { x: HEAD_PLAN.x - 1.5, y: HEAD_PLAN.y - 1.5, w: HEAD_PLAN.w + 3, d: 5, r: 1.5 };
  out.push(S(k.slabOf(visor, HEAD_Z + HEAD_H - 3, 3.5, P, 2, 0.5), { tone: "lo" }));

  const bezel = { x: HEAD_PLAN.x + 4, y: HEAD_PLAN.y + HEAD_PLAN.d - 3, w: HEAD_PLAN.w - 8, d: 2.5, r: 1.5 };
  out.push(S(k.slabOf(bezel, HEAD_Z + 7, 13, P, 2, 0.4), { tone: "lo", lit: true }));

  // Readout text
  const matWeight = k.topMatrix([HEAD_PLAN.x + 7, HEAD_PLAN.y + HEAD_PLAN.d - 1], HEAD_Z + 15, P, "x");
  out.push(`<g id="indicator-display-text">${k.faceTextSvg(matWeight, "50.00 kg", { size: 3.6, tone: "hi" })}</g>`);

  const matFlags = k.topMatrix([HEAD_PLAN.x + 7, HEAD_PLAN.y + HEAD_PLAN.d - 1], HEAD_Z + 9, P, "x");
  out.push(`<g id="indicator-display-flags">${k.faceTextSvg(matFlags, "[STABLE] e=50g III", { size: 1.9, tone: "mid" })}</g>`);

  // Keypad
  for (let bx = HEAD_PLAN.x + 8; bx <= HEAD_PLAN.x + HEAD_PLAN.w - 10; bx += 7) {
    out.push(S(k.cylinder(bx, HEAD_PLAN.y + HEAD_PLAN.d - 1, 1.6, HEAD_Z + 3, 0.8, P, 14), { tone: "hi" }));
  }

  // Official wire seal
  const sealWire = [
    [HEAD_PLAN.x + HEAD_PLAN.w - 1, HEAD_PLAN.y + HEAD_PLAN.d - 2, HEAD_Z + 10],
    [HEAD_PLAN.x + HEAD_PLAN.w + 3, HEAD_PLAN.y + HEAD_PLAN.d - 2, HEAD_Z - 6]
  ];
  const pts = sealWire.map(at);
  out.push(k.wireSvg(pts[0], pts[1], { tone: "lo", size: 0.6 }));
  out.push(S(k.cylinder(HEAD_PLAN.x + HEAD_PLAN.w + 3, HEAD_PLAN.y + HEAD_PLAN.d - 2, 2.8, HEAD_Z - 10, 3.5, P, 16), { tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-indicator">${out.join("")}</g>`;
}

// 7. PrecisionX Sentinel IoT Dongle (Rear DB9 Intercept)
function renderDongle() {
  const out = [];
  const db9Mate = { x: HEAD_PLAN.x + 10, y: HEAD_PLAN.y - 4, w: 20, d: 4, r: 1 };
  out.push(S(k.slabOf(db9Mate, HEAD_Z + 8, 10, P, 1.5, 0.4), { tone: "lo" }));

  out.push(S(k.slabOf(DONGLE_PLAN, DONGLE_Z, DONGLE_H, P, 3, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(DONGLE_PLAN, 2), DONGLE_Z + DONGLE_H, P), { tone: "lo" }));

  // Tamper tape
  const tape = { x: DONGLE_PLAN.x + 2, y: DONGLE_PLAN.y + 6, w: DONGLE_PLAN.w - 4, d: 4.5, r: 0.5 };
  out.push(S(k.slabOf(tape, DONGLE_Z + DONGLE_H, 0.3, P, 1), { tone: "lo", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([tape.x + 2, tape.y + 3.4], DONGLE_Z + DONGLE_H + 0.3, P, "x"), "SEALED · PRECISIONX", { size: 1.6, tone: "hi" }));

  // LEDs
  out.push(S(k.cylinder(DONGLE_PLAN.x + 6, DONGLE_PLAN.y + 14, 1.4, DONGLE_Z + DONGLE_H, 1, P, 14), { tone: "hi", lit: true }));
  out.push(S(k.cylinder(DONGLE_PLAN.x + 12, DONGLE_PLAN.y + 14, 1.4, DONGLE_Z + DONGLE_H, 1, P, 14), { tone: "hi", lit: true }));

  // Antenna
  out.push(S(k.cylinder(DONGLE_PLAN.x + DONGLE_PLAN.w - 4, DONGLE_PLAN.y + 4, 1.2, DONGLE_Z + DONGLE_H, 15, P, 14), { tone: "lo" }));

  return `<g class="anatomy-assembly" id="assembly-dongle">${out.join("")}</g>`;
}

// 8. 50 kg Burlap Grain Sack
function renderSack() {
  const out = [];
  out.push(S(k.slabOf(SACK, SACK_Z, 22, P, 7, 5), { tone: "mid" }));
  out.push(S(k.slabOf(k.insetPlan(SACK, 10), SACK_Z + 22, 8, P, 5, 4), { tone: "hi" }));

  const neckPos = [SACK.x + SACK.w / 2, SACK.y + SACK.d / 2];
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 7, SACK_Z + 30, 6, P, 20), { tone: "lo" }));
  out.push(S(k.cylinder(neckPos[0], neckPos[1], 10, SACK_Z + 36, 3.5, P, 20), { tone: "mid" }));
  out.push(L(k.ring(neckPos[0], neckPos[1], 7, SACK_Z + 33, P, 20), { tone: "hi" }));

  const sackLabel = { x: SACK.x + 14, y: SACK.y + 20, w: 52, d: 24, r: 2 };
  out.push(S(k.slabOf(sackLabel, SACK_Z + 30, 0.4, P, 1), { tone: "lo", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([sackLabel.x + 4, sackLabel.y + 15], SACK_Z + 30.4, P, "x"), "50 kg WHEAT", { size: 3.4, tone: "hi" }));
  out.push(k.faceTextSvg(k.topMatrix([sackLabel.x + 4, sackLabel.y + 7.5], SACK_Z + 30.4, P, "x"), "APMC · CLASS III", { size: 2.0, tone: "mid" }));

  return `<g class="anatomy-assembly" id="assembly-sack">${out.join("")}</g>`;
}

// 9. Modern Laptop (Running PrecisionX Project Dashboard)
function renderLaptop() {
  const out = [];

  // A. Lower Deck (Base Chassis)
  for (const [x, y] of byDepth(k.corners(LAPTOP, 16))) {
    out.push(S(k.cylinder(x, y, 4, 0, 1.5, P, 18), { tone: "lo" }));
  }
  out.push(S(k.slabOf(LAPTOP, 1.5, LAPTOP_H - 1.5, P, 4, 0.8), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(LAPTOP, 2), LAPTOP_H, P), { tone: "lo" }));

  // USB Port on left side where the cable enters
  const usbPort = { x: LAPTOP.x - 1, y: LAPTOP.y + 30, w: 2, d: 10, r: 0.5 };
  out.push(S(k.slabOf(usbPort, 2, 2.5, P, 1), { tone: "lo", crease: "none" }));

  // Recessed Keyboard Tray
  const kbTray = { x: LAPTOP.x + 14, y: LAPTOP.y + 8, w: LAPTOP.w - 28, d: 52, r: 2.5 };
  out.push(S(k.slabOf(kbTray, LAPTOP_H, 0.8, P, 2), { tone: "lo" }));

  // Key rows (sleek chiclet keyboard)
  for (let row = 0; row < 5; row++) {
    const ry = kbTray.y + 4 + row * 9.5;
    for (let col = 0; col < 12; col++) {
      const cx = kbTray.x + 4 + col * 11.5;
      const keyPlan = { x: cx, y: ry, w: 9.5, d: 7.5, r: 1 };
      out.push(S(k.slabOf(keyPlan, LAPTOP_H + 0.8, 0.8, P, 1, 0.2), { tone: "hi", crease: "none" }));
    }
  }

  // Spacebar
  const spacebar = { x: kbTray.x + 46, y: kbTray.y + 42, w: 48, d: 7.5, r: 1 };
  out.push(S(k.slabOf(spacebar, LAPTOP_H + 0.8, 0.8, P, 1, 0.2), { tone: "hi", crease: "none" }));

  // Trackpad
  const trackpad = { x: LAPTOP.x + LAPTOP.w / 2 - 24, y: LAPTOP.y + 68, w: 48, d: 38, r: 2 };
  out.push(S(k.slabOf(trackpad, LAPTOP_H, 0.3, P, 1.5), { tone: "lo", crease: "none" }));
  out.push(L(k.planOutline(trackpad, LAPTOP_H + 0.3, P), { tone: "mid" }));

  // B. Cylindrical Hinge
  const hinge = [LAPTOP.x + 8, LAPTOP.y - 1];
  out.push(S(k.cylinder(hinge[0], hinge[1], 2.8, LAPTOP_H - 1, LAPTOP.w - 16, P, 20), { tone: "lo" }));

  // C. Display Lid (Tilted back upright screen facing viewer)
  // Let us draw the display upright along X with a subtle backward tilt in Y
  const SCR_W = LAPTOP.w;
  const SCR_H = 105;
  const SCR_Y0 = LAPTOP.y - 2;
  const SCR_Y1 = LAPTOP.y - 24; // 22 units backward tilt
  const SCR_Z0 = LAPTOP_H + 1;
  const SCR_Z1 = SCR_Z0 + SCR_H;

  // Outer Display Housing (Slab with tilt)
  const p0 = at([LAPTOP.x, SCR_Y0, SCR_Z0]);
  const p1 = at([LAPTOP.x + SCR_W, SCR_Y0, SCR_Z0]);
  const p2 = at([LAPTOP.x + SCR_W, SCR_Y1, SCR_Z1]);
  const p3 = at([LAPTOP.x, SCR_Y1, SCR_Z1]);

  const p0_back = at([LAPTOP.x, SCR_Y0 - 3, SCR_Z0]);
  const p1_back = at([LAPTOP.x + SCR_W, SCR_Y0 - 3, SCR_Z0]);
  const p2_back = at([LAPTOP.x + SCR_W, SCR_Y1 - 3, SCR_Z1]);
  const p3_back = at([LAPTOP.x, SCR_Y1 - 3, SCR_Z1]);

  // Back and Top Rim
  out.push(`<path class="iso-shade" data-shade="1" d="${k.pathOf([p3, p2, p2_back, p3_back], true)}"/>`);
  out.push(`<path class="iso-shade" data-shade="0" d="${k.pathOf([p1, p2, p2_back, p1_back], true)}"/>`);
  out.push(`<path class="iso-top" d="${k.pathOf([p0, p1, p2, p3], true)}"/>`);
  out.push(`<path class="iso-line" data-tone="hi" d="${k.pathOf([p0, p1, p2, p3, p0])}"/>`);

  // Screen Glass Inset (The Bezel & Active Display)
  const bz = 6;
  const g0 = at([LAPTOP.x + bz, SCR_Y0 - 0.8, SCR_Z0 + bz]);
  const g1 = at([LAPTOP.x + SCR_W - bz, SCR_Y0 - 0.8, SCR_Z0 + bz]);
  const g2 = at([LAPTOP.x + SCR_W - bz, SCR_Y1 - 0.8, SCR_Z1 - bz]);
  const g3 = at([LAPTOP.x + bz, SCR_Y1 - 0.8, SCR_Z1 - bz]);

  out.push(`<path class="iso-solid" style="fill:var(--anatomy-paper)" d="${k.pathOf([g0, g1, g2, g3], true)}"/>`);
  out.push(`<path class="iso-line" data-tone="lo" d="${k.pathOf([g0, g1, g2, g3, g0])}"/>`);

  // Web camera dot at top bezel
  const camPos = at([LAPTOP.x + SCR_W / 2, (SCR_Y0 + SCR_Y1) / 2 - 10, SCR_Z1 - bz / 2]);
  out.push(D([camPos], { size: 0.6, tone: "hi" }));

  // Inside Screen: PRECISIONX PROJECT DASHBOARD!
  // Header bar
  const h0 = at([LAPTOP.x + bz + 2, SCR_Y1 + 19, SCR_Z1 - bz - 14]);
  const h1 = at([LAPTOP.x + SCR_W - bz - 2, SCR_Y1 + 19, SCR_Z1 - bz - 14]);
  out.push(`<path class="iso-line" data-tone="lo" d="${k.pathOf([h0, h1])}"/>`);

  // Text on Screen
  const tTitle = at([LAPTOP.x + bz + 4, SCR_Y1 + 20, SCR_Z1 - bz - 7]);
  out.push(`<text x="${tTitle[0]}" y="${tTitle[1]}" class="iso-face-text" data-tone="hi" font-size="7.5" font-weight="700">PRECISIONX · OIML R-76 MANDI PORTAL</text>`);

  // Live Big Weight Display on Laptop Screen!
  const tWeight = at([LAPTOP.x + bz + 6, SCR_Y1 + 14, SCR_Z1 - bz - 34]);
  out.push(`<text x="${tWeight[0]}" y="${tWeight[1]}" id="laptop-live-weight" class="iso-face-text" data-tone="hi" font-size="20" font-weight="800">50.000 kg</text>`);

  // Status Badge
  const tBadge = at([LAPTOP.x + bz + 6, SCR_Y1 + 11, SCR_Z1 - bz - 46]);
  out.push(`<text x="${tBadge[0]}" y="${tBadge[1]}" id="laptop-live-status" class="iso-face-text" data-tone="mid" font-size="6.8">[STABLE · CLASS III · e=50g · MPE ±50g]</text>`);

  // Statutory Error Verification Card
  const tError = at([LAPTOP.x + bz + 6, SCR_Y1 + 7, SCR_Z1 - bz - 58]);
  out.push(`<text x="${tError[0]}" y="${tError[1]}" id="laptop-live-mpe" class="iso-face-text" data-tone="hi" font-size="6.5">STATUTORY ERROR: +12.0g [LEGAL PASS]</text>`);

  // ADC Waveform Line (The live strain gauge graph settling)
  const gY = SCR_Z1 - bz - 72;
  const wavePts = [
    [LAPTOP.x + bz + 6, SCR_Y1 + 4, gY],
    [LAPTOP.x + bz + 20, SCR_Y1 + 4, gY + 5],
    [LAPTOP.x + bz + 35, SCR_Y1 + 4, gY - 6],
    [LAPTOP.x + bz + 50, SCR_Y1 + 4, gY + 3],
    [LAPTOP.x + bz + 65, SCR_Y1 + 4, gY - 1],
    [LAPTOP.x + bz + 85, SCR_Y1 + 4, gY],
    [LAPTOP.x + bz + 110, SCR_Y1 + 4, gY]
  ].map(at);
  out.push(`<path class="iso-line" data-tone="hi" d="${k.pathOf(wavePts)}"/>`);

  // Transaction Info & Cryptographic Seal
  const tTx = at([LAPTOP.x + bz + 6, SCR_Y1 + 1, SCR_Z1 - bz - 82]);
  out.push(`<text x="${tTx[0]}" y="${tTx[1]}" class="iso-face-text" data-tone="mid" font-size="5.8">FARMER: RAMESH KUMAR · LOT: #1048 · WHEAT GR-A</text>`);

  const tSig = at([LAPTOP.x + bz + 6, SCR_Y1 - 2, SCR_Z1 - bz - 92]);
  out.push(`<text x="${tSig[0]}" y="${tSig[1]}" id="laptop-live-sig" class="iso-face-text" data-tone="hi" font-size="5.8">Ed25519 SEAL: 7f3b482...9a41 [OFFLINE VERIFIED]</text>`);

  // QR Code Icon Stamp on the Screen
  const qrX = LAPTOP.x + SCR_W - bz - 28;
  const qrZ = SCR_Z1 - bz - 58;
  const qrBox = [
    at([qrX, SCR_Y1 + 10, qrZ]),
    at([qrX + 22, SCR_Y1 + 10, qrZ]),
    at([qrX + 22, SCR_Y1 + 10, qrZ + 22]),
    at([qrX, SCR_Y1 + 10, qrZ + 22])
  ];
  out.push(`<path class="iso-line" data-tone="hi" d="${k.pathOf([...qrBox, qrBox[0]])}"/>`);
  out.push(`<rect x="${qrBox[0][0] + 3}" y="${qrBox[2][1] + 3}" width="4" height="4" fill="var(--anatomy-hi)"/>`);
  out.push(`<rect x="${qrBox[0][0] + 12}" y="${qrBox[2][1] + 3}" width="4" height="4" fill="var(--anatomy-hi)"/>`);
  out.push(`<rect x="${qrBox[0][0] + 3}" y="${qrBox[2][1] + 12}" width="4" height="4" fill="var(--anatomy-hi)"/>`);

  return `<g class="anatomy-assembly" id="assembly-laptop">${out.join("")}</g>`;
}

// 10. The Hardware Connection Cable (Serial RS-232 to Laptop USB)
function renderConnectionCable() {
  const out = [];

  // Cable starts at Dongle DB9 -> travels down the pole -> across the bench -> into Laptop USB
  const cablePath = [
    [DONGLE_PLAN.x + DONGLE_PLAN.w / 2, DONGLE_PLAN.y + DONGLE_PLAN.d, DONGLE_Z + 4],
    [POLE[0] + 14, POLE[1] - 8, DONGLE_Z - 10],
    [POLE[0] + 16, POLE[1] - 8, 30],
    [POLE[0] + 25, POLE[1] + 10, 8],
    [-20, -10, 4],
    [10, 15, 3],
    [LAPTOP.x - 2, LAPTOP.y + 35, 3.5]
  ];
  const pts = cablePath.map(at);

  // Black & white braided wire
  out.push(k.wireSvg(pts[0], pts[pts.length - 1], { via: pts.slice(1, -1), tone: "mid", size: 1.8 }));

  // Animated Data Stream packet flow along the wire
  out.push(`<path class="iso-line" data-tone="hi" data-flow d="${k.wireSvg(pts[0], pts[pts.length - 1], { via: pts.slice(1, -1), tone: "hi", size: 1.2 })}"/>`);

  // Molded USB connector entering laptop
  const usbPlug = { x: LAPTOP.x - 8, y: LAPTOP.y + 31, w: 8, d: 8, r: 1 };
  out.push(S(k.slabOf(usbPlug, 2, 3, P, 1), { tone: "hi", crease: "none" }));
  out.push(D([at([usbPlug.x + 4, usbPlug.y + 4, 5])], { size: 0.45, tone: "lo" }));

  return `<g class="anatomy-assembly" id="assembly-cable">${out.join("")}</g>`;
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
  renderSack(),
  renderLaptop(),
  renderConnectionCable()
];

const svg = `<svg xmlns="http://www.w3.org/2000/svg" class="iso-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" role="img" aria-label="Non-Automatic Weighing Instrument (NAWI) Mandi Platform Scale connected via PrecisionX RS-232 telemetry cable to Laptop running the legal metrology project dashboard.">${svgParts.join("")}</svg>`;

// Interactive Client-Side Script
const liveScript = `
let currentLoad = 50; // kg
let exploded = false;
let tamper = false;

const displayEl = document.getElementById("indicator-display-text");
const readoutEl = document.querySelector("[data-readout]");
const laptopWeight = document.getElementById("laptop-live-weight");
const laptopStatus = document.getElementById("laptop-live-status");
const laptopMpe = document.getElementById("laptop-live-mpe");
const laptopSig = document.getElementById("laptop-live-sig");
const assemblyPlatter = document.getElementById("assembly-platter");
const assemblySack = document.getElementById("assembly-sack");

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

  if (assemblySack) {
    assemblySack.style.display = kg === 0 ? "none" : "";
  }

  // Active button styling
  document.querySelectorAll(".load-btn").forEach(btn => {
    const bkg = parseInt(btn.getAttribute("data-kg"), 10);
    btn.classList.toggle("active", bkg === kg);
  });

  // Platter deflection physics
  if (assemblyPlatter && !exploded) {
    const deflection = (kg / 150.0) * 1.5;
    assemblyPlatter.style.transform = \`translate(0, \${deflection}px)\`;
  }

  // Update Laptop Screen in real time!
  if (laptopWeight) {
    laptopWeight.textContent = item.label;
  }
  if (laptopStatus) {
    if (tamper) {
      laptopStatus.textContent = "[TAMPER DETECTED · ANALOG SKEW > MPE]";
      laptopStatus.setAttribute("data-tone", "lo");
    } else {
      laptopStatus.textContent = \`[STABLE · CLASS III · e=50g · MPE \${item.mpe}]\`;
      laptopStatus.setAttribute("data-tone", "mid");
    }
  }
  if (laptopMpe) {
    if (tamper) {
      laptopMpe.textContent = "STATUTORY ERROR: +340.0g [REJECTED & LOCKED]";
      laptopMpe.style.fill = "var(--anatomy-red)";
    } else {
      laptopMpe.textContent = \`STATUTORY ERROR: +12.0g [LEGAL PASS]\`;
      laptopMpe.style.fill = "var(--anatomy-hi)";
    }
  }
  if (laptopSig) {
    laptopSig.textContent = \`Ed25519 SEAL: \${item.hash} [OFFLINE VERIFIED]\`;
  }

  // Readout Corner Tag
  if (readoutEl) {
    if (tamper) {
      readoutEl.textContent = \`LOAD: \${item.label} · [TAMPER DETECTED: SKEW > MPE] · BLOCKED\`;
      readoutEl.style.color = "var(--anatomy-red)";
    } else {
      readoutEl.textContent = \`LOAD: \${item.label} · MPE \${item.mpe} · \${item.status} · Ed25519 [VALID]\`;
      readoutEl.style.color = "var(--anatomy-text)";
    }
  }

  // Telemetry HUD update
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
  [assemblyPlatter, assemblySack].forEach(el => {
    if (el) {
      el.style.transform = shift;
      el.style.transition = "transform 400ms cubic-bezier(.32,.72,0,1)";
    }
  });
  const expBtn = document.getElementById("btn-explode");
  if (expBtn) expBtn.classList.toggle("active", exploded);
}

function toggleTamper() {
  tamper = !tamper;
  const tBtn = document.getElementById("btn-tamper");
  if (tBtn) tBtn.classList.toggle("active", tamper);
  updateLoad(currentLoad);
}

window.setLoad = updateLoad;
window.toggleExploded = toggleExploded;
window.toggleTamper = toggleTamper;

// Keyboard navigation
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

const body = `
${k.plateHtml({
  fig: "Fig 1 · NAWI OIML R-76 & PrecisionX System",
  title: "Mandi NAWI Scale Connected to Laptop Running PrecisionX Suite",
  hint: "Hover / Arrow Keys: Change Load · Space: Explode View · T: Tamper Test",
  readout: "LOAD: 50.00 kg · MPE ±50.0g · WHEAT SACK · Ed25519 [VALID]",
  keys: [
    { mark: "lit", label: "Mandi Platform Scale (NAWI Class III with 50kg grain sack & load cell)" },
    { mark: "raised", label: "Direct RS-232 to USB Intercept Cable (Live animated data packet flow)" },
    { mark: "dim", label: "Modern Laptop running PrecisionX Metrology Suite (Live 50.00 kg & QR seal)" },
  ],
  caption:
    "End-to-end Non-Automatic Weighing Instrument (NAWI) architecture. The Mandi platform scale's raw RS-232 serial telemetry is captured directly by the PrecisionX Sentinel dongle before operator manual intervention. The encrypted stream travels across the hardware bridge into the laptop, where the PrecisionX Statutory Metrology application runs OIML R-76 Table 6 MPE checks, signs the measurement with an Ed25519 key, and generates an offline verification QR code.",
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="NAWI connected to Laptop: Arrow keys change load, Space explodes load cell, T tests tamper" aria-valuemin="0" aria-valuemax="150" aria-valuenow="50">${svg}</div>`,
})}

<!-- Interactive Controls -->
<div class="nawi-controls">
  <button class="load-btn" data-kg="0" onclick="setLoad(0)">0 kg (Zero Balance)</button>
  <button class="load-btn" data-kg="20" onclick="setLoad(20)">20 kg (M1 Cal Weight)</button>
  <button class="load-btn active" data-kg="50" onclick="setLoad(50)">50 kg (Wheat Sack)</button>
  <button class="load-btn" data-kg="100" onclick="setLoad(100)">100 kg (Double)</button>
  <button class="load-btn" data-kg="150" onclick="setLoad(150)">150 kg (Max Load)</button>
  <button class="load-btn" id="btn-explode" onclick="toggleExploded()">⇪ Exploded View</button>
  <button class="load-btn" id="btn-tamper" onclick="toggleTamper()">⚡ Test Magnet Fraud</button>
</div>

<!-- Telemetry HUD -->
<div class="nawi-hud">
  <div class="hud-item">
    <span class="hud-label">Instrument Weight</span>
    <span class="hud-value" id="hud-gross">50.00 kg</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">OIML Table 6 MPE</span>
    <span class="hud-value" id="hud-mpe">±50.0 g</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">RS-232 Serial Feed</span>
    <span class="hud-value" id="hud-rs232">ST,GS,+0050.00,kg</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">Laptop Proof Hash</span>
    <span class="hud-value" id="hud-hash">7f3b...9a41</span>
  </div>
  <div class="hud-item">
    <span class="hud-label">Legal Metrology</span>
    <span class="hud-value" id="hud-status" style="color:var(--anatomy-green)">STATUTORY PASS</span>
  </div>
</div>
`;

// Write HTML
const fullHtml = k.pageHtml({
  title: "NAWI Scale Connected to Laptop — PrecisionX OIML R-76 Explainer",
  theme: "light",
  body,
  script: kitScript() + liveScript
}).replace("</style>", `${extraStyles}</style>`);

const outHtml1 = "/home/zeno/Desktop/SIH_NAWI_Laptop_Connected.html";
const outHtml2 = "/home/zeno/Desktop/SIH_NAWI_Anatomy_BW.html";

writeFileSync(outHtml1, fullHtml);
writeFileSync(outHtml2, fullHtml);
console.log("Compiled master Connected NAWI & Laptop explainer to:", outHtml1);

// Write standalone SVG
const outSvg1 = "/home/zeno/Desktop/SIH_NAWI_Laptop_Connected.svg";
const outSvg2 = "/home/zeno/Desktop/SIH_NAWI_Anatomy_BW.svg";
writeFileSync(outSvg1, svg);
writeFileSync(outSvg2, svg);
console.log("Saved vector SVG to:", outSvg1);
