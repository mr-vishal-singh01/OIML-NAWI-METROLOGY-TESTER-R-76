import { writeFileSync } from "node:fs";

// 1920x1080 Viewport
const WIDTH = 1920;
const HEIGHT = 1080;

// High-craft SVG of an instantly recognizable commercial Mandi Platform Scale (NAWI)
// With:
// 1. Heavy low-profile platform with diamond plate
// 2. Vertical tubular chrome column/pole
// 3. Digital indicator terminal head with bright red 7-segment LED display & annunciator lights
// 4. L-shaped tubular safety backrail (where sacks lean)
// 5. Real 50 kg stitched jute grain sack sitting on the platform
// 6. Direct RS-232 serial telemetry cable streaming data pulses
// 7. PrecisionX Sovereign Metrology Inspector Tablet/Terminal on the bench validating OIML R-76
const realNawiSvg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="background:#030712; display:block;">
  <defs>
    <!-- Background Ambient Glow -->
    <radialGradient id="nawiCenterGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.16"/>
      <stop offset="55%" stop-color="#030712" stop-opacity="0.65"/>
      <stop offset="100%" stop-color="#030712" stop-opacity="0.98"/>
    </radialGradient>

    <!-- Diamond Plate Tread Pattern for Stainless Platter -->
    <pattern id="treadPattern" width="14" height="14" patternUnits="userSpaceOnUse">
      <path d="M 7 0 L 14 7 L 7 14 L 0 7 Z" fill="none" stroke="rgba(255,255,255,0.09)" stroke-width="0.8"/>
    </pattern>

    <!-- Chrome / Steel Gradient for Indicator Pole -->
    <linearGradient id="chromeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="35%" stop-color="#94a3b8"/>
      <stop offset="60%" stop-color="#f1f5f9"/>
      <stop offset="85%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>

    <!-- Red LED Glow Filter -->
    <filter id="ledGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Cyan Pulse Glow Filter -->
    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    @keyframes cablePulseAnim {
      from { stroke-dashoffset: 0; }
      to { stroke-dashoffset: -36px; }
    }
    .data-pulse {
      animation: cablePulseAnim 0.75s linear infinite;
    }
    .led-digit {
      font-family: 'Courier New', Courier, monospace;
      font-weight: 900;
      letter-spacing: 2px;
    }
  </style>

  <!-- Deep Navy Blueprint Backdrop -->
  <rect width="1920" height="1080" fill="#030712"/>
  <rect width="1920" height="1080" fill="url(#nawiCenterGlow)"/>

  <!-- Perspective Floor Grid (Isometric Metrology Hall) -->
  <g opacity="0.14">
    <ellipse cx="960" cy="620" rx="720" ry="280" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="4 8"/>
    <ellipse cx="960" cy="620" rx="480" ry="190" fill="none" stroke="#38bdf8" stroke-width="1" stroke-dasharray="2 6"/>
    <!-- Floor Ray Lines -->
    <line x1="240" y1="620" x2="1680" y2="620" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="4 8"/>
    <line x1="960" y1="200" x2="960" y2="980" stroke="#38bdf8" stroke-width="0.8" stroke-dasharray="4 8"/>
  </g>

  <!-- Ground Drop Shadow under Scale & Terminal -->
  <ellipse cx="580" cy="740" rx="340" ry="120" fill="#000000" opacity="0.6" filter="blur(18px)"/>
  <ellipse cx="1320" cy="680" rx="220" ry="80" fill="#000000" opacity="0.5" filter="blur(14px)"/>

  <!-- ========================================================================= -->
  <!-- 1. LEFT SIDE: THE RECOGNIZABLE COMMERCIAL MANDI WEIGHING SCALE (NAWI)      -->
  <!-- ========================================================================= -->
  <g id="nawi-scale-complete">

    <!-- A. Four Heavy Steel Leveling Feet -->
    <ellipse cx="320" cy="710" rx="26" ry="11" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
    <ellipse cx="820" cy="710" rx="26" ry="11" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
    <ellipse cx="570" cy="830" rx="30" ry="13" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
    <ellipse cx="570" cy="590" rx="30" ry="13" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>

    <!-- B. Lower Platform Sub-Chassis (Fabricated Heavy Mild Steel) -->
    <!-- Base Thickness Side Walls -->
    <polygon points="280,680 570,810 570,845 280,715" fill="#1e293b" stroke="#334155" stroke-width="1.2"/>
    <polygon points="570,810 860,680 860,715 570,845" fill="#0f172a" stroke="#334155" stroke-width="1.2"/>
    <!-- Sub-Chassis Top Bed -->
    <polygon points="570,550 860,680 570,810 280,680" fill="#1e293b" stroke="#475569" stroke-width="1.5"/>

    <!-- Inside Cutaway: Shear Beam Load Cell & Sensor Wiring (visible under gap) -->
    <polygon points="530,660 610,696 610,720 530,684" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
    <rect x="560" y="682" width="18" height="8" fill="#f59e0b" rx="1"/>
    <path d="M 610,705 Q 640,730 670,710" fill="none" stroke="#ef4444" stroke-width="2"/>
    <path d="M 610,709 Q 640,734 670,714" fill="none" stroke="#38bdf8" stroke-width="2"/>

    <!-- C. Suspended Stainless Steel Weighing Pan (Diamond Plate Tread) -->
    <g id="weighing-pan">
      <!-- 4 Corner Damping Springs -->
      <path d="M 330 665 L 330 635" stroke="#94a3b8" stroke-width="4"/>
      <path d="M 810 665 L 810 635" stroke="#94a3b8" stroke-width="4"/>
      <path d="M 570 790 L 570 760" stroke="#94a3b8" stroke-width="4"/>
      <path d="M 570 565 L 570 535" stroke="#94a3b8" stroke-width="4"/>

      <!-- Platter Rim Depth (Beveled Sheet Metal) -->
      <polygon points="260,635 570,770 570,788 260,653" fill="#475569" stroke="#64748b" stroke-width="1.2"/>
      <polygon points="570,770 880,635 880,653 570,788" fill="#334155" stroke="#64748b" stroke-width="1.2"/>
      <!-- Top Stainless Pan Deck -->
      <polygon points="570,500 880,635 570,770 260,635" fill="#475569" stroke="#cbd5e1" stroke-width="2"/>
      <polygon points="570,500 880,635 570,770 260,635" fill="url(#treadPattern)"/>

      <!-- 5 OIML R-76 Marked Test Points (Center, Q1, Q2, Q3, Q4) -->
      <ellipse cx="570" cy="635" rx="20" ry="9" fill="none" stroke="#38bdf8" stroke-width="1.8"/>
      <circle cx="570" cy="635" r="3.5" fill="#38bdf8"/>
      <text x="570" y="650" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="700" fill="#38bdf8" text-anchor="middle">CENTER (0)</text>

      <ellipse cx="400" cy="640" rx="14" ry="6" fill="none" stroke="#64748b" stroke-width="1.2"/>
      <text x="400" y="652" font-family="'JetBrains Mono', monospace" font-size="8" fill="#94a3b8" text-anchor="middle">Q1</text>
      <ellipse cx="740" cy="640" rx="14" ry="6" fill="none" stroke="#64748b" stroke-width="1.2"/>
      <text x="740" y="652" font-family="'JetBrains Mono', monospace" font-size="8" fill="#94a3b8" text-anchor="middle">Q2</text>
      <ellipse cx="740" cy="580" rx="14" ry="6" fill="none" stroke="#64748b" stroke-width="1.2"/>
      <text x="740" y="592" font-family="'JetBrains Mono', monospace" font-size="8" fill="#94a3b8" text-anchor="middle">Q3</text>
      <ellipse cx="400" cy="580" rx="14" ry="6" fill="none" stroke="#64748b" stroke-width="1.2"/>
      <text x="400" y="592" font-family="'JetBrains Mono', monospace" font-size="8" fill="#94a3b8" text-anchor="middle">Q4</text>

      <!-- Spirit Level Bubble (Corner) -->
      <circle cx="290" cy="640" r="10" fill="#020617" stroke="#64748b" stroke-width="1.5"/>
      <circle cx="290" cy="640" r="4" fill="#10b981" opacity="0.8"/>
    </g>

    <!-- D. Tubular Steel Backrest Guard Rail (The iconic L-rail behind platform) -->
    <g id="scale-backrail">
      <!-- Left Back Upright Tube -->
      <path d="M 400 560 L 400 420" stroke="#94a3b8" stroke-width="12" stroke-linecap="round"/>
      <path d="M 400 560 L 400 420" stroke="#f1f5f9" stroke-width="4" stroke-linecap="round"/>
      <!-- Right Back Upright Tube -->
      <path d="M 740 560 L 740 420" stroke="#94a3b8" stroke-width="12" stroke-linecap="round"/>
      <path d="M 740 560 L 740 420" stroke="#f1f5f9" stroke-width="4" stroke-linecap="round"/>
      <!-- Cross Horizontal Top Rail -->
      <path d="M 400 420 L 740 420" stroke="#64748b" stroke-width="12" stroke-linecap="round"/>
      <path d="M 400 420 L 740 420" stroke="#cbd5e1" stroke-width="4" stroke-linecap="round"/>
      <!-- Middle Reinforcement Bar -->
      <path d="M 400 480 L 740 480" stroke="#475569" stroke-width="8" stroke-linecap="round"/>
    </g>

    <!-- E. Real Test Load: 50 kg Burlap / Jute Grain Mandi Sack -->
    <g id="grain-sack" transform="translate(570, 605)">
      <!-- Jute Sack Bag Shadow -->
      <ellipse cx="0" cy="20" rx="75" ry="32" fill="#000000" opacity="0.4" filter="blur(6px)"/>
      <!-- Sack Bulge Body -->
      <path d="M -65,-30 Q 0,-50 65,-30 Q 85,15 60,35 Q 0,55 -60,35 Q -85,15 -65,-30 Z" fill="#d97706" stroke="#b45309" stroke-width="2.5"/>
      <!-- Shading and Jute Seam Lines -->
      <path d="M -50,-10 Q 0,-30 50,-10" fill="none" stroke="#b45309" stroke-width="2"/>
      <path d="M -55,10 Q 0,-10 55,10" fill="none" stroke="#b45309" stroke-width="2"/>
      <!-- Tied Top Neck with String -->
      <ellipse cx="0" cy="-35" rx="24" ry="10" fill="#b45309" stroke="#78350f" stroke-width="2"/>
      <ellipse cx="0" cy="-44" rx="16" ry="7" fill="#f59e0b" stroke="#b45309" stroke-width="2"/>
      <!-- Stencil Print on Grain Bag -->
      <rect x="-42" y="-5" width="84" height="24" rx="3" fill="#78350f" opacity="0.85"/>
      <text x="0" y="8" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="900" fill="#fef3c7" text-anchor="middle">50 kg WHEAT</text>
      <text x="0" y="16" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="700" fill="#fbbf24" text-anchor="middle">APMC MANDI • OIML CLASS III</text>
    </g>

    <!-- F. Tall Chrome Tubular Pole / Column Rising from Back Right -->
    <g id="indicator-pole">
      <!-- Pole Base Socket Bracket -->
      <ellipse cx="780" cy="540" rx="20" ry="10" fill="#0f172a" stroke="#334155" stroke-width="2"/>
      <!-- Vertical Round Steel Pipe (Height ~280px) -->
      <rect x="772" y="240" width="16" height="300" fill="url(#chromeGrad)" stroke="#1e293b" stroke-width="1.2"/>
    </g>

    <!-- G. The Digital Indicator Terminal Head (Mounted on top of pole) -->
    <g id="indicator-head" transform="translate(680, 130)">
      <!-- Swivel Mounting Arm Bracket -->
      <rect x="94" y="95" width="12" height="25" fill="#334155" stroke="#1e293b" stroke-width="1"/>
      <circle cx="100" cy="100" r="5" fill="#94a3b8"/>

      <!-- Terminal Housing Box (Beveled Heavy Industrial Enclosure with Top Visor) -->
      <polygon points="10,20 190,20 200,95 0,95" fill="#0f172a" stroke="#334155" stroke-width="2"/>
      <!-- Front Bezel Recess -->
      <rect x="12" y="25" width="176" height="65" rx="5" fill="#020617" stroke="#1e293b" stroke-width="1.5"/>

      <!-- 7-Segment High-Contrast RED LED Digital Display Window -->
      <rect x="20" y="32" width="160" height="34" rx="3" fill="#180408" stroke="#ef4444" stroke-width="1.2"/>
      <!-- Bright Red Digital Digits (The unmistakable look of an Indian digital scale) -->
      <text x="170" y="58" class="led-digit" font-size="24" fill="#ef4444" filter="url(#ledGlow)" text-anchor="end">50.00 kg</text>

      <!-- Annunciator Status Dots under display -->
      <!-- Stable Indicator -->
      <circle cx="30" cy="74" r="2.5" fill="#10b981" filter="url(#ledGlow)"/>
      <text x="35" y="76" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="700" fill="#a7f3d0">STABLE</text>
      <!-- Zero Indicator -->
      <circle cx="75" cy="74" r="2.5" fill="#10b981" filter="url(#ledGlow)"/>
      <text x="80" y="76" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="700" fill="#a7f3d0">ZERO</text>
      <!-- Net Indicator -->
      <circle cx="115" cy="74" r="2.5" fill="#38bdf8"/>
      <text x="120" y="76" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="700" fill="#7dd3fc">NET</text>
      <!-- Unit kg -->
      <text x="165" y="76" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="900" fill="#ef4444">kg</text>

      <!-- Push Button Membrane Keypad -->
      <rect x="20" y="98" width="36" height="12" rx="2" fill="#1e293b" stroke="#475569" stroke-width="1"/>
      <text x="38" y="106" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="700" fill="#cbd5e1" text-anchor="middle">ZERO</text>

      <rect x="62" y="98" width="36" height="12" rx="2" fill="#1e293b" stroke="#475569" stroke-width="1"/>
      <text x="80" y="106" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="700" fill="#cbd5e1" text-anchor="middle">TARE</text>

      <rect x="104" y="98" width="36" height="12" rx="2" fill="#1e293b" stroke="#475569" stroke-width="1"/>
      <text x="122" y="106" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="700" fill="#cbd5e1" text-anchor="middle">PRINT</text>

      <rect x="146" y="98" width="34" height="12" rx="2" fill="#1e293b" stroke="#475569" stroke-width="1"/>
      <text x="163" y="106" font-family="'JetBrains Mono', monospace" font-size="6" font-weight="700" fill="#cbd5e1" text-anchor="middle">MODE</text>

      <!-- Government Stamped Gazette Lead Verification Seal hanging from wire -->
      <line x1="188" y1="95" x2="188" y2="120" stroke="#94a3b8" stroke-width="1.2"/>
      <circle cx="188" cy="124" r="5" fill="#f59e0b" stroke="#b45309" stroke-width="1"/>
      <text x="188" y="126" font-family="'JetBrains Mono', monospace" font-size="4" font-weight="900" fill="#000000" text-anchor="middle">GOV</text>
    </g>

    <!-- H. Explanatory Label Badge for Scale -->
    <rect x="380" y="855" width="380" height="34" rx="6" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5"/>
    <text x="570" y="873" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="900" fill="#f59e0b" text-anchor="middle">COMMERCIAL PLATFORM SCALE (NAWI)</text>
    <text x="570" y="884" font-family="'Inter', sans-serif" font-size="8.5" fill="#94a3b8" text-anchor="middle">Class III (e=50g, Max 150kg) • Live Operator Weighing Instrument</text>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. SHIELDED SERIAL RS-232 / USB TELEMETRY INTERFACE CABLE                 -->
  <!-- ========================================================================= -->
  <g id="serial-cable">
    <!-- Heavy shielded black cable running from indicator head down to inspector terminal -->
    <path d="M 875 220 C 980 250, 1050 480, 1180 540" fill="none" stroke="#0f172a" stroke-width="10" stroke-linecap="round"/>
    <path d="M 875 220 C 980 250, 1050 480, 1180 540" fill="none" stroke="#0284c7" stroke-width="5" stroke-linecap="round"/>
    <path class="data-pulse" d="M 875 220 C 980 250, 1050 480, 1180 540" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="8 18" stroke-linecap="round"/>
    
    <!-- DB9 Industrial Serial Connector on Inspector Terminal -->
    <rect x="1170" y="530" width="18" height="22" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
    <!-- Floating Telemetry Stream Badge -->
    <g transform="translate(980, 360)">
      <rect x="0" y="0" width="130" height="28" rx="6" fill="#082f49" stroke="#38bdf8" stroke-width="1.2"/>
      <text x="65" y="14" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="800" fill="#38bdf8" text-anchor="middle">DIRECT RS-232 TELEMETRY</text>
      <text x="65" y="23" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="600" fill="#7dd3fc" text-anchor="middle">100 Hz RAW LOAD CELL STREAM</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. RIGHT SIDE: PRECISIONX SOVEREIGN INSPECTOR TERMINAL (THE SOLUTION)    -->
  <!-- ========================================================================= -->
  <g id="precisionx-inspector-terminal" transform="translate(1180, 440)">
    <!-- Heavy Rugged Metal Station Chassis -->
    <polygon points="140,50 320,130 320,230 140,290 0,210 0,110" fill="#090e1a" stroke="#1e293b" stroke-width="2"/>
    <polygon points="0,210 140,290 140,230 0,150" fill="#0f172a" stroke="#334155" stroke-width="1.2"/>
    <polygon points="140,290 320,230 320,170 140,230" fill="#1e293b" stroke="#475569" stroke-width="1.2"/>
    <!-- Top Slanted Console Deck -->
    <polygon points="140,50 320,130 140,210 0,110" fill="#111d33" stroke="#00f2fe" stroke-width="2"/>

    <!-- High-Resolution Cyber-Metrology VFD/OLED Inspection Screen -->
    <g transform="translate(20, 85)">
      <polygon points="120,0 260,65 120,130 0,55" fill="#020817" stroke="#22d3ee" stroke-width="1.5"/>

      <!-- Header -->
      <text x="125" y="24" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="900" fill="#38bdf8" text-anchor="middle">🇮🇳 PRECISIONX OIML R-76 ENGINE</text>
      <text x="125" y="36" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="700" fill="#94a3b8" text-anchor="middle">LEGAL METROLOGY DIVISION • SIH26035</text>

      <!-- Live Stream Data Line -->
      <rect x="25" y="44" width="200" height="22" rx="3" fill="#082f49" stroke="#0284c7" stroke-width="1"/>
      <text x="125" y="58" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="900" fill="#38bdf8" text-anchor="middle">NET: 50.000 kg • e=50g</text>

      <!-- Statutory OIML R-76 MPE Tolerance Evaluation -->
      <rect x="25" y="70" width="200" height="24" rx="3" fill="#022c22" stroke="#10b981" stroke-width="1.2"/>
      <text x="125" y="82" font-family="'JetBrains Mono', monospace" font-size="8.5" font-weight="900" fill="#34d399" text-anchor="middle">TABLE 6 MPE: ±1.0e (±50 g)</text>
      <text x="125" y="91" font-family="'JetBrains Mono', monospace" font-size="7.5" font-weight="700" fill="#6ee7b7" text-anchor="middle">DEV: Δ = +12.0 g [CERTIFIED PASS]</text>

      <!-- Cryptographic Proof Footer -->
      <text x="125" y="106" font-family="'JetBrains Mono', monospace" font-size="7" font-weight="600" fill="#c084fc" text-anchor="middle">RFC 8032 Ed25519 • PTB DCC XML</text>
      <text x="125" y="116" font-family="'JetBrains Mono', monospace" font-size="6.5" font-weight="700" fill="#10b981" text-anchor="middle">QR VERIFIED • ZERO-WAIT AUTOMATION</text>
    </g>

    <!-- Offline QR Stamp Plaque on Terminal Face -->
    <g transform="translate(18, 222)">
      <rect x="0" y="0" width="280" height="36" rx="6" fill="#0f172a" stroke="#a855f7" stroke-width="1.5"/>
      <text x="140" y="16" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="900" fill="#e9d5ff" text-anchor="middle">SOVEREIGN AUDIT SEAL GENERATED</text>
      <text x="140" y="28" font-family="'JetBrains Mono', monospace" font-size="8" font-weight="600" fill="#a855f7" text-anchor="middle">SHA256: 9e4f2a8c...71b0 • ANTI-TAMPER SECURED</text>
    </g>
  </g>

  <!-- ========================================================================= -->
  <!-- 4. BOTTOM ARCHITECTURAL COMPARISON (WHY PRECISIONX IS THE SOLUTION)       -->
  <!-- ========================================================================= -->
  <g transform="translate(120, 930)">
    <!-- Problem Box -->
    <rect x="0" y="0" width="800" height="110" rx="10" fill="#0f172a" stroke="#f43f5e" stroke-width="1.2" opacity="0.95"/>
    <text x="24" y="28" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="900" fill="#f43f5e">⚠️ TRADITIONAL PROBLEM: WHY MANUAL WEIGHING & WAITING FAILS</text>
    <text x="24" y="52" font-family="'Inter', sans-serif" font-size="10.5" fill="#e2e8f0">• Scale Latency: Inspectors wait for platform oscillation to stop before manually writing numbers on paper.</text>
    <text x="24" y="72" font-family="'Inter', sans-serif" font-size="10.5" fill="#e2e8f0">• Human Miscalculation: Transcribing scale division (e) by hand leads to errors in OIML R-76 MPE limits.</text>
    <text x="24" y="92" font-family="'Inter', sans-serif" font-size="10.5" fill="#e2e8f0">• Tampering: Paper inspection records lack cryptographic audit trails, enabling uncalibrated scales to pass.</text>

    <!-- Solution Box -->
    <rect x="840" y="0" width="840" height="110" rx="10" fill="#0f172a" stroke="#06b6d4" stroke-width="1.2" opacity="0.95"/>
    <text x="864" y="28" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="900" fill="#22d3ee">⚡ PRECISIONX SOLUTION: AUTOMATED ZERO-WAIT SOVEREIGN TELEMETRY</text>
    <text x="864" y="52" font-family="'Inter', sans-serif" font-size="10.5" fill="#e2e8f0">• Zero-Wait Intercept: Intercepts raw serial RS-232 / USB telemetry directly from NAWI scale in sub-milliseconds.</text>
    <text x="864" y="72" font-family="'Inter', sans-serif" font-size="10.5" fill="#e2e8f0">• Automated OIML R-76: Real-time Table 6 algorithm verifies allowable tolerances (±0.5e, ±1.0e, ±1.5e) instantly.</text>
    <text x="864" y="92" font-family="'Inter', sans-serif" font-size="10.5" fill="#e2e8f0">• Cryptographic Proof: Stamped with Ed25519 signature & PTB DCC XML into ISO PDF/A-3 with offline QR verification.</text>
  </g>
</svg>
`;

const svgPath = "/home/zeno/Desktop/SIH_NAWI_Login_Background.svg";
writeFileSync(svgPath, realNawiSvg);
console.log("Successfully wrote real Mandi NAWI Platform Scale SVG to:", svgPath);
