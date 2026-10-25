import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));

// 1200x650 Wide Metrology Studio Canvas
const WIDTH = 1200;
const HEIGHT = 650;

// High-craft custom SVG generator with explicit 4-tone metrological shading
// Colors: Slate Neutrals, Cyan/Blue Metrology Core, Amber Mandi Accents, Emerald Verification Seals
const completeWorkbenchHtml = `<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrecisionX (SIH26035) — 3-Tier Sovereign Legal Metrology NAWI Verification Workbench</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            cyan: '#06b6d4',
                            emerald: '#10b981',
                            amber: '#f59e0b',
                            purple: '#a855f7',
                            slateBg: '#030712'
                        }
                    },
                    fontFamily: {
                        mono: ['JetBrains Mono', 'Menlo', 'Consolas', 'monospace'],
                        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
                    }
                }
            }
        };
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        body {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: #030712;
            color: #f8fafc;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }

        /* Ambient Glowing Metrology Highlights */
        .glow-cyan { filter: drop-shadow(0 0 12px rgba(6, 182, 212, 0.4)); }
        .glow-amber { filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.4)); }
        .glow-emerald { filter: drop-shadow(0 0 12px rgba(16, 185, 129, 0.4)); }
        .glow-purple { filter: drop-shadow(0 0 12px rgba(168, 85, 247, 0.4)); }

        .hud-card {
            background: rgba(11, 18, 33, 0.88);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 14px 18px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .hud-card:hover {
            transform: translateY(-2px);
        }

        .iso-control-btn {
            background: #0f172a;
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 8px;
            padding: 8px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .iso-control-btn:hover {
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 0 16px rgba(6, 182, 212, 0.45);
        }
        .iso-control-btn.active {
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.6);
        }

        /* Isometric Layer Transitions for Explode Mode */
        .iso-deck, .iso-tier-block {
            transition: transform 0.7s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.5s ease;
        }

        @keyframes pulseTelemetry {
            from { stroke-dashoffset: 0; }
            to { stroke-dashoffset: -32px; }
        }
        .telemetry-pulse {
            animation: pulseTelemetry 0.8s linear infinite;
        }
    </style>
</head>
<body class="p-4 sm:p-6 lg:p-8 min-h-screen flex flex-col items-center">

    <div class="w-full max-w-7xl space-y-6">

        <!-- 1. NATIONAL SIH BANNER & MASTER CONTROLS -->
        <header class="flex flex-wrap items-center justify-between gap-4 p-5 rounded-2xl bg-slate-950/90 border border-cyan-500/30 shadow-2xl backdrop-blur-md">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-700 flex items-center justify-center text-white text-2xl font-black shadow-lg shadow-cyan-500/25">
                    ⚖️
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <span class="px-2.5 py-0.5 rounded text-[10px] font-mono font-bold bg-cyan-950 text-cyan-300 border border-cyan-700/60 uppercase tracking-widest">
                            SIH26035 SOVEREIGN ARCHITECTURE
                        </span>
                        <span class="text-xs text-slate-400 font-mono">Ministry of Consumer Affairs • Legal Metrology Division</span>
                    </div>
                    <h1 class="text-xl sm:text-2xl font-black text-white tracking-tight mt-0.5">
                        PrecisionX: 3-Tier Sovereign Legal Metrology Workbench (OIML R-76 NAWI)
                    </h1>
                </div>
            </div>

            <!-- Interactive Workbench Action Buttons -->
            <div class="flex flex-wrap items-center gap-2 sm:gap-3">
                <button id="btn-explode" class="iso-control-btn active" onclick="toggleExplode()">
                    <span>💥</span>
                    <span>Explode Architecture (Inspect Internals)</span>
                </button>
                <button class="iso-control-btn" onclick="applyTestLoad(150.000, 'Max Mandi Capacity')">
                    <span>🌾</span>
                    <span>150 kg (Max Load)</span>
                </button>
                <button class="iso-control-btn" onclick="applyTestLoad(50.000, '50kg Wheat Sack')">
                    <span>⚖️</span>
                    <span>50 kg (Standard)</span>
                </button>
                <button class="iso-control-btn" onclick="simulateCornerBias()">
                    <span>⚠️</span>
                    <span>Corner Bias Test</span>
                </button>
            </div>
        </header>

        <!-- 2. REAL-TIME NATIONAL METROLOGY TELEMETRY HUD -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Metric 1: Compliance -->
            <div class="hud-card border-l-4 border-l-cyan-400">
                <div class="text-[11px] font-mono text-slate-400 font-semibold uppercase tracking-wider">National Compliance Rate</div>
                <div id="hud-compliance" class="text-3xl font-black text-cyan-400 font-mono mt-1">98.4%</div>
                <div class="text-[11px] text-emerald-400 font-mono mt-1 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>42,890 Mandis Verified Under R-76</span>
                </div>
            </div>

            <!-- Metric 2: Active Nodes -->
            <div class="hud-card border-l-4 border-l-emerald-400">
                <div class="text-[11px] font-mono text-slate-400 font-semibold uppercase tracking-wider">Active Enforcement Nodes</div>
                <div id="hud-nodes" class="text-3xl font-black text-emerald-400 font-mono mt-1">7,412</div>
                <div class="text-[11px] text-slate-400 font-mono mt-1 flex items-center gap-1.5">
                    <span>District Enforcement & Flying Squads</span>
                </div>
            </div>

            <!-- Metric 3: Live Scale Telemetry -->
            <div class="hud-card border-l-4 border-l-amber-400">
                <div class="text-[11px] font-mono text-slate-400 font-semibold uppercase tracking-wider">Mandi Platform Telemetry</div>
                <div id="hud-mass" class="text-3xl font-black text-amber-400 font-mono mt-1">50.000 kg</div>
                <div class="text-[11px] text-cyan-300 font-mono mt-1 flex items-center gap-1.5">
                    <span>RS-232 / USB 100 Hz Continuous Stream</span>
                </div>
            </div>

            <!-- Metric 4: Cryptographic Seal -->
            <div class="hud-card border-l-4 border-l-purple-400">
                <div class="text-[11px] font-mono text-slate-400 font-semibold uppercase tracking-wider">Statutory Audit Seal</div>
                <div id="hud-hash" class="text-xs font-bold text-purple-300 font-mono mt-2 truncate">SHA256: 9e4f2a8c...71b0</div>
                <div class="text-[11px] text-emerald-400 font-mono mt-1.5 flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-purple-400"></span>
                    <span>RFC 8032 Ed25519 • PTB DCC Sealed</span>
                </div>
            </div>
        </div>

        <!-- 3. PRODUCTION-GRADE ISOMETRIC 3D ARCHITECTURAL SVG CANVAS -->
        <div class="relative w-full rounded-2xl overflow-hidden border border-slate-800 bg-[#040814] shadow-2xl p-4 sm:p-6 flex flex-col items-center">
            
            <!-- Isometric SVG Engine -->
            <svg id="metrologySvg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 640" class="w-full h-auto max-h-[640px] select-none" style="display:block;">
                <defs>
                    <!-- Lighting Gradients -->
                    <radialGradient id="stageGlow" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.14"/>
                        <stop offset="60%" stop-color="#020617" stop-opacity="0.6"/>
                        <stop offset="100%" stop-color="#020617" stop-opacity="0.95"/>
                    </radialGradient>
                    <!-- Diamond Tread Plate Pattern -->
                    <pattern id="diamondTread" width="16" height="16" patternUnits="userSpaceOnUse">
                        <path d="M 8 0 L 16 8 L 8 16 L 0 8 Z" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.8"/>
                    </pattern>
                </defs>

                <!-- Ambient Stage Backdrop -->
                <rect width="1200" height="640" fill="#040814"/>
                <rect width="1200" height="640" fill="url(#stageGlow)"/>

                <!-- Metrology Coordinate Rings & Perspective Grid Lines -->
                <g opacity="0.16">
                    <ellipse cx="600" cy="350" rx="540" ry="220" fill="none" stroke="#22d3ee" stroke-width="1.2" stroke-dasharray="4 8"/>
                    <ellipse cx="600" cy="350" rx="360" ry="150" fill="none" stroke="#22d3ee" stroke-width="1" stroke-dasharray="3 6"/>
                    <line x1="100" y1="350" x2="1100" y2="350" stroke="#22d3ee" stroke-width="0.8" stroke-dasharray="4 6"/>
                </g>

                <!-- ================= 0. HEAVY GRANITE SURFACE BENCH ================= -->
                <g id="granite-bench">
                    <!-- Base pneumatic leveling feet -->
                    <ellipse cx="140" cy="340" rx="28" ry="12" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
                    <ellipse cx="1060" cy="340" rx="28" ry="12" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
                    <ellipse cx="600" cy="530" rx="36" ry="16" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
                    <ellipse cx="600" cy="180" rx="36" ry="16" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>

                    <!-- Main Granite Slab Base (Isometric Hexagon) -->
                    <polygon points="600,160 1090,320 1090,360 600,560 110,360 110,320" fill="#090e1a" stroke="#1e293b" stroke-width="2"/>
                    <!-- Slab Thickness Side Bevels -->
                    <polygon points="110,320 600,520 600,560 110,360" fill="#0d1527" stroke="#1e293b" stroke-width="1"/>
                    <polygon points="600,520 1090,320 1090,360 600,560" fill="#141e34" stroke="#1e293b" stroke-width="1"/>
                    <!-- Top Slab Surface -->
                    <polygon points="600,160 1090,320 600,520 110,320" fill="#101a2e" stroke="#22d3ee" stroke-opacity="0.35" stroke-width="1.8"/>

                    <!-- Front Scale Ruler Ticks -->
                    <path d="M 170 340 L 580 510" stroke="#334155" stroke-width="2"/>
                    <path d="M 180 340 L 180 348 M 220 357 L 220 365 M 260 373 L 260 381 M 300 390 L 300 398 M 340 407 L 340 415 M 380 423 L 380 431 M 420 440 L 420 448 M 460 457 L 460 465 M 500 473 L 500 481 M 540 490 L 540 498" stroke="#38bdf8" stroke-width="1.5"/>
                    <text x="350" y="445" font-family="'JetBrains Mono', monospace" font-size="10" fill="#64748b" transform="rotate(22 350 445)">OIML R-76 DATUM BENCH</text>
                </g>

                <!-- ================= HIGH-SPEED INTERCONNECTING TELEMETRY BUSES ================= -->
                <!-- Bus 1: Physical NAWI -> Statutory MPE Engine -->
                <g id="telemetry-bus-1">
                    <path d="M 370 330 C 420 360, 440 340, 480 330" fill="none" stroke="#0f172a" stroke-width="8" stroke-linecap="round"/>
                    <path d="M 370 330 C 420 360, 440 340, 480 330" fill="none" stroke="#0284c7" stroke-width="4" stroke-linecap="round"/>
                    <path class="telemetry-pulse" d="M 370 330 C 420 360, 440 340, 480 330" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="6 14" stroke-linecap="round"/>
                    <!-- Data Packet Flow Badge -->
                    <rect x="400" y="318" width="54" height="16" rx="4" fill="#082f49" stroke="#0284c7" stroke-width="1"/>
                    <text x="427" y="329" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" fill="#38bdf8" text-anchor="middle">100Hz RAW</text>
                </g>

                <!-- Bus 2: Statutory MPE Engine -> Sovereign Cryptographic Vault -->
                <g id="telemetry-bus-2">
                    <path d="M 720 330 C 760 340, 780 360, 830 330" fill="none" stroke="#0f172a" stroke-width="8" stroke-linecap="round"/>
                    <path d="M 720 330 C 760 340, 780 360, 830 330" fill="none" stroke="#7e22ce" stroke-width="4" stroke-linecap="round"/>
                    <path class="telemetry-pulse" d="M 720 330 C 760 340, 780 360, 830 330" fill="none" stroke="#c084fc" stroke-width="2.5" stroke-dasharray="6 14" stroke-linecap="round"/>
                    <!-- Data Packet Flow Badge -->
                    <rect x="750" y="318" width="58" height="16" rx="4" fill="#3b0764" stroke="#a855f7" stroke-width="1"/>
                    <text x="779" y="329" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" fill="#e9d5ff" text-anchor="middle">MPE AUDIT</text>
                </g>

                <!-- ================= 1. PHYSICAL TIER (MANDI & NAWI SCALE) ================= -->
                <g id="tier-physical" class="iso-tier-block">
                    <!-- Base Sub-Chassis Block -->
                    <g id="nawi-subchassis">
                        <!-- Left-side isometric box (X: 180 to 360, Y: 220 to 380) -->
                        <polygon points="270,220 370,270 370,330 270,380 170,330 170,270" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
                        <!-- Side facets -->
                        <polygon points="170,270 270,320 270,380 170,330" fill="#1e293b" stroke="#334155" stroke-width="1"/>
                        <polygon points="270,320 370,270 370,330 270,380" fill="#334155" stroke="#475569" stroke-width="1"/>
                        <!-- Top bed -->
                        <polygon points="270,220 370,270 270,320 170,270" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>

                        <!-- Internal Cutaway: Bending Beam Load Cell -->
                        <polygon points="245,260 295,285 295,305 245,280" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
                        <polygon points="295,285 305,280 305,300 295,305" fill="#94a3b8" stroke="#64748b" stroke-width="1"/>
                        <polygon points="245,260 255,255 305,280 295,285" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
                        <!-- Strain Gauge Rosette & Wiring -->
                        <rect x="265" y="270" width="14" height="6" fill="#f59e0b" rx="1"/>
                        <path d="M 305 290 L 325 300 L 340 295" stroke="#ef4444" stroke-width="1.5" fill="none"/>
                        <path d="M 305 293 L 325 303 L 340 298" stroke="#38bdf8" stroke-width="1.5" fill="none"/>

                        <!-- 4 Corner Coil Suspension Flexure Springs -->
                        <path d="M 195 260 L 195 235" stroke="#94a3b8" stroke-width="3"/>
                        <path d="M 345 260 L 345 235" stroke="#94a3b8" stroke-width="3"/>
                        <path d="M 270 295 L 270 270" stroke="#94a3b8" stroke-width="3"/>
                        <path d="M 270 230 L 270 205" stroke="#94a3b8" stroke-width="3"/>

                        <!-- Mandi Terminal Local LED Screen (Front face) -->
                        <polygon points="180,300 250,335 250,360 180,325" fill="#020617" stroke="#0284c7" stroke-width="1.2"/>
                        <text id="scale-live-text" x="215" y="338" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800" fill="#38bdf8" text-anchor="middle" transform="rotate(26 215 338)">50.000 kg</text>
                        <!-- Zero Stability Indicator LED -->
                        <circle cx="240" cy="350" r="3" fill="#10b981" class="glow-emerald"/>
                        <text x="233" y="352" font-family="'JetBrains Mono', monospace" font-size="6" fill="#a7f3d0" text-anchor="end">ZERO</text>
                    </g>

                    <!-- Suspended Weighing Platter & Grain Sack (Lifts in Explode Mode) -->
                    <g id="weighing-deck" class="iso-deck" style="transform: translateY(0px);">
                        <!-- Stainless Steel Diamond Platter -->
                        <polygon points="270,180 380,235 380,248 270,303 160,248 160,235" fill="#334155" stroke="#64748b" stroke-width="1"/>
                        <polygon points="160,235 270,290 270,303 160,248" fill="#475569" stroke="#64748b" stroke-width="1"/>
                        <polygon points="270,290 380,235 380,248 270,303" fill="#64748b" stroke="#94a3b8" stroke-width="1"/>
                        <!-- Platter Top with Diamond Tread -->
                        <polygon points="270,180 380,235 270,290 160,235" fill="#475569" stroke="#94a3b8" stroke-width="1.8"/>
                        <polygon points="270,180 380,235 270,290 160,235" fill="url(#diamondTread)"/>

                        <!-- 5 OIML R-76 Eccentricity Test Target Rings stamped on pan -->
                        <!-- Center -->
                        <ellipse cx="270" cy="235" rx="14" ry="7" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
                        <circle cx="270" cy="235" r="2.5" fill="#38bdf8"/>
                        <text x="270" y="247" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="700" fill="#38bdf8" text-anchor="middle">CTR (0)</text>
                        <!-- Q1 Front-Left -->
                        <ellipse cx="215" cy="245" rx="10" ry="5" fill="none" stroke="#64748b" stroke-width="1"/>
                        <text x="215" y="254" font-family="'JetBrains Mono', monospace" font-size="6" fill="#94a3b8" text-anchor="middle">Q1</text>
                        <!-- Q2 Front-Right -->
                        <ellipse cx="325" cy="245" rx="10" ry="5" fill="none" stroke="#64748b" stroke-width="1"/>
                        <text x="325" y="254" font-family="'JetBrains Mono', monospace" font-size="6" fill="#94a3b8" text-anchor="middle">Q2</text>
                        <!-- Q3 Rear-Right -->
                        <ellipse cx="325" cy="215" rx="10" ry="5" fill="none" stroke="#64748b" stroke-width="1"/>
                        <text x="325" y="224" font-family="'JetBrains Mono', monospace" font-size="6" fill="#94a3b8" text-anchor="middle">Q3</text>
                        <!-- Q4 Rear-Left -->
                        <ellipse cx="215" cy="215" rx="10" ry="5" fill="none" stroke="#64748b" stroke-width="1"/>
                        <text x="215" y="224" font-family="'JetBrains Mono', monospace" font-size="6" fill="#94a3b8" text-anchor="middle">Q4</text>

                        <!-- Mandi Commercial Test Load: 50 kg Burlap Grain Sack -->
                        <g id="grain-sack">
                            <!-- Burlap Sack Body -->
                            <path d="M 245 205 Q 270 195 295 205 Q 315 220 305 245 Q 270 260 235 245 Q 225 220 245 205 Z" fill="#d97706" stroke="#b45309" stroke-width="1.8"/>
                            <path d="M 235 245 Q 270 260 305 245 L 305 250 Q 270 265 235 250 Z" fill="#92400e"/>
                            <!-- Sack Tie Neck -->
                            <ellipse cx="270" cy="205" rx="12" ry="6" fill="#b45309" stroke="#78350f" stroke-width="1.5"/>
                            <ellipse cx="270" cy="198" rx="8" ry="4" fill="#f59e0b" stroke="#b45309" stroke-width="1.2"/>
                            <!-- Printed Government Mandi Stencil -->
                            <text x="270" y="232" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="800" fill="#78350f" text-anchor="middle">50 kg WHEAT</text>
                            <text x="270" y="241" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="600" fill="#92400e" text-anchor="middle">CLASS III (e=50g)</text>
                        </g>
                    </g>
                </g>

                <!-- ================= 2. STATUTORY MPE ENGINE TIER (OIML R-76 TABLE 6) ================= -->
                <g id="tier-engine" class="iso-tier-block">
                    <!-- Engine Enclosure Box (Center: X: 500 to 700, Y: 220 to 390) -->
                    <polygon points="600,200 710,255 710,325 600,380 490,325 490,255" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
                    <!-- Facets -->
                    <polygon points="490,255 600,310 600,380 490,325" fill="#0d1b33" stroke="#1e293b" stroke-width="1"/>
                    <polygon points="600,310 710,255 710,325 600,380" fill="#142646" stroke="#1e293b" stroke-width="1"/>
                    <!-- Top Deck -->
                    <polygon points="600,200 710,255 600,310 490,255" fill="#112240" stroke="#06b6d4" stroke-width="1.8"/>

                    <!-- Tilted Glass Inspection Core Console -->
                    <polygon points="590,215 690,265 600,310 500,260" fill="#020817" stroke="#00f2fe" stroke-width="1.5"/>

                    <!-- Display Matrix Text Lines (OIML Table 6 Engine) -->
                    <g transform="rotate(2 600 250)">
                        <text x="595" y="235" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="800" fill="#38bdf8" text-anchor="middle">⚖️ OIML R-76 TABLE 6 ENGINE</text>
                        <text x="595" y="247" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="700" fill="#94a3b8" text-anchor="middle">CLASS III: 500e &lt; m ≤ 2000e</text>
                        
                        <!-- High-Contrast Verdict Banner -->
                        <rect x="525" y="254" width="140" height="24" rx="4" fill="#022c22" stroke="#10b981" stroke-width="1.2"/>
                        <text id="engine-verdict" x="595" y="266" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="900" fill="#34d399" text-anchor="middle">MPE LIMIT: ±1.0e (±50g)</text>
                        <text id="engine-dev" x="595" y="275" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="700" fill="#6ee7b7" text-anchor="middle">DEV: Δ = +12.0g [PASS]</text>

                        <text x="595" y="291" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="600" fill="#38bdf8" text-anchor="middle">ZERO DRIFT: 0.00e • CORNER: 0.04e</text>
                    </g>

                    <!-- Status LEDs (Zero, MPE, Linear) -->
                    <circle cx="530" cy="325" r="3.5" fill="#10b981" class="glow-emerald"/>
                    <text x="530" y="337" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="700" fill="#a7f3d0" text-anchor="middle">ZERO OK</text>

                    <circle cx="600" cy="340" r="3.5" fill="#10b981" class="glow-emerald"/>
                    <text x="600" y="352" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="700" fill="#a7f3d0" text-anchor="middle">MPE PASS</text>

                    <circle cx="670" cy="325" r="3.5" fill="#38bdf8" class="glow-cyan"/>
                    <text x="670" y="337" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="700" fill="#bae6fd" text-anchor="middle">LINEAR</text>
                </g>

                <!-- ================= 3. SOVEREIGN CRYPTOGRAPHIC TIER (Ed25519 & PDF/A-3) ================= -->
                <g id="tier-crypto" class="iso-tier-block">
                    <!-- High-Security Cryptographic Vault Block (Right: X: 840 to 1040, Y: 220 to 390) -->
                    <polygon points="940,200 1050,255 1050,335 940,390 830,335 830,255" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
                    <!-- Facets -->
                    <polygon points="830,255 940,310 940,390 830,335" fill="#1a102f" stroke="#2e1065" stroke-width="1"/>
                    <polygon points="940,310 1050,255 1050,335 940,390" fill="#2e1065" stroke="#3b0764" stroke-width="1"/>
                    <!-- Top Vault Plate -->
                    <polygon points="940,200 1050,255 940,310 830,255" fill="#241442" stroke="#a855f7" stroke-width="1.8"/>

                    <!-- Chamber A: Ed25519 Hardware Signing Enclave (RFC 8032) -->
                    <g transform="translate(850, 225)">
                        <polygon points="40,0 75,18 40,36 5,18" fill="#0f0728" stroke="#a855f7" stroke-width="1.2"/>
                        <text x="40" y="15" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="800" fill="#c084fc" text-anchor="middle">ED25519 HSM</text>
                        <text x="40" y="25" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="600" fill="#e9d5ff" text-anchor="middle">RFC 8032 SIGN</text>
                    </g>

                    <!-- Chamber B: PTB Digital Calibration Certificate (DCC) XML Engine -->
                    <g transform="translate(930, 225)">
                        <polygon points="40,0 75,18 40,36 5,18" fill="#061e1b" stroke="#10b981" stroke-width="1.2"/>
                        <text x="40" y="15" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="800" fill="#34d399" text-anchor="middle">PTB DCC XML</text>
                        <text x="40" y="25" font-family="'JetBrains Mono', monospace" font-size="5.5" font-weight="600" fill="#a7f3d0" text-anchor="middle">ISO/IEC 17025</text>
                    </g>

                    <!-- Offline Cryptographic QR Verification Matrix Seal Plaque -->
                    <g transform="translate(885, 270)">
                        <polygon points="55,0 110,28 55,56 0,28" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
                        <!-- QR Pattern Blocks -->
                        <!-- Top-Left Finder Box -->
                        <polygon points="20,12 34,19 20,26 6,19" fill="#020617"/>
                        <polygon points="20,15 28,19 20,23 12,19" fill="#ffffff"/>
                        <!-- Top-Right Finder Box -->
                        <polygon points="75,12 89,19 75,26 61,19" fill="#020617"/>
                        <polygon points="75,15 83,19 75,23 67,19" fill="#ffffff"/>
                        <!-- Bottom Finder Box -->
                        <polygon points="48,27 62,34 48,41 34,34" fill="#020617"/>
                        <polygon points="48,30 56,34 48,38 40,34" fill="#ffffff"/>

                        <text x="55" y="50" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="800" fill="#020617" text-anchor="middle">OFFLINE QR STAMP</text>
                    </g>

                    <!-- Vault Status Badges on Side -->
                    <text x="940" y="340" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="800" fill="#e9d5ff" text-anchor="middle">ISO PDF/A-3 EMBEDDED</text>
                    <text x="940" y="354" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="600" fill="#a855f7" text-anchor="middle">ANTI-ROLLBACK SECURED</text>
                </g>

                <!-- Tier Descriptive Labels Under The Bases -->
                <text x="270" y="420" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800" fill="#f59e0b" text-anchor="middle">TIER 1: PHYSICAL SCALE</text>
                <text x="270" y="434" font-family="'Inter', sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">Grain Mandi Platform & Load Cell</text>

                <text x="600" y="420" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800" fill="#38bdf8" text-anchor="middle">TIER 2: STATUTORY ENGINE</text>
                <text x="600" y="434" font-family="'Inter', sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">OIML R-76 Table 6 MPE Evaluator</text>

                <text x="940" y="420" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800" fill="#c084fc" text-anchor="middle">TIER 3: CRYPTOGRAPHIC VAULT</text>
                <text x="940" y="434" font-family="'Inter', sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">Ed25519 & PDF/A-3 DCC Archive</text>
            </svg>
        </div>

        <!-- 4. THREE-TIER ARCHITECTURAL SPECIFICATION BREAKDOWN -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <!-- Tier 1 Spec -->
            <div class="hud-card border-t-4 border-t-amber-400">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-mono font-bold text-amber-400 uppercase tracking-wider">Tier 1: Physical Metrology</span>
                    <span class="text-[11px] font-mono text-slate-400">Mandi Weighing Deck</span>
                </div>
                <h3 class="text-base font-bold text-white mb-2">Commercial Weighing Platform (NAWI)</h3>
                <p class="text-xs text-slate-300 leading-relaxed mb-3">
                    Rugged Class III platform scale in agricultural mandis receiving grain bags and bulk produce, equipped with dual-ended shear beam load cells, coil suspension flexures, and shielded telemetry interface.
                </p>
                <ul class="space-y-1.5 text-[11px] font-mono text-slate-400">
                    <li class="flex items-center gap-1.5">
                        <span class="text-amber-400">▸</span>
                        <span>Capacity: <strong>150 kg (e = 50 g, n = 3000)</strong></span>
                    </li>
                    <li class="flex items-center gap-1.5">
                        <span class="text-amber-400">▸</span>
                        <span>Continuous Telemetry: <strong>RS-232 / USB at 100 Hz</strong></span>
                    </li>
                    <li class="flex items-center gap-1.5">
                        <span class="text-amber-400">▸</span>
                        <span>5-Point Eccentricity: <strong>Center, Q1, Q2, Q3, Q4</strong></span>
                    </li>
                </ul>
            </div>

            <!-- Tier 2 Spec -->
            <div class="hud-card border-t-4 border-t-cyan-400">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider">Tier 2: Statutory MPE Engine</span>
                    <span class="text-[11px] font-mono text-slate-400">OIML R-76 Table 6</span>
                </div>
                <h3 class="text-base font-bold text-white mb-2">Tolerance & Bias Verification Core</h3>
                <p class="text-xs text-slate-300 leading-relaxed mb-3">
                    Computes statutory Maximum Permissible Error (MPE) brackets dynamically. Validates scale compliance across zero-point drift, repeatability, and corner weight eccentricity bias in sub-milliseconds.
                </p>
                <ul class="space-y-1.5 text-[11px] font-mono text-slate-400">
                    <li class="flex items-center gap-1.5">
                        <span class="text-cyan-400">▸</span>
                        <span>Initial Verification: <strong>0 ≤ m ≤ 500e → ±0.5e</strong></span>
                    </li>
                    <li class="flex items-center gap-1.5">
                        <span class="text-cyan-400">▸</span>
                        <span>Medium Load Bracket: <strong>500e &lt; m ≤ 2000e → ±1.0e</strong></span>
                    </li>
                    <li class="flex items-center gap-1.5">
                        <span class="text-cyan-400">▸</span>
                        <span>Tolerance Verdict: <strong>Δ = +12.0 g (Limit ±50 g) PASS</strong></span>
                    </li>
                </ul>
            </div>

            <!-- Tier 3 Spec -->
            <div class="hud-card border-t-4 border-t-purple-400">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-mono font-bold text-purple-400 uppercase tracking-wider">Tier 3: Cryptographic Vault</span>
                    <span class="text-[11px] font-mono text-slate-400">Ed25519 & PDF/A-3</span>
                </div>
                <h3 class="text-base font-bold text-white mb-2">Sovereign Archival & QR Verification</h3>
                <p class="text-xs text-slate-300 leading-relaxed mb-3">
                    Cryptographic hardware security module signing records with RFC 8032 Ed25519 (64-byte signature), embedding PTB Digital Calibration Certificate (DCC) XML into ISO PDF/A-3, and stamping offline QR codes.
                </p>
                <ul class="space-y-1.5 text-[11px] font-mono text-slate-400">
                    <li class="flex items-center gap-1.5">
                        <span class="text-purple-400">▸</span>
                        <span>Digital Signature: <strong>RFC 8032 Ed25519 Asymmetric</strong></span>
                    </li>
                    <li class="flex items-center gap-1.5">
                        <span class="text-purple-400">▸</span>
                        <span>Interoperability: <strong>PTB DCC XML (ISO/IEC 17025)</strong></span>
                    </li>
                    <li class="flex items-center gap-1.5">
                        <span class="text-purple-400">▸</span>
                        <span>Flying Squad Audit: <strong>100% Offline QR Verification</strong></span>
                    </li>
                </ul>
            </div>
        </div>

        <!-- 5. FOOTER & GOVERNMENT GAZETTE METROLOGY CREDENTIALS -->
        <footer class="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-800/80 text-xs text-slate-400 font-mono">
            <div>PrecisionX Metrology Engineering Team • Smart India Hackathon (SIH26035)</div>
            <div class="flex items-center gap-2">
                <span>National Legal Metrology Portal</span>
                <span>•</span>
                <span class="text-cyan-400">OIML R-76 Table 6 Certified</span>
            </div>
        </footer>

    </div>

    <!-- Interactive JS Controller -->
    <script>
        let isExploded = true; // Starts in exploded view to showcase full architecture
        let clock = 0;
        let baseMass = 50.000;
        let isCornerBias = false;

        const deck = document.getElementById("weighing-deck");
        const tierPhysical = document.getElementById("tier-physical");
        const tierEngine = document.getElementById("tier-engine");
        const tierCrypto = document.getElementById("tier-crypto");
        const scaleText = document.getElementById("scale-live-text");
        const hudMass = document.getElementById("hud-mass");
        const engineDev = document.getElementById("engine-dev");
        const engineVerdict = document.getElementById("engine-verdict");

        // Explode / Collapse Interaction Handler
        function updateExplodeView() {
            const btn = document.getElementById("btn-explode");
            if (isExploded) {
                if (btn) btn.innerHTML = "<span>💥</span><span>Collapse Assemblies</span>";
                if (deck) deck.style.transform = "translateY(-48px)";
                if (tierEngine) tierEngine.style.transform = "translateY(-24px)";
                if (tierCrypto) tierCrypto.style.transform = "translateY(-36px)";
            } else {
                if (btn) btn.innerHTML = "<span>💥</span><span>Explode Architecture (Inspect Internals)</span>";
                if (deck) deck.style.transform = "translateY(0px)";
                if (tierEngine) tierEngine.style.transform = "translateY(0px)";
                if (tierCrypto) tierCrypto.style.transform = "translateY(0px)";
            }
        }
        updateExplodeView();

        window.toggleExplode = function() {
            isExploded = !isExploded;
            updateExplodeView();
        };

        window.applyTestLoad = function(massKg, label) {
            baseMass = massKg;
            isCornerBias = false;
            updateLoadState();
        };

        window.simulateCornerBias = function() {
            isCornerBias = true;
            updateLoadState();
        };

        function updateLoadState() {
            const displayMass = isCornerBias ? (baseMass + 0.085) : baseMass;
            const devGrams = isCornerBias ? "+85.0g" : "+12.0g";
            const isPass = !isCornerBias;

            if (scaleText) scaleText.textContent = displayMass.toFixed(3) + " kg";
            if (hudMass) hudMass.textContent = displayMass.toFixed(3) + " kg";

            if (engineVerdict) {
                engineVerdict.textContent = isPass ? "MPE LIMIT: ±1.0e (±50g)" : "MPE LIMIT EXCEEDED (±50g)";
                engineVerdict.setAttribute("fill", isPass ? "#34d399" : "#f87171");
            }
            if (engineDev) {
                engineDev.textContent = isPass ? ("DEV: Δ = " + devGrams + " [PASS]") : ("DEV: Δ = " + devGrams + " [FAIL: CORNER BIAS]");
                engineDev.setAttribute("fill", isPass ? "#6ee7b7" : "#fca5a5");
            }
        }

        // Live balance jitter simulation
        function liveLoop() {
            clock += 0.016;
            const jitter = (Math.sin(clock * 4.2) * 0.003);
            const currentLive = (isCornerBias ? (baseMass + 0.085) : baseMass) + jitter;

            if (scaleText && !isCornerBias) scaleText.textContent = currentLive.toFixed(3) + " kg";
            if (hudMass && !isCornerBias) hudMass.textContent = currentLive.toFixed(3) + " kg";

            requestAnimationFrame(liveLoop);
        }
        requestAnimationFrame(liveLoop);
    </script>
</body>
</html>
`;

// Save production-grade workbench
const desktopPath = "/home/zeno/Desktop/PrecisionX_Sovereign_NAWI_Workbench.html";
const componentPath = "/home/zeno/Desktop/SIH APP/desktop/PrecisionX_Workbench_Component.html";

writeFileSync(desktopPath, completeWorkbenchHtml);
writeFileSync(componentPath, completeWorkbenchHtml);

console.log("Successfully generated high-craft PrecisionX Sovereign NAWI Workbench:");
console.log("- " + desktopPath);
console.log("- " + componentPath);
