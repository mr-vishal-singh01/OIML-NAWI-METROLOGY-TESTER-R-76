import { writeFileSync } from "node:fs";

// 1920x1080 Master Full HD Canvas
const WIDTH = 1920;
const HEIGHT = 1080;

const masterNawiSvg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="background:#020617; display:block;">
  <defs>
    <!-- Background Gradients -->
    <radialGradient id="ambientLeftGlow" cx="25%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.22"/>
      <stop offset="70%" stop-color="#020617" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="1"/>
    </radialGradient>

    <radialGradient id="ambientRightGlow" cx="80%" cy="50%" r="45%">
      <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.18"/>
      <stop offset="50%" stop-color="#06b6d4" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#020617" stop-opacity="1"/>
    </radialGradient>

    <!-- Metallic Gradients for Scale & Housing -->
    <linearGradient id="chromeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="25%" stop-color="#64748b"/>
      <stop offset="50%" stop-color="#f8fafc"/>
      <stop offset="75%" stop-color="#94a3b8"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <linearGradient id="steelPanGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="35%" stop-color="#1e293b"/>
      <stop offset="70%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <linearGradient id="goldSealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="40%" stop-color="#f59e0b"/>
      <stop offset="80%" stop-color="#b45309"/>
      <stop offset="100%" stop-color="#78350f"/>
    </linearGradient>

    <!-- Diamond Plate Tread Pattern -->
    <pattern id="treadPattern" width="16" height="16" patternUnits="userSpaceOnUse">
      <path d="M 8 0 L 16 8 L 8 16 L 0 8 Z" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="0.9"/>
      <circle cx="8" cy="8" r="1.5" fill="rgba(255,255,255,0.18)"/>
    </pattern>

    <!-- Cyber Isometric Grid Pattern -->
    <pattern id="isoGridPattern" width="60" height="34.64" patternUnits="userSpaceOnUse">
      <path d="M 0 17.32 L 30 0 L 60 17.32 L 30 34.64 Z" fill="none" stroke="rgba(30, 41, 59, 0.45)" stroke-width="0.8"/>
    </pattern>

    <!-- Glow Filters -->
    <filter id="ledBloom" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur1"/>
      <feGaussianBlur stdDeviation="9" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="shadowBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>
  </defs>

  <style>
    @keyframes pulseData {
      0% { stroke-dashoffset: 240; opacity: 0.4; }
      50% { opacity: 1; }
      100% { stroke-dashoffset: 0; opacity: 0.4; }
    }
    @keyframes ringRotate {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    @keyframes ledBlink {
      0%, 100% { opacity: 1; filter: drop-shadow(0 0 6px #ef4444); }
      50% { opacity: 0.88; filter: drop-shadow(0 0 3px #ef4444); }
    }
    @keyframes packetFlow {
      0% { transform: translate(0, 0); opacity: 0; }
      10% { opacity: 1; }
      90% { opacity: 1; }
      100% { transform: translate(750px, 120px); opacity: 0; }
    }
    .pulse-cable {
      stroke-dasharray: 12 18;
      animation: pulseData 4s linear infinite;
    }
    .live-digit {
      font-family: 'JetBrains Mono', monospace;
      animation: ledBlink 3s ease-in-out infinite;
    }
    .rotating-seal {
      transform-origin: center;
      animation: ringRotate 40s linear infinite;
    }
  </style>

  <!-- ========================================================================= -->
  <!-- 0. BASE CANVAS, AMBIENT GLOWS & ISOMETRIC GROUND GRID                      -->
  <!-- ========================================================================= -->
  <rect width="1920" height="1080" fill="#020617"/>
  <rect width="1920" height="1080" fill="url(#ambientLeftGlow)"/>
  <rect width="1920" height="1080" fill="url(#ambientRightGlow)"/>

  <!-- Floor Grid (Isometric Perspective) -->
  <g opacity="0.75">
    <rect y="420" width="1920" height="660" fill="url(#isoGridPattern)"/>
  </g>

  <!-- Background Center Vignette (Ensures Login Card readability) -->
  <ellipse cx="960" cy="540" rx="520" ry="460" fill="#020617" opacity="0.82" filter="blur(40px)"/>

  <!-- ========================================================================= -->
  <!-- TOP STATUS BAR: SOVEREIGN LEGAL METROLOGY GRID (OIML R-76.1)              -->
  <!-- ========================================================================= -->
  <g id="top-bar">
    <rect x="0" y="0" width="1920" height="48" fill="#030712" opacity="0.95"/>
    <line x1="0" y1="48" x2="1920" y2="48" stroke="#1e293b" stroke-width="1.5"/>

    <!-- Left Badge: National Legal Metrology -->
    <g transform="translate(40, 14)">
      <circle cx="10" cy="10" r="7" fill="#f59e0b" opacity="0.2"/>
      <circle cx="10" cy="10" r="3.5" fill="#f59e0b"/>
      <text x="26" y="14" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800" fill="#f8fafc" letter-spacing="1">INDIA LEGAL METROLOGY SOVEREIGN GRID</text>
      <text x="360" y="14" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="600" fill="#38bdf8">• OIML R-76.1 NON-AUTOMATIC WEIGHING INSTRUMENT REGIME</text>
    </g>

    <!-- Right Live Telemetry Tickers -->
    <g transform="translate(1380, 14)">
      <rect x="0" y="0" width="110" height="20" rx="4" fill="#064e3b" stroke="#10b981" stroke-width="1"/>
      <text x="55" y="14" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="800" fill="#34d399" text-anchor="middle">ONLINE 99.98%</text>

      <text x="130" y="14" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="600" fill="#94a3b8">NODES: <tspan fill="#38bdf8" font-weight="800">14,820</tspan></text>
      <text x="260" y="14" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="600" fill="#94a3b8">SIH CODE: <tspan fill="#f59e0b" font-weight="800">SIH26035</tspan></text>
      <text x="400" y="14" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="600" fill="#94a3b8">VERSION: <tspan fill="#c084fc" font-weight="800">v4.2-PROD</tspan></text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- LEFT ZONE (x: 50 to 620): THE REAL COMMERCIAL MANDI NAWI SCALE            -->
  <!-- ========================================================================= -->
  <g id="nawi-scale-cluster">
    <!-- Zone Header Tag -->
    <g transform="translate(70, 75)">
      <rect x="0" y="0" width="360" height="28" rx="6" fill="#0f172a" stroke="#f59e0b" stroke-width="1.2"/>
      <circle cx="16" cy="14" r="5" fill="#f59e0b"/>
      <text x="32" y="18" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800" fill="#fbbf24">PHYSICAL NAWI: COMMERCIAL PLATFORM SCALE</text>
      <text x="0" y="44" font-family="'Inter', sans-serif" font-size="11" fill="#94a3b8">APMC Mandi • Class III Standard (Max 150 kg, e = 50 g)</text>
    </g>

    <!-- Ground Ambient Shadow under Scale -->
    <ellipse cx="320" cy="800" rx="260" ry="85" fill="#000000" opacity="0.65" filter="url(#shadowBlur)"/>

    <!-- 1. Scale Foundation: Corner Leveling Rubber Feet -->
    <g id="scale-feet">
      <ellipse cx="140" cy="740" rx="18" ry="8" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
      <ellipse cx="490" cy="740" rx="18" ry="8" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>
      <ellipse cx="260" cy="840" rx="22" ry="9" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
      <ellipse cx="370" cy="840" rx="22" ry="9" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
    </g>

    <!-- 2. Cast Iron / Fabricated Steel Base Frame (Isometric) -->
    <!-- Front Face -->
    <polygon points="120,700 320,790 520,700 520,730 320,820 120,730" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
    <!-- Left Lower Side -->
    <polygon points="120,700 320,790 320,820 120,730" fill="#0a0f1d" stroke="#1e293b" stroke-width="1.5"/>
    <!-- Right Lower Side -->
    <polygon points="320,790 520,700 520,730 320,820" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>

    <!-- 3. Cutaway Window showing Internal Single-Point Load Cell & Strain Gauge -->
    <g id="load-cell-cutaway" transform="translate(230, 715)">
      <!-- Cutaway Aperture -->
      <polygon points="40,25 150,-20 150,55 40,100" fill="#020617" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3 3"/>
      <!-- S-Type / Bending Beam Aluminum Load Cell Block -->
      <polygon points="65,40 125,12 125,50 65,78" fill="#475569" stroke="#94a3b8" stroke-width="1.2"/>
      <circle cx="95" cy="45" r="9" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
      <circle cx="95" cy="45" r="4" fill="#38bdf8"/>
      <!-- Strain Gauge Bridge Wires -->
      <path d="M 95,45 C 115,55 130,40 145,52" fill="none" stroke="#ef4444" stroke-width="1.8"/>
      <path d="M 95,45 C 115,65 130,50 145,62" fill="none" stroke="#10b981" stroke-width="1.8"/>
      <!-- Load Cell Label Callout -->
      <rect x="2" y="85" width="130" height="20" rx="3" fill="#082f49" stroke="#0ea5e9" stroke-width="1"/>
      <text x="67" y="98" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#38bdf8" text-anchor="middle">IP67 STRAIN GAUGE</text>
    </g>

    <!-- 4. Heavy Stainless Steel Top Platter (Diamond Plate Anti-Slip Pan) -->
    <!-- Upper Isometric Platter Top -->
    <polygon points="100,680 320,580 540,680 320,780" fill="url(#steelPanGrad)" stroke="#64748b" stroke-width="2.5"/>
    <polygon points="100,680 320,580 540,680 320,780" fill="url(#treadPattern)"/>
    <!-- Platter Front Beveled Skirt -->
    <polygon points="100,680 320,780 320,795 100,695" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <polygon points="320,780 540,680 540,695 320,795" fill="#334155" stroke="#475569" stroke-width="1.5"/>
    <!-- Platter Top Highlight Sheen -->
    <line x1="102" y1="680" x2="320" y2="780" stroke="#94a3b8" stroke-width="1.5" opacity="0.6"/>

    <!-- 5. L-Shaped Chrome Safety Backrest Rail (Where Mandi Sacks Lean) -->
    <g id="scale-backrail">
      <!-- Left Vertical Stanchion -->
      <path d="M 170,640 L 170,470" stroke="#334155" stroke-width="14" stroke-linecap="round"/>
      <path d="M 170,640 L 170,470" stroke="#f1f5f9" stroke-width="4" stroke-linecap="round"/>
      <!-- Right Vertical Stanchion -->
      <path d="M 450,640 L 450,470" stroke="#334155" stroke-width="14" stroke-linecap="round"/>
      <path d="M 450,640 L 450,470" stroke="#f1f5f9" stroke-width="4" stroke-linecap="round"/>
      <!-- Top Horizontal Heavy Cross Rail -->
      <path d="M 170,470 L 450,470" stroke="#475569" stroke-width="14" stroke-linecap="round"/>
      <path d="M 170,470 L 450,470" stroke="#cbd5e1" stroke-width="4" stroke-linecap="round"/>
      <!-- Mid Reinforcement Crossbar -->
      <path d="M 170,530 L 450,530" stroke="#1e293b" stroke-width="8" stroke-linecap="round"/>
      <path d="M 170,530 L 450,530" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
    </g>

    <!-- 6. Real Mandi Load: 50 kg Burlap / Jute Grain Sack on the Pan -->
    <g id="grain-sack" transform="translate(320, 660)">
      <!-- Sack Cast Shadow on Platter -->
      <ellipse cx="0" cy="35" rx="100" ry="38" fill="#000000" opacity="0.5" filter="blur(5px)"/>
      <!-- Burlap Sack Body (Fat Oval/Bulge) -->
      <path d="M -90,-25 Q 0,-55 90,-25 Q 115,25 80,50 Q 0,75 -80,50 Q -115,25 -90,-25 Z" fill="#d97706" stroke="#92400e" stroke-width="3"/>
      <!-- Jute Fabric Texture Wrinkles & Seams -->
      <path d="M -75,0 Q 0,-25 75,0" fill="none" stroke="#b45309" stroke-width="2.5"/>
      <path d="M -80,25 Q 0,0 80,25" fill="none" stroke="#b45309" stroke-width="2.5"/>
      <path d="M -40,-35 Q -30,20 -40,55" fill="none" stroke="#78350f" stroke-width="1.8" stroke-dasharray="4 2"/>
      <path d="M 40,-35 Q 30,20 40,55" fill="none" stroke="#78350f" stroke-width="1.8" stroke-dasharray="4 2"/>
      <!-- Tied Top Neck with Twine String -->
      <ellipse cx="0" cy="-35" rx="34" ry="14" fill="#b45309" stroke="#78350f" stroke-width="2.5"/>
      <ellipse cx="0" cy="-46" rx="24" ry="10" fill="#f59e0b" stroke="#b45309" stroke-width="2.5"/>
      <!-- Authentic Stenciled Ink Stamp on Grain Sack -->
      <rect x="-65" y="-5" width="130" height="34" rx="4" fill="#78350f" opacity="0.9"/>
      <text x="0" y="14" font-family="'JetBrains Mono', monospace" font-size="13" font-weight="900" fill="#fef3c7" text-anchor="middle" letter-spacing="1">50 kg WHEAT</text>
      <text x="0" y="24" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="700" fill="#fbbf24" text-anchor="middle">APMC MANDI • OIML CLASS III</text>
    </g>

    <!-- 7. Tall Upright Chrome Pole / Column Rising from Rear Right Corner -->
    <g id="indicator-pole">
      <!-- Pole Base Socket Bracket -->
      <ellipse cx="490" cy="620" rx="24" ry="12" fill="#0f172a" stroke="#334155" stroke-width="2"/>
      <!-- Vertical Round Steel Pipe (Height ~380px) -->
      <rect x="480" y="220" width="20" height="400" fill="url(#chromeGrad)" stroke="#1e293b" stroke-width="1.5"/>
      <!-- Cable Clip Fasteners along the pole -->
      <rect x="477" y="280" width="26" height="6" rx="2" fill="#0f172a" stroke="#475569" stroke-width="1"/>
      <rect x="477" y="380" width="26" height="6" rx="2" fill="#0f172a" stroke="#475569" stroke-width="1"/>
      <rect x="477" y="480" width="26" height="6" rx="2" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    </g>

    <!-- 8. Commercial Digital Indicator Head (Mounted on top of pole, clear of login card) -->
    <g id="indicator-head" transform="translate(370, 95)">
      <!-- Swivel Mounting Arm Bracket -->
      <rect x="110" y="115" width="20" height="30" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
      <circle cx="120" cy="125" r="7" fill="#94a3b8" stroke="#0f172a" stroke-width="1"/>

      <!-- Industrial Die-Cast Enclosure (Angled Front Bezel with Top Sun Visor Hood) -->
      <polygon points="10,20 230,20 240,115 0,115" fill="#0f172a" stroke="#334155" stroke-width="2.5"/>
      <!-- Sun Visor Overhang Hood -->
      <polygon points="5,15 235,15 230,20 10,20" fill="#1e293b" stroke="#475569" stroke-width="1"/>

      <!-- Front Bezel Recess -->
      <rect x="12" y="24" width="216" height="84" rx="6" fill="#020617" stroke="#1e293b" stroke-width="2"/>

      <!-- 7-Segment High-Intensity RED LED Digital Display Window -->
      <rect x="22" y="30" width="196" height="44" rx="4" fill="#180408" stroke="#ef4444" stroke-width="1.5"/>

      <!-- The Unmistakable Glowing Red Digits: 50.00 kg -->
      <text x="206" y="63" class="live-digit" font-size="30" font-weight="900" fill="#ef4444" filter="url(#ledBloom)" text-anchor="end" letter-spacing="2">50.00</text>
      <text x="210" y="63" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="900" fill="#ef4444" filter="url(#ledBloom)">kg</text>

      <!-- Annunciator Status Lamps under LED Display -->
      <!-- STABLE LED -->
      <circle cx="35" cy="85" r="3" fill="#10b981" filter="url(#ledBloom)"/>
      <text x="43" y="88" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#a7f3d0">STABLE</text>
      <!-- ZERO LED -->
      <circle cx="95" cy="85" r="3" fill="#10b981" filter="url(#ledBloom)"/>
      <text x="103" y="88" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#a7f3d0">ZERO</text>
      <!-- NET LED -->
      <circle cx="150" cy="85" r="3" fill="#38bdf8"/>
      <text x="158" y="88" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#7dd3fc">NET</text>

      <!-- Front Tactile Membrane Keypad -->
      <g transform="translate(22, 94)">
        <rect x="0" y="0" width="44" height="15" rx="3" fill="#1e293b" stroke="#475569" stroke-width="1"/>
        <text x="22" y="11" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#cbd5e1" text-anchor="middle">ZERO</text>

        <rect x="50" y="0" width="44" height="15" rx="3" fill="#1e293b" stroke="#475569" stroke-width="1"/>
        <text x="72" y="11" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#cbd5e1" text-anchor="middle">TARE</text>

        <rect x="100" y="0" width="44" height="15" rx="3" fill="#1e293b" stroke="#475569" stroke-width="1"/>
        <text x="122" y="11" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#cbd5e1" text-anchor="middle">PRINT</text>

        <rect x="150" y="0" width="44" height="15" rx="3" fill="#0284c7" stroke="#38bdf8" stroke-width="1"/>
        <text x="172" y="11" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="800" fill="#ffffff" text-anchor="middle">SEND</text>
      </g>

      <!-- Government Stamped Gazette Lead Verification Seal hanging from wire -->
      <line x1="228" y1="110" x2="228" y2="135" stroke="#94a3b8" stroke-width="1.5"/>
      <circle cx="228" cy="142" r="7" fill="url(#goldSealGrad)" stroke="#78350f" stroke-width="1"/>
      <text x="228" y="145" font-family="'JetBrains Mono', monospace" font-size="5" font-weight="900" fill="#000000" text-anchor="middle">GOV</text>
    </g>

    <!-- Scale Verification Badge Callout -->
    <g transform="translate(100, 890)">
      <rect x="0" y="0" width="440" height="42" rx="8" fill="#090f1d" stroke="#0284c7" stroke-width="1.5"/>
      <text x="20" y="20" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="900" fill="#38bdf8">NAWI MODEL: IND-MANDI-150K</text>
      <text x="20" y="33" font-family="'Inter', sans-serif" font-size="9" fill="#94a3b8">Division: e = 50g • Min: 1 kg • Max: 150 kg • MPE Class: Class III</text>
      <rect x="340" y="10" width="85" height="22" rx="4" fill="#064e3b" stroke="#10b981" stroke-width="1"/>
      <text x="382" y="24" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="800" fill="#34d399" text-anchor="middle">VERIFIED</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- TELEMETRY HIGHWAY CONDUIT (Passing Underneath/Behind the Center Card)     -->
  <!-- ========================================================================= -->
  <g id="telemetry-highway">
    <!-- Main Heavy Industrial Shielded Serial Cable -->
    <path d="M 600,210 C 720,240 760,860 1140,860 C 1300,860 1340,640 1420,540" fill="none" stroke="#0b1329" stroke-width="14" stroke-linecap="round"/>
    <path d="M 600,210 C 720,240 760,860 1140,860 C 1300,860 1340,640 1420,540" fill="none" stroke="#0369a1" stroke-width="6" stroke-linecap="round"/>
    
    <!-- Animated Glowing Fiber-Optic Telemetry Pulses -->
    <path class="pulse-cable" d="M 600,210 C 720,240 760,860 1140,860 C 1300,860 1340,640 1420,540" fill="none" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" filter="url(#cyanGlow)"/>

    <!-- DB9 Industrial Serial Connector on Scale Output -->
    <rect x="590" y="200" width="20" height="20" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
    <text x="590" y="194" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="800" fill="#38bdf8">RS-232 / USB</text>

    <!-- Ground Circuit Traces linking Left & Right -->
    <path d="M 520,760 L 720,860 L 1200,860 L 1400,760" fill="none" stroke="#0ea5e9" stroke-width="1.2" stroke-dasharray="6 8" opacity="0.4"/>
    <circle cx="720" cy="860" r="3" fill="#38bdf8"/>
    <circle cx="1200" cy="860" r="3" fill="#38bdf8"/>
  </g>

  <!-- ========================================================================= -->
  <!-- RIGHT ZONE (x: 1320 to 1880): PRECISIONX SOVEREIGN ENGINE (THE SOLUTION)   -->
  <!-- ========================================================================= -->
  <g id="precisionx-sovereign-engine">
    <!-- Zone Header Tag -->
    <g transform="translate(1420, 75)">
      <rect x="0" y="0" width="420" height="28" rx="6" fill="#0f172a" stroke="#06b6d4" stroke-width="1.2"/>
      <circle cx="16" cy="14" r="5" fill="#06b6d4"/>
      <text x="32" y="18" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="800" fill="#22d3ee">SOVEREIGN CORE: STATUTORY ENGINE & DCC VAULT</text>
      <text x="0" y="44" font-family="'Inter', sans-serif" font-size="11" fill="#94a3b8">Real-Time OIML R-76 MPE Checker • RFC 8032 Cryptography</text>
    </g>

    <!-- Ground Ambient Shadow under Server Rack -->
    <ellipse cx="1620" cy="820" rx="220" ry="75" fill="#000000" opacity="0.65" filter="url(#shadowBlur)"/>

    <!-- 1. PrecisionX Rugged Field Inspection Server Chassis (Isometric) -->
    <!-- Server Main Isometric Cube -->
    <!-- Left Face -->
    <polygon points="1440,540 1600,630 1600,820 1440,730" fill="#090f1d" stroke="#1e293b" stroke-width="2"/>
    <!-- Right Face -->
    <polygon points="1600,630 1800,530 1800,720 1600,820" fill="#0f172a" stroke="#334155" stroke-width="2"/>
    <!-- Top Face -->
    <polygon points="1440,540 1640,440 1800,530 1600,630" fill="#111c35" stroke="#0284c7" stroke-width="2.5"/>

    <!-- Glowing Blue Cooling Louvers on Server Sides -->
    <g stroke="#0284c7" stroke-width="2" opacity="0.8">
      <line x1="1460" y1="590" x2="1580" y2="655"/>
      <line x1="1460" y1="620" x2="1580" y2="685"/>
      <line x1="1460" y1="650" x2="1580" y2="715"/>
      <line x1="1460" y1="680" x2="1580" y2="745"/>
    </g>

    <!-- 2. Holographic HUD Floating Above Server Rack (Angled towards user) -->
    <g transform="translate(1380, 160)">
      <!-- Glassmorphic Hologram Frame -->
      <rect x="0" y="0" width="470" height="360" rx="12" fill="#030816" stroke="#0ea5e9" stroke-width="1.8" opacity="0.94" filter="url(#cyanGlow)"/>

      <!-- Hologram Header -->
      <g transform="translate(20, 24)">
        <circle cx="8" cy="8" r="4" fill="#10b981"/>
        <text x="20" y="12" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="900" fill="#f8fafc">PRECISIONX MPE VERIFICATION ENGINE</text>
        <text x="20" y="25" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="#38bdf8">OIML R-76-1:2006 (E) TABLE 6 ALGORITHM</text>
      </g>

      <!-- Live Settlement Waveform Curve (Shows Zero-Point Stability) -->
      <g transform="translate(20, 60)">
        <rect x="0" y="0" width="430" height="60" rx="6" fill="#020617" stroke="#1e293b" stroke-width="1"/>
        <!-- Grid lines inside curve -->
        <line x1="0" y1="30" x2="430" y2="30" stroke="#1e293b" stroke-width="1" stroke-dasharray="4 4"/>
        <!-- Damped Sine Wave settling to perfect 50.00kg flat line -->
        <path d="M 10,48 Q 40,5 70,45 T 130,22 T 180,34 T 230,28 T 280,30 L 420,30" fill="none" stroke="#38bdf8" stroke-width="2"/>
        <circle cx="420" cy="30" r="4" fill="#10b981" filter="url(#ledBloom)"/>
        <text x="12" y="16" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="800" fill="#94a3b8">RAW TELEMETRY: 100 Hz FILTERED [STABLE IN 1.2s]</text>
        <text x="350" y="24" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="900" fill="#10b981">STABLE ✅</text>
      </g>

      <!-- Statutory OIML Tolerance Calculation Card -->
      <g transform="translate(20, 130)">
        <rect x="0" y="0" width="430" height="92" rx="8" fill="#022c22" stroke="#10b981" stroke-width="1.5"/>

        <text x="18" y="22" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="900" fill="#34d399">CLASS III MPE FORMULA CHECK</text>
        
        <text x="18" y="42" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="600" fill="#e2e8f0">Load Range (m): <tspan fill="#fbbf24" font-weight="800">500 e &lt; m ≤ 2000 e (25 kg to 100 kg)</tspan></text>
        <text x="18" y="58" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="600" fill="#e2e8f0">Statutory MPE Limit: <tspan fill="#34d399" font-weight="900">± 1.0 e (± 50.00 g)</tspan></text>
        
        <!-- Live Result Pill -->
        <rect x="18" y="66" width="394" height="20" rx="4" fill="#064e3b" stroke="#34d399" stroke-width="1"/>
        <text x="28" y="80" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="900" fill="#a7f3d0">OBSERVED ERROR: Δ = +12.0 g (0.24 e) ➔ PASS (WITHIN LEGAL MPE)</text>
      </g>

      <!-- Digital Calibration Certificate (PTB DCC XML) & Cryptographic Signature Box -->
      <g transform="translate(20, 230)">
        <rect x="0" y="0" width="430" height="60" rx="8" fill="#180b2c" stroke="#a855f7" stroke-width="1.5"/>
        
        <!-- Rotating Holographic Seal Icon -->
        <circle cx="28" cy="30" r="16" fill="none" stroke="#c084fc" stroke-width="1.5" stroke-dasharray="4 3" class="rotating-seal"/>
        <circle cx="28" cy="30" r="10" fill="#581c87"/>
        <text x="28" y="34" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="900" fill="#f3e8ff" text-anchor="middle">DCC</text>

        <text x="54" y="22" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" fill="#e9d5ff">ISO 19005-3 PDF/A-3 + DCC XML ARCHIVE</text>
        <text x="54" y="36" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="#c084fc">RFC 8032 Ed25519 Signature: <tspan fill="#f3e8ff">7d9f...b420</tspan></text>
        <text x="54" y="48" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="600" fill="#a855f7">SHA-256 Anti-Rollback Hash: 3c8e41a...d910 (Tamper-Evident)</text>
      </g>

      <!-- Offline QR Verification Seal Button -->
      <g transform="translate(20, 300)">
        <rect x="0" y="0" width="430" height="42" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1.2"/>
        <!-- Mini QR Matrix Graphic -->
        <rect x="12" y="7" width="28" height="28" fill="#38bdf8" rx="2"/>
        <rect x="15" y="10" width="8" height="8" fill="#020617"/>
        <rect x="29" y="10" width="8" height="8" fill="#020617"/>
        <rect x="15" y="24" width="8" height="8" fill="#020617"/>
        
        <text x="50" y="22" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" fill="#f8fafc">PUBLIC QR SEAL: INSTANT OFFLINE CITIZEN VERIFICATION</text>
        <text x="50" y="34" font-family="'Inter', sans-serif" font-size="8.5" fill="#94a3b8">Scan with standard smartphone camera to verify weights &amp; measures authenticity</text>
      </g>
    </g>

    <!-- Terminal Status Badge -->
    <g transform="translate(1420, 890)">
      <rect x="0" y="0" width="420" height="42" rx="8" fill="#090f1d" stroke="#10b981" stroke-width="1.5"/>
      <text x="20" y="20" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="900" fill="#34d399">ZERO-WAIT DIRECT CAPTURE: COMPLETED</text>
      <text x="20" y="33" font-family="'Inter', sans-serif" font-size="9" fill="#94a3b8">Manual Waiting Latency: 0.00s • Transcribing Errors: 0% • Anti-Tamper: 100%</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 4. BOTTOM 4-STEP SOVEREIGN ARCHITECTURAL WORKFLOW RIBBON                 -->
  <!-- ========================================================================= -->
  <g id="bottom-architecture-ribbon" transform="translate(40, 970)">
    <!-- Master Background Plate -->
    <rect x="0" y="0" width="1840" height="85" rx="10" fill="#030712" stroke="#1e293b" stroke-width="1.5"/>

    <!-- Step 1 -->
    <g transform="translate(25, 14)">
      <rect x="0" y="0" width="400" height="58" rx="6" fill="#0b1329" stroke="#f59e0b" stroke-width="1.2"/>
      <circle cx="24" cy="20" r="10" fill="#f59e0b"/>
      <text x="24" y="24" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" fill="#000000" text-anchor="middle">1</text>
      <text x="44" y="22" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="900" fill="#fbbf24">PHYSICAL NAWI PLATFORM</text>
      <text x="44" y="38" font-family="'Inter', sans-serif" font-size="9.5" fill="#94a3b8">Operator places load (e.g. 50kg grain sack) on Mandi scale.</text>
      <text x="44" y="49" font-family="'Inter', sans-serif" font-size="9.5" fill="#64748b">Internal IP67 strain gauge generates analog micro-volt signal.</text>
    </g>

    <!-- Arrow 1 to 2 -->
    <path d="M 435,43 L 460,43" stroke="#0ea5e9" stroke-width="2.5" marker-end="url(#cyanArrow)"/>

    <!-- Step 2 -->
    <g transform="translate(475, 14)">
      <rect x="0" y="0" width="410" height="58" rx="6" fill="#0b1329" stroke="#0284c7" stroke-width="1.2"/>
      <circle cx="24" cy="20" r="10" fill="#0284c7"/>
      <text x="24" y="24" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle">2</text>
      <text x="44" y="22" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="900" fill="#38bdf8">DIRECT RS-232 TELEMETRY</text>
      <text x="44" y="38" font-family="'Inter', sans-serif" font-size="9.5" fill="#94a3b8">Zero-wait raw serial stream intercepted via hardware bridge.</text>
      <text x="44" y="49" font-family="'Inter', sans-serif" font-size="9.5" fill="#64748b">Eliminates human delay, manual recording, and display tampering.</text>
    </g>

    <!-- Arrow 2 to 3 -->
    <path d="M 895,43 L 920,43" stroke="#10b981" stroke-width="2.5"/>

    <!-- Step 3 -->
    <g transform="translate(935, 14)">
      <rect x="0" y="0" width="420" height="58" rx="6" fill="#0b1329" stroke="#10b981" stroke-width="1.2"/>
      <circle cx="24" cy="20" r="10" fill="#10b981"/>
      <text x="24" y="24" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" fill="#000000" text-anchor="middle">3</text>
      <text x="44" y="22" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="900" fill="#34d399">OIML R-76 MPE MATH ENGINE</text>
      <text x="44" y="38" font-family="'Inter', sans-serif" font-size="9.5" fill="#94a3b8">Calculates Table 6 MPE limits (±0.5e, ±1.0e, ±1.5e) dynamically.</text>
      <text x="44" y="49" font-family="'Inter', sans-serif" font-size="9.5" fill="#64748b">Flags eccentric loading bias, tare abuse, and zero-point drift.</text>
    </g>

    <!-- Arrow 3 to 4 -->
    <path d="M 1365,43 L 1390,43" stroke="#a855f7" stroke-width="2.5"/>

    <!-- Step 4 -->
    <g transform="translate(1405, 14)">
      <rect x="0" y="0" width="410" height="58" rx="6" fill="#0b1329" stroke="#a855f7" stroke-width="1.2"/>
      <circle cx="24" cy="20" r="10" fill="#a855f7"/>
      <text x="24" y="24" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" fill="#ffffff" text-anchor="middle">4</text>
      <text x="44" y="22" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="900" fill="#c084fc">CRYPTOGRAPHIC PROOF &amp; DCC</text>
      <text x="44" y="38" font-family="'Inter', sans-serif" font-size="9.5" fill="#94a3b8">Signs with RFC 8032 Ed25519 &amp; PTB DCC XML into ISO PDF/A-3.</text>
      <text x="44" y="49" font-family="'Inter', sans-serif" font-size="9.5" fill="#64748b">Generates tamper-evident offline QR verification certificate.</text>
    </g>
  </g>
</svg>
`;

const outputPath = "/home/zeno/Desktop/SIH_NAWI_Login_Background.svg";
writeFileSync(outputPath, masterNawiSvg);
console.log("Successfully generated Master NAWI Explainer SVG:", outputPath);
