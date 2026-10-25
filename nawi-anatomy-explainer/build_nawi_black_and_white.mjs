import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "/home/zeno/.agents/skills/anatomy/kit/iso-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));

// 1920x1080 Full HD Viewport (Also scalable down to any width)
const WIDTH = 1920;
const HEIGHT = 1080;

// Coordinate System tuned for balanced spacing:
// Left: Mandi Platform Scale (NAWI Class III)
// Center: Smart IoT Bridge Hardware Intercept
// Right: PrecisionX Sovereign Verification Console

const BENCH = { x: -390, y: -190, w: 780, d: 380, r: 16 };
const BENCH_H = 14;
const FOOT_H = 8;

// Physical Scale Assembly
const SCALE_BASE = { x: -340, y: -140, w: 230, d: 250, r: 10 };
const SCALE_BASE_H = 22;

const PLATTER = { x: -345, y: -145, w: 240, d: 260, r: 8 };
const PLATTER_Z = SCALE_BASE_H + 6;
const PLATTER_H = 8;

const POLE = [-130, -115];
const POLE_R = 7;
const POLE_H = 280;

const HEAD = { x: -165, y: -130, w: 70, d: 45, r: 6 };
const HEAD_Z = POLE_H - 10;
const HEAD_H = 38;

// Smart IoT Dongle (Direct Hardware Intercept)
const DONGLE = { x: -65, y: -95, w: 50, d: 38, r: 4 };
const DONGLE_H = 16;

// PrecisionX Sovereign Verification Terminal
const TERMINAL = { x: 110, y: -145, w: 240, d: 270, r: 12 };
const TERMINAL_H = 34;

const P = k.fitProjection(
  [
    ...k.boxCorners(BENCH, -BENCH_H - FOOT_H, 0),
    [SCALE_BASE.x, SCALE_BASE.y, PLATTER_Z + PLATTER_H + 80],
    [POLE[0], POLE[1], POLE_H + HEAD_H + 30],
    [TERMINAL.x + TERMINAL.w, TERMINAL.y + TERMINAL.d, TERMINAL_H + 110],
  ],
  WIDTH,
  HEIGHT,
  { pad: 60, azimuth: 42, elevation: 30 }
);

const at = (point) => k.iso(point, P);
const S = (paths, style) => k.solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

// 1. Bench Plate Assembly
function renderBench() {
  const out = [];
  out.push(`<path class="iso-halo" d="${k.haloOf(BENCH, -BENCH_H - FOOT_H, BENCH_H, P)}"/>`);

  for (const [x, y] of byDepth(k.corners(BENCH, 30))) {
    out.push(S(k.cylinder(x, y, 14, -BENCH_H - FOOT_H, 3, P, 32), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 10, -BENCH_H - FOOT_H + 3, FOOT_H - 3, P, 32), { tone: "mid" }));
    out.push(L(k.knurl(x, y, 10, -BENCH_H - FOOT_H + 3, -BENCH_H, 16, P), { tone: "lo" }));
  }

  out.push(S(k.slabOf(BENCH, -BENCH_H, BENCH_H, P, 8, 2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(BENCH, 8), 0, P), { tone: "lo" }));

  const screws = k.corners(BENCH, 16);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 3.2, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.7 }));

  // Precision Ruler Ticks along Bench
  const rulerStrip = { x: -360, y: BENCH.y + BENCH.d - 18, w: 720, d: 8, r: 2 };
  out.push(S(k.slabOf(rulerStrip, 0, 0.8, P, 4), { tone: "lo", crease: "none" }));
  const ticks = k.topTicks(rulerStrip.x + 8, rulerStrip.x + rulerStrip.w - 8, 8, 5, rulerStrip.y + 1, 0.8, [2.5, 4.5], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));

  // Sovereign Identification Engraved Plaque
  const plaque = { x: -65, y: BENCH.y + BENCH.d - 22, w: 130, d: 14, r: 2 };
  out.push(S(k.slabOf(plaque, 0, 1.2, P, 3), { tone: "hi", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([plaque.x + 8, plaque.y + 9], 1.2, P, "x"), "INDIA LEGAL METROLOGY · OIML R-76.1", { size: 3.8, tone: "lo" }));

  return out.join("");
}

// 2. Fixed Scale Base Frame
function renderScaleBase() {
  const out = [];
  for (const [x, y] of byDepth(k.corners(SCALE_BASE, 18))) {
    out.push(S(k.cylinder(x, y, 9, 0, 4, P, 24), { tone: "lo" }));
  }
  out.push(S(k.slabOf(SCALE_BASE, 4, SCALE_BASE_H - 4, P, 6, 1.8), { tone: "lo" }));

  // Pillar Pole
  out.push(S(k.cylinder(POLE[0], POLE[1], 14, 0, 10, P, 28), { tone: "lo" }));
  out.push(S(k.cylinder(POLE[0], POLE[1], POLE_R, 10, POLE_H - 10, P, 32), { tone: "hi" }));
  return out.join("");
}

// 3. Load Cell Assembly
function renderLoadCell() {
  const out = [];
  const cellBlock = { x: -250, y: -30, w: 55, d: 32, r: 3 };
  out.push(S(k.slabOf(cellBlock, 8, 12, P, 4, 1), { tone: "hi" }));
  out.push(S(k.cylinder(-222, -14, 5.5, 8, 12, P, 20), { tone: "lo" }));
  out.push(L(k.ring(-222, -14, 5.5, 20, P, 20), { tone: "lo" }));
  return `<g class="anatomy-assembly" id="assembly-loadcell">${out.join("")}</g>`;
}

// 4. Springs Assembly
function renderSprings() {
  const out = [];
  for (const [x, y] of byDepth(k.corners(SCALE_BASE, 26))) {
    out.push(L(k.coil([x, y, SCALE_BASE_H], [x, y, PLATTER_Z], [x, y], 5.5, 4, "z", P, 18), { tone: "mid" }));
  }
  return `<g class="anatomy-assembly" id="assembly-springs">${out.join("")}</g>`;
}

// 5. Platter Assembly
function renderPlatter() {
  const out = [];
  out.push(S(k.slabOf(PLATTER, PLATTER_Z, PLATTER_H, P, 6, 2), { tone: "hi" }));
  out.push(L(k.planOutline(k.insetPlan(PLATTER, 4), PLATTER_Z + PLATTER_H, P), { tone: "mid" }));

  // Diamond Tread Ticks
  for (let px = PLATTER.x + 18; px < PLATTER.x + PLATTER.w - 18; px += 24) {
    for (let py = PLATTER.y + 18; py < PLATTER.y + PLATTER.d - 18; py += 24) {
      out.push(L(k.lineOnTop([px - 4, py], [px + 4, py], PLATTER_Z + PLATTER_H, P), { tone: "lo" }));
      out.push(L(k.lineOnTop([px, py - 4], [px, py + 4], PLATTER_Z + PLATTER_H, P), { tone: "lo" }));
    }
  }

  // Backrest Rail
  const railZ0 = PLATTER_Z + PLATTER_H;
  const railZ1 = railZ0 + 130;
  const leftPost = [PLATTER.x + 25, PLATTER.y + 25];
  const rightPost = [PLATTER.x + PLATTER.w - 25, PLATTER.y + 25];

  out.push(S(k.cylinder(leftPost[0], leftPost[1], 5, railZ0, 130, P, 24), { tone: "hi" }));
  out.push(S(k.cylinder(rightPost[0], rightPost[1], 5, railZ0, 130, P, 24), { tone: "hi" }));
  const topCross = { x: leftPost[0], y: leftPost[1] - 4, w: rightPost[0] - leftPost[0], d: 8, r: 4 };
  out.push(S(k.slabOf(topCross, railZ1, 8, P, 4, 1), { tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-platter">${out.join("")}</g>`;
}

// 6. 50 kg Grain Sack
function renderSack() {
  const out = [];
  const sackPlan = { x: -295, y: -95, w: 145, d: 155, r: 35 };
  const sackZ = PLATTER_Z + PLATTER_H;
  out.push(S(k.slabOf(sackPlan, sackZ, 45, P, 10, 8), { tone: "mid" }));
  out.push(S(k.slabOf(k.insetPlan(sackPlan, 18), sackZ + 45, 18, P, 8, 6), { tone: "hi" }));
  out.push(S(k.cylinder(-222, -17, 14, sackZ + 63, 10, P, 24), { tone: "lo" }));
  out.push(S(k.cylinder(-222, -17, 18, sackZ + 73, 6, P, 24), { tone: "mid" }));

  const sackLabel = { x: -265, y: -38, w: 85, d: 42, r: 3 };
  out.push(S(k.slabOf(sackLabel, sackZ + 63, 0.6, P, 2), { tone: "lo", crease: "none" }));
  out.push(k.faceTextSvg(k.topMatrix([sackLabel.x + 6, sackLabel.y + 25], sackZ + 63.6, P, "x"), "50 kg WHEAT", { size: 5.5, tone: "hi" }));
  out.push(k.faceTextSvg(k.topMatrix([sackLabel.x + 6, sackLabel.y + 12], sackZ + 63.6, P, "x"), "APMC MANDI · CLASS III", { size: 3.2, tone: "mid" }));

  return `<g class="anatomy-assembly" id="assembly-sack">${out.join("")}</g>`;
}

// 7. Digital Indicator Head
function renderIndicatorHead() {
  const out = [];
  out.push(S(k.slabOf(HEAD, HEAD_Z, HEAD_H, P, 6, 2), { tone: "mid" }));
  const visor = { x: HEAD.x - 2, y: HEAD.y - 2, w: HEAD.w + 4, d: 8, r: 2 };
  out.push(S(k.slabOf(visor, HEAD_Z + HEAD_H - 4, 5, P, 2), { tone: "lo" }));

  // Front Recessed 7-Segment Display
  const windowFront = { x: HEAD.x + 6, y: HEAD.y + HEAD.d - 4, w: HEAD.w - 12, d: 3, r: 2 };
  out.push(S(k.slabOf(windowFront, HEAD_Z + 12, 18, P, 2), { tone: "lo", lit: true }));

  // Official Seal
  const sealWire = [[HEAD.x + HEAD.w - 2, HEAD.y + HEAD.d, HEAD_Z + 14], [HEAD.x + HEAD.w - 2, HEAD.y + HEAD.d, HEAD_Z - 12]];
  const pts = sealWire.map(at);
  out.push(k.wireSvg(pts[0], pts[1], { tone: "lo", size: 0.9 }));
  out.push(S(k.cylinder(HEAD.x + HEAD.w - 2, HEAD.y + HEAD.d, 4.5, HEAD_Z - 18, 5, P, 18), { tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-indicator">${out.join("")}</g>`;
}

// 8. Smart IoT Dongle (Direct Hardware Intercept)
function renderDongle() {
  const out = [];
  out.push(S(k.slabOf(DONGLE, 0, DONGLE_H, P, 4, 1.2), { tone: "mid" }));
  out.push(L(k.planOutline(k.insetPlan(DONGLE, 3), DONGLE_H, P), { tone: "lo" }));

  out.push(S(k.cylinder(DONGLE.x + 12, DONGLE.y + 12, 2.5, DONGLE_H, 1.5, P, 16), { tone: "hi", lit: true }));
  out.push(S(k.cylinder(DONGLE.x + 22, DONGLE.y + 12, 2.5, DONGLE_H, 1.5, P, 16), { tone: "hi", lit: true }));

  out.push(k.faceTextSvg(k.topMatrix([DONGLE.x + 8, DONGLE.y + 24], DONGLE_H, P, "x"), "PX-IOT BRIDGE", { size: 2.8, tone: "lo" }));

  const cablePath = [
    [HEAD.x + HEAD.w / 2, HEAD.y, HEAD_Z + 10],
    [POLE[0], POLE[1] + 12, HEAD_Z - 10],
    [POLE[0], POLE[1] + 12, 20],
    [DONGLE.x + DONGLE.w / 2, DONGLE.y, 8],
    [DONGLE.x + DONGLE.w, DONGLE.y + DONGLE.d / 2, 8],
    [TERMINAL.x, TERMINAL.y + 40, 12]
  ];
  const pts = cablePath.map(at);
  out.push(`<g class="iso-wire-harness">${k.wireSvg(pts[0], pts[pts.length - 1], { via: pts.slice(1, -1), tone: "mid", size: 2.2 })}</g>`);

  return `<g class="anatomy-assembly" id="assembly-dongle">${out.join("")}</g>`;
}

// 9. PrecisionX Sovereign Terminal Console
function renderTerminal() {
  const out = [];
  for (const [x, y] of byDepth(k.corners(TERMINAL, 24))) {
    out.push(S(k.cylinder(x, y, 10, 0, 5, P, 24), { tone: "lo" }));
  }
  out.push(S(k.slabOf(TERMINAL, 5, TERMINAL_H - 5, P, 8, 2), { tone: "mid" }));

  const deck = k.insetPlan(TERMINAL, 10);
  out.push(S(k.slabOf(deck, TERMINAL_H, 12, P, 6, 1.5), { tone: "hi" }));

  const screen = k.insetPlan(deck, 8);
  out.push(S(k.slabOf(screen, TERMINAL_H + 12, 1.2, P, 4), { tone: "lo", lit: true }));

  const mat = k.topMatrix([screen.x + 10, screen.y + screen.d - 15], TERMINAL_H + 13.2, P, "x");
  out.push(k.faceTextSvg(mat, "OIML R-76 STATUTORY ENGINE", { size: 5.5, tone: "hi" }));
  
  const mat2 = k.topMatrix([screen.x + 10, screen.y + screen.d - 30], TERMINAL_H + 13.2, P, "x");
  out.push(k.faceTextSvg(mat2, "NET: 50.000 kg · TABLE 6 MPE: ±50.0 g", { size: 4.2, tone: "mid" }));

  const mat3 = k.topMatrix([screen.x + 10, screen.y + screen.d - 45], TERMINAL_H + 13.2, P, "x");
  out.push(k.faceTextSvg(mat3, "ERROR: +12.0 g [LEGAL COMPLIANT PASS]", { size: 4.2, tone: "hi" }));

  const slot = { x: TERMINAL.x + TERMINAL.w - 45, y: TERMINAL.y + 25, w: 35, d: 6, r: 1 };
  out.push(S(k.slabOf(slot, TERMINAL_H + 12, 0.8, P, 2), { tone: "lo", crease: "none" }));
  const paper = { x: slot.x + 2, y: slot.y - 15, w: 31, d: 20, r: 1 };
  out.push(S(k.slabOf(paper, TERMINAL_H + 12.8, 0.4, P, 1), { tone: "hi", crease: "none" }));

  const sealPlaque = { x: TERMINAL.x + 30, y: TERMINAL.y + TERMINAL.d - 4, w: 70, d: 3, r: 2 };
  out.push(S(k.slabOf(sealPlaque, 10, 18, P, 2), { tone: "hi" }));

  return `<g class="anatomy-assembly" id="assembly-terminal">${out.join("")}</g>`;
}

const allGeometry = [
  renderBench(),
  renderScaleBase(),
  renderLoadCell(),
  renderSprings(),
  renderPlatter(),
  renderSack(),
  renderIndicatorHead(),
  renderDongle(),
  renderTerminal()
].join("\n");

// Complete Signature Anatomy Black & White / Light-Theme Application
const bwPage = `<!DOCTYPE html>
<html lang="en" class="iso" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PrecisionX (SIH26035) — Black & White Anatomy Sovereign Explainer</title>
  <style>
    ${k.ISO_CSS}

    /* Strict Signature Anatomy Black & White Palette */
    .iso[data-theme="light"] {
      --anatomy-page: #fbfbfa;
      --anatomy-card: #ffffff;
      --anatomy-text: #37373a;
      --anatomy-strong: #111113;
      --anatomy-muted: #717176;
      --anatomy-paper: #fbfbfa;
      --anatomy-face: #ffffff;
      --anatomy-top: #ffffff;
      --anatomy-shade-0: #d4d4d0;
      --anatomy-shade-1: #dfdfdb;
      --anatomy-shade-2: #e9e9e5;
      --anatomy-shade-3: #f3f3f0;
      --anatomy-hi: #18181a;
      --anatomy-mid: #525258;
      --anatomy-lo: #82828a;
      --anatomy-faint: #d4d4d8;
      --anatomy-halo: #8a8a80;
      --anatomy-halo-opacity: 0.28;
      --anatomy-lift: inset 0 1px 0 0 #ffffff, 0 0 0 1px #00000012, 0 4px 16px -2px #00000010, 0 16px 32px -8px #00000014;
    }

    body {
      margin: 0;
      padding: 32px;
      background: var(--anatomy-page);
      font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
      color: var(--anatomy-text);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      overflow-x: hidden;
    }

    .bw-card {
      width: 100%;
      max-width: 1380px;
      background: var(--anatomy-card);
      border: 1px solid rgba(0, 0, 0, 0.12);
      border-radius: 20px;
      padding: 32px;
      box-shadow: var(--anatomy-lift);
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    .card-header {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      border-bottom: 1px solid var(--anatomy-faint);
      padding-bottom: 20px;
    }

    .fig-label {
      font-family: var(--anatomy-mono);
      font-size: 13px;
      font-weight: 800;
      color: var(--anatomy-strong);
      letter-spacing: 0.8px;
    }

    .fig-title {
      font-size: 24px;
      font-weight: 900;
      color: var(--anatomy-strong);
      margin-top: 4px;
      letter-spacing: -0.5px;
    }

    .bw-btn {
      padding: 9px 18px;
      border-radius: 10px;
      font-family: var(--anatomy-mono);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid rgba(0, 0, 0, 0.18);
      background: #ffffff;
      color: var(--anatomy-strong);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .bw-btn:hover {
      background: #f4f4f1;
      border-color: #000000;
    }
    .bw-btn.active {
      background: #18181a;
      color: #ffffff;
      border-color: #18181a;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    .readout-pill {
      padding: 8px 18px;
      border-radius: 9999px;
      background: #f4f4f1;
      border: 1px solid #18181a;
      color: #18181a;
      font-family: var(--anatomy-mono);
      font-size: 13px;
      font-weight: 800;
    }
    .readout-pill.tamper {
      background: #fee2e2;
      border-color: #b91c1c;
      color: #991b1b;
    }

    .svg-stage {
      width: 100%;
      height: auto;
      aspect-ratio: 16 / 9;
      background: #ffffff;
      border-radius: 16px;
      overflow: hidden;
      border: 1px solid rgba(0, 0, 0, 0.08);
      position: relative;
    }

    /* 3D Exploded Assemblies Transitions */
    .anatomy-assembly {
      transition: transform 0.65s cubic-bezier(0.32, 0.72, 0, 1), opacity 0.4s ease;
    }

    .exploded #assembly-sack {
      transform: translateY(-160px);
    }
    .exploded #assembly-platter {
      transform: translateY(-80px);
    }
    .exploded #assembly-loadcell {
      transform: translate(60px, 30px);
    }
    .exploded #assembly-indicator {
      transform: translateY(-50px);
    }
    .exploded #assembly-dongle {
      transform: translate(40px, 20px);
    }

    .card-footer {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      border-top: 1px solid var(--anatomy-faint);
      padding-top: 20px;
      font-size: 13px;
    }

    .legend-list {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      font-family: var(--anatomy-mono);
      font-size: 12px;
      font-weight: 600;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .legend-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      border: 1px solid #000;
    }
  </style>
</head>
<body>

  <div class="bw-card">
    
    <!-- Anatomy Card Header -->
    <div class="card-header">
      <div>
        <div class="fig-label">FIG 1. PHYSICAL TELEMETRY INTERCEPT &amp; STATUTORY VERIFICATION (OIML R-76)</div>
        <div class="fig-title">PrecisionX Sovereign NAWI Legal Metrology Architecture</div>
      </div>

      <div style="display:flex; gap:10px;">
        <button id="btnExplode" onclick="toggleExplode()" class="bw-btn">
          <span>💥</span>
          <span id="lblExplode">Explode Machine</span>
        </button>

        <button id="btnTamper" onclick="toggleTamper()" class="bw-btn">
          <span>🧲</span>
          <span id="lblTamper">Simulate Magnet Fraud</span>
        </button>

        <a href="SIH_Login_With_Background.html" class="bw-btn" style="background:#18181a; color:#ffffff;">
          <span>🔐</span>
          <span>Login Screen</span>
        </a>
      </div>
    </div>

    <!-- Interactive Load Selector Strip -->
    <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; padding:12px 20px; border-radius:12px; background:#f8f8f6; border:1px solid #e5e5e2;">
      <div style="font-family:var(--anatomy-mono); font-size:12px; font-weight:800; color:var(--anatomy-strong);">
        SELECT APPLIED LOAD (MANDI SACK):
      </div>

      <div style="display:flex; gap:8px;">
        <button onclick="setLoad(0)" id="load-0" class="bw-btn">0 kg (Tare)</button>
        <button onclick="setLoad(5)" id="load-5" class="bw-btn">5 kg</button>
        <button onclick="setLoad(25)" id="load-25" class="bw-btn">25 kg (500e)</button>
        <button onclick="setLoad(50)" id="load-50" class="bw-btn active">50 kg (1000e)</button>
        <button onclick="setLoad(150)" id="load-150" class="bw-btn">150 kg (Max)</button>
      </div>

      <div id="readoutStatus" class="readout-pill">
        TABLE 6 MPE: PASS (Δ = +12.0 g)
      </div>
    </div>

    <!-- Black & White 3D Isometric SVG Container -->
    <div class="svg-stage" id="svgStage">
      <svg class="iso-svg" viewBox="0 0 ${WIDTH} ${HEIGHT}" width="${WIDTH}" height="${HEIGHT}">
        ${allGeometry}
      </svg>
    </div>

    <!-- Legend & Technical Specification -->
    <div class="card-footer">
      <div class="legend-list">
        <div class="legend-item">
          <span class="legend-dot" style="background:#ffffff;"></span>
          <span>1. NAWI Mandi Platform Scale (Class III)</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background:#dfdfdb;"></span>
          <span>2. Smart IoT Bridge Dongle (RS-232 / USB)</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background:#82828a;"></span>
          <span>3. Sovereign OIML Table 6 Engine</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background:#18181a;"></span>
          <span>4. RFC 8032 Ed25519 DCC Certificate</span>
        </div>
      </div>

      <div style="font-family:var(--anatomy-mono); font-size:11px; color:var(--anatomy-muted);">
        Live 100 Hz Raw ADC · Latency &lt; 0.01s · Anti-Tamper Sealed
      </div>
    </div>

  </div>

  <script>
    let isExploded = false;
    let isTampered = false;
    let currentWeight = 50;

    function toggleExplode() {
      const stage = document.getElementById('svgStage');
      const btn = document.getElementById('btnExplode');
      const lbl = document.getElementById('lblExplode');
      isExploded = !isExploded;

      if (isExploded) {
        stage.classList.add('exploded');
        btn.classList.add('active');
        lbl.textContent = 'Collapse Machine';
      } else {
        stage.classList.remove('exploded');
        btn.classList.remove('active');
        lbl.textContent = 'Explode Machine';
      }
    }

    function toggleTamper() {
      const btn = document.getElementById('btnTamper');
      const lbl = document.getElementById('lblTamper');
      const readout = document.getElementById('readoutStatus');
      isTampered = !isTampered;

      if (isTampered) {
        btn.classList.add('active');
        lbl.textContent = 'Remove Magnet (+250g Fraud)';
        readout.className = 'readout-pill tamper';
        readout.textContent = 'MPE VIOLATION DETECTED: FRAUD (Δ = +262.0 g > ±50g)';
      } else {
        btn.classList.remove('active');
        lbl.textContent = 'Simulate Magnet Fraud';
        updateReadout();
      }
    }

    function setLoad(kg) {
      currentWeight = kg;
      [0, 5, 25, 50, 150].forEach(w => {
        const b = document.getElementById('load-' + w);
        if (b) {
          if (w === kg) b.classList.add('active');
          else b.classList.remove('active');
        }
      });
      if (!isTampered) updateReadout();
    }

    function updateReadout() {
      const readout = document.getElementById('readoutStatus');
      if (currentWeight === 0) {
        readout.className = 'readout-pill';
        readout.textContent = 'TARE ZERO SETTLED: 0.000 kg (e = 50g)';
      } else if (currentWeight === 5) {
        readout.className = 'readout-pill';
        readout.textContent = 'TABLE 6 MPE (±25.0 g): PASS (Δ = +4.0 g)';
      } else if (currentWeight === 25) {
        readout.className = 'readout-pill';
        readout.textContent = 'TABLE 6 MPE (±50.0 g): PASS (Δ = +8.0 g)';
      } else if (currentWeight === 50) {
        readout.className = 'readout-pill';
        readout.textContent = 'TABLE 6 MPE (±50.0 g): PASS (Δ = +12.0 g)';
      } else if (currentWeight === 150) {
        readout.className = 'readout-pill';
        readout.textContent = 'TABLE 6 MPE (±75.0 g): PASS (Δ = +24.0 g)';
      }
    }
  </script>

</body>
</html>
`;

const outputPath = "/home/zeno/Desktop/SIH_NAWI_Anatomy_BW.html";
writeFileSync(outputPath, bwPage);
console.log("Successfully compiled Signature Black & White Anatomy Explainer to:", outputPath);
