# PrecisionX — OIML R-76 Sovereign Legal Metrology Workbench
## उपयोगकर्ता मार्गदर्शिका एवं परिचालन नियमावली (User Manual & How-to-Use Guide)

**National Sovereign Metrology Verification & Automated Sealing Platform**  
*Under the Statutory Mandate of Section 15, Legal Metrology Act, 2009 & OIML R 76-1:2006 (E)*  
*Ministry of Consumer Affairs, Food & Public Distribution | Department of Consumer Affairs, Government of India*

---

## विषय सूची (Table of Contents)

1. [प्रणाली अवलोकन एवं सार्वजनिक टेलीमेट्री (System Overview & Public Telemetry)](#1-प्रणाली-अवलोकन-एवं-सार्वजनिक-टेलीमेट्री-system-overview--public-telemetry)
   - 1.1 [मुख्य पृष्ठ एवं सूचना पट्टिका (Hero Masthead & Advisory Ticker)](#11-मुख्य-पृष्ठ-एवं-सूचना-पट्टिका-hero-masthead--advisory-ticker)
   - 1.2 [प्रेसिजनएक्स का वैधानिक अधिदेश (Statutory Mandate: What is PrecisionX?)](#12-प्रेसिजनएक्स-का-वैधानिक-अधिदेश-statutory-mandate-what-is-precisionx)
   - 1.3 [राष्ट्रीय सांख्यिकी एवं जोखिम हीटमैप (Milestones & Regional Risk Heatmap)](#13-राष्ट्रीय-सांख्यिकी-एवं-जोखिम-हीटमैप-milestones--regional-risk-heatmap)
   - 1.4 [क्षेत्राधिकार निगरानी नोड्स एवं विफलता विश्लेषण (Monitored Nodes & Primary Failures)](#14-क्षेत्राधिकार-निगरानी-नोड्स-एवं-विफलता-विश्लेषण-monitored-nodes--primary-failures)
   - 1.5 [कोर तकनीकी स्तंभ एवं वैधानिक प्रकटीकरण (Core Engine Pillars & Statutory Disclosures)](#15-कोर-तकनीकी-स्तंभ-एवं-वैधानिक-प्रकटीकरण-core-engine-pillars--statutory-disclosures)
2. [बहु-भूमिका अभिगम नियंत्रण (Multi-Role Authentication & Access Gate)](#2-बहु-भूमिका-अभिगम-नियंत्रण-multi-role-authentication--access-gate)
   - 2.1 [बहु-भूमिका साइन-इन कार्ड (Multi-Role Sign-In Card)](#21-बहु-भूमिका-साइन-इन-कार्ड-multi-role-sign-in-card)
   - 2.2 [दो-चरणीय प्रमाणीकरण (Two-Factor Authentication - 2FA / TOTP)](#22-दो-चरणीय-प्रमाणीकरण-two-factor-authentication---2fa--totp)
   - 2.3 [हेडर एवं साइडबार टॉगल नियंत्रण (Sidebar Header Quick Controls)](#23-हेडर-एवं-साइडबार-टॉगल-नियंत्रण-sidebar-header-quick-controls)
3. [निरीक्षक कार्यक्षेत्र एवं प्रवर्तन कतार (Inspector Workbench & Verification Queue)](#3-निरीक्षक-कार्यक्षेत्र-एवं-प्रवर्तन-कतार-inspector-workbench--verification-queue)
   - 3.1 [परिचालन डैशबोर्ड एवं सत्र अवलोकन (Operational Dashboard & Session Overview)](#31-परिचालन-डैशबोर्ड-एवं-सत्र-अवलोकन-operational-dashboard--session-overview)
   - 3.2 [सक्रिय सत्यापन कार्य कतार (Active Verification Task Queue)](#32-सक्रिय-सत्यापन-कार्य-कतार-active-verification-task-queue)
   - 3.3 [राष्ट्रीय निगरानी एवं एआई एज ऑडिट कंसोल (AI Edge Surveillance Console)](#33-राष्ट्रीय-निगरानी-एवं-एआई-एज-ऑडिट-कंसोल-ai-edge-surveillance-console)
   - 3.4 [जिला जोखिम एवं विसंगति खुफिया कंसोल (District Risk & Anomaly Intelligence)](#34-जिला-जोखिम-एवं-विसंगति-खुफिया-कंसोल-district-risk--anomaly-intelligence)
   - 3.5 [प्रवर्तन प्रभाग वैधानिक अनुपालन कार्य (Enforcement Division Statutory Tasks)](#35-प्रवर्तन-प्रभाग-वैधानिक-अनुपालन-कार्य-enforcement-division-statutory-tasks)
   - 3.6 [बहु-व्यापारी प्रतिष्ठान एवं सत्यापन स्थिति ग्रिड (Multi-Trader Verification Queue & In-Service Tasks)](#36-बहु-व्यापारी-प्रतिष्ठान-एवं-सत्यापन-स्थिति-ग्रिड-multi-trader-verification-queue--in-service-tasks)
4. [उपकरण एवं प्रयोगशाला सेटअप (Instrument & Laboratory Setup)](#4-उपकरण-एवं-प्रयोगशाला-सेटअप-instrument--laboratory-setup)
   - 4.1 [उपकरण विवरण एवं पर्यावरणीय परिस्थितियां (NAWI OIML R-76 Setup & Conditions)](#41-उपकरण-विवरण-एवं-पर्यावरणीय-परिस्थितियां-nawi-oiml-r-76-setup--conditions)
5. [फॉर्म 1: वजन निष्पादन परीक्षण (Form 1: Weighing Performance Test - Clause A.4.4)](#5-फॉर्म-1-वजन-निष्पादन-परीक्षण-form-1-weighing-performance-test---clause-a44)
   - 5.1 [क्लॉज A.4.4.3 शून्य संदर्भ रीडिंग (Zero Reference Reading & Drift Compensation)](#51-क्लॉज-a443-शून्य-संदर्भ-रीडिंग-zero-reference-reading--drift-compensation)
   - 5.2 [वजन परीक्षण प्रविष्टि एवं लाइव स्केल अंतर्ग्रहण (Record Weighing Step & MT-SICS Ingest)](#52-वजन-परीक्षण-प्रविष्टि-एवं-लाइव-स्केल-अंतर्ग्रहण-record-weighing-step--mt-sics-ingest)
   - 5.3 [वजन अवलोकन तालिका एवं एम.पी.ई. मूल्यांकन (Accuracy Observation Table & Evaluation)](#53-वजन-अवलोकन-तालिका-एवं-एमपीई-मूल्यांकन-accuracy-observation-table--evaluation)
6. [फॉर्म 3: कोना विलक्षणता परीक्षण (Form 3: Corner Eccentricity Test - Clause 3.6.2 & A.4.7)](#6-फॉर्म-3-कोना-विलक्षणता-परीक्षण-form-3-corner-eccentricity-test---clause-362--a47)
   - 6.1 [पांच-बिंदु स्केल पैन स्कीमेटिक (Scale Pan 5-Point Schematic & 1/3 Max Load)](#61-पांच-बिंदु-स्केल-पैन-स्कीमेटिक-scale-pan-5-point-schematic--13-max-load)
   - 6.2 [विलक्षणता अवलोकन तालिका एवं कोना त्रुटि गणना (Eccentricity Table & Corner Error Ec)](#62-विलक्षणता-अवलोकन-तालिका-एवं-कोना-त्रुटि-गणना-eccentricity-table--corner-error-ec)
7. [फॉर्म 5: पुनरावृत्ति परीक्षण (Form 5: Repeatability Test - Clause 3.6.1 & A.4.10)](#7-फॉर्म-5-पुनरावृत्ति-परीक्षण-form-5-repeatability-test---clause-361--a410)
   - 7.1 [दोहरी श्रृंखला पुनरावृत्ति परीक्षण (Dual Series 50% & 100% Max Repeatability)](#71-दोहरी-श्रृंखला-पुनरावृत्ति-परीक्षण-dual-series-50--100-max-repeatability)
8. [फॉर्म 15: सॉफ्टवेयर परीक्षण एवं चेकसम (Form 15: Software Examination - WELMEC 7.2)](#8-फॉर्म-15-सॉफ्टवेयर-परीक्षण-एवं-चेकसम-form-15-software-examination---welmec-72)
   - 8.1 [सॉफ्टवेयर अखंडता, SHA-256 एवं 6-बिंदु वेल्मेक चेकलिस्ट (WELMEC 7.2 LRS Kernel Audit)](#81-सॉफ्टवेयर-अखंडता-sha-256-एवं-6-बिंदु-वेल्मेक-चेकलिस्ट-welmec-72-lrs-kernel-audit)
9. [एम.पी.ई. तुरही वक्र सहनशीलता गलियारा (MPE Trumpet Tolerance Corridor - Table 6)](#9-एमपीई-तुरही-वक्र-सहनशीलता-गलियारा-mpe-trumpet-tolerance-corridor---table-6)
   - 9.1 [इंटरएक्टिव तुरही आवरण वक्र (Interactive Trumpet Curve Limits & Table 6 Brackets)](#91-इंटरएक्टिव-तुरही-आवरण-वक्र-interactive-trumpet-curve-limits--table-6-brackets)
   - 9.2 [वास्तविक समय विचलन एवं मार्जिन ट्रैकिंग (Real-Time Error Deviation & Corridor Plot)](#92-वास्तविक-समय-विचलन-एवं-मार्जिन-ट्रैकिंग-real-time-error-deviation--corridor-plot)
10. [थोक सीएसवी डेटा अंतर्ग्रहण (Batch CSV Ingestion Engine)](#10-थोक-सीएसवी-डेटा-अंतर्ग्रहण-batch-csv-ingestion-engine)
    - 10.1 [प्रयोगशाला सीएसवी डेटा अंतर्ग्रहण एवं स्वचालित पार्सिंग (Batch CSV Ingestion Engine)](#101-प्रयोगशाला-सीएसवी-डेटा-अंतर्ग्रहण-एवं-स्वचालित-पार्सिंग-batch-csv-ingestion-engine)
11. [डिजिटल भंडार, आईएसओ पीडीएफ/ए-3 एवं पीटीबी डीसीसी (Digital Repository & ISO 19005-3)](#11-डिजिटल-भंडार-आईएसओ-पीडीएफए-3-एवं-पीटीबी-डीसीसी-digital-repository--iso-19005-3)
    - 11.1 [आईएसओ 19005-3 पीडीएफ/ए-3 कंटेनर एवं पीटीबी डीसीसी v3.2.1 सत्यापनकर्ता (PDF/A-3 & PTB DCC Verifier)](#111-आईएसओ-19005-3-पीडीएफए-3-कंटेनर-एवं-पीटीबी-डीसीसी-v321-सत्यापनकर्ता-pdfa-3--ptb-dcc-verifier)
    - 11.2 [डिजिटल मेट्रोलॉजी रिपॉजिटरी एवं टेस्ट रिपोर्ट खोज (Digital Metrology Repository Records)](#112-डिजिटल-मेट्रोलॉजी-रिपॉजिटरी-एवं-टेस्ट-रिपोर्ट-खोज-digital-metrology-repository-records)
    - 11.3 [ऐतिहासिक परीक्षण रिपोर्ट, स्थिति फ़िल्टर एवं मास्टर पीडीएफ (Repository Search & Master Download)](#113-ऐतिहासिक-परीक्षण-रिपोर्ट-स्थिति-फ़िल्टर-एवं-मास्टर-पीडीएफ-repository-search--master-download)
12. [विधिक मापविज्ञान समीक्षा एवं औपचारिक प्रमाणीकरण (Legal Metrology Review & Revision Audit Trail)](#12-विधिक-मापविज्ञान-समीक्षा-एवं-औपचारिक-प्रमाणीकरण-legal-metrology-review--revision-audit-trail)
    - 12.1 [विधिक समीक्षा, सरकारी स्टाम्पिंग शुल्क एवं वैधता अवधि (Review & Formal Certification - OIML R 76-2)](#121-विधिक-समीक्षा-सरकारी-स्टाम्पिंग-शुल्क-एवं-वैधता-अवधि-review--formal-certification---oiml-r-76-2)
    - 12.2 [एंटी-रोलबैक जीवनचक्र, संशोधन ऑडिट ट्रेल एवं जनरेटेड आर्टिफैक्ट्स (Anti-Rollback Lifecycle & Archival Artifacts)](#122-एंटी-रोलबैक-जीवनचक्र-संशोधन-ऑडिट-ट्रेल-एवं-जनरेटेड-आर्टिफैक्ट्स-anti-rollback-lifecycle--archival-artifacts)
13. [ऑफ़लाइन एड25519 क्रिप्टोग्राफ़िक क्यूआर कोड सत्यापन (Offline Ed25519 Cryptographic QR Verification)](#13-ऑफ़लाइन-एड25519-क्रिप्टोग्राफ़िक-क्यूआर-कोड-सत्यापन-offline-ed25519-cryptographic-qr-verification)
    - 13.1 [डिजिटल सील एवं 100% ऑफ़लाइन क्यूआर सत्यापन (Ed25519 Offline Digital Seal Verification)](#131-डिजिटल-सील-एवं-100-ऑफ़लाइन-क्यूआर-सत्यापन-ed25519-offline-digital-seal-verification)
14. [वैधानिक कानून, राजपत्र एवं विधिक मापविज्ञान कैलकुलेटर (Statutory Law, Gazette & Tools)](#14-वैधानिक-कानून-राजपत्र-एवं-विधिक-मापविज्ञान-कैलकुलेटर-statutory-law-gazette--tools)
    - 14.1 [मंत्रालय वैधानिक उपकरण (Schedule IX Fee, Test Load Substitution, Jan Vishwas Penalties)](#141-मंत्रालय-वैधानिक-उपकरण-schedule-ix-fee-test-load-substitution-jan-vishwas-penalties)
    - 14.2 [विधिक मापविज्ञान राजपत्र अन्वेषक (Legal Metrology Gazette Explorer - 91 Official Acts)](#142-विधिक-मापविज्ञान-राजपत्र-अन्वेषक-legal-metrology-gazette-explorer---91-official-acts)
    - 14.3 [प्रत्यक्ष आधिकारिक राजपत्र पीडीएफ दर्शक (Official Gazette Direct PDF Viewer)](#143-प्रत्यक्ष-आधिकारिक-राजपत्र-पीडीएफ-दर्शक-official-gazette-direct-pdf-viewer)
15. [व्यवस्थापक नियंत्रण केंद्र (Admin Control Center & Director Authorization)](#15-व्यवस्थापक-नियंत्रण-केंद्र-admin-control-center--director-authorization)
    - 15.1 [निदेशक प्राधिकरण द्वार (Lab Director Authorization Gate)](#151-निदेशक-प्राधिकरण-द्वार-lab-director-authorization-gate)
    - 15.2 [निदेशक लॉगिन संवाद एवं जूरी क्रेडेंशियल्स (Director Login Modal & Fast-Auth)](#152-निदेशक-लॉगिन-संवाद-एवं-जूरी-क्रेडेंशियल्स-director-login-modal--fast-auth)
16. [नेविगेशन साइडबार एवं निओन रेड थीम अनुकूलन (Sidebar Controls & Neon Red Theme)](#16-नेविगेशन-साइडबार-एवं-निओन-रेड-थीम-अनुकूलन-sidebar-controls--neon-red-theme)
    - 16.1 [पूर्ण वर्कबेंच साइडबार नेविगेशन मेनू (Full Workbench Sidebar Modules)](#161-पूर्ण-वर्कबेंच-साइडबार-नेविगेशन-मेनू-full-workbench-sidebar-modules)
    - 16.2 [विस्तारित कार्यक्षेत्र कंसोल एवं निओन रेड थीम (Expanded Workbench Console & Neon Red Theme)](#162-विस्तारित-कार्यक्षेत्र-कंसोल-एवं-निओन-रेड-थीम-expanded-workbench-console--neon-red-theme)
17. [तकनीकी सहायता एवं संपर्क (Support & Verification Hotline)](#17-तकनीकी-सहायता-एवं-संपर्क-support--verification-hotline)

---

## 1. प्रणाली अवलोकन एवं सार्वजनिक टेलीमेट्री (System Overview & Public Telemetry)

पोर्टल के लैंडिंग पृष्ठ पर राष्ट्रीय विधिक मापविज्ञान प्रभाग का आधिकारिक सार्वजनिक दृश्य उपलब्ध है।

### 1.1 मुख्य पृष्ठ एवं सूचना पट्टिका (Hero Masthead & Advisory Ticker)
![Portal Hero Masthead](docs/screenshots/Screenshot%20from%202026-10-22%2018-45-49.png)
- **शीर्ष बैनर (Top Header):** भारत सरकार का आधिकारिक प्रतीक, उपभोक्ता मामले मंत्रालय का नाम, स्मार्ट इंडिया हैकाथॉन 2026 (SIH26035) बैनर और लाइव सर्वर सिंक स्थिति।
- **ताज़ा समाचार टिकर (What's New Ticker):** विधिक मापविज्ञान अधिनियम 2009, आवश्यक वस्तु अधिनियम और नवीनतम सरकारी अधिसूचनाएं वास्तविक समय में स्क्रॉल होती हैं। इसे पॉज/प्ले बटन द्वारा नियंत्रित किया जा सकता है।
- **त्वरित नियंत्रण (Quick Controls):** भाषा बदलने हेतु  टॉगल, थीम पैलेट पिकर  और फ़ुलस्क्रीन  बटन शीर्ष पर उपलब्ध हैं।

### 1.2 प्रेसिजनएक्स का वैधानिक अधिदेश (Statutory Mandate: What is PrecisionX?)
![What is PrecisionX](docs/screenshots/Screenshot%20from%202026-10-22%2018-46-13.png)
- **उद्देश्य (Objective):** धारा 15 विधिक मापविज्ञान अधिनियम 2009 और OIML R 76-1:2006 मानक के अंतर्गत गैर-स्वचालित तौल उपकरणों (NAWI) का वास्तविक समय डिजिटल सत्यापन एवं सीलिंग।
- **सुरक्षा विशेषताएं (Security Architecture):** Ed25519 असममित डिजिटल हस्ताक्षर, पीटीबी डीसीसी (PTB DCC v3.2.1) एक्सएमएल स्कीमा, आईएसओ 19005-3 पीडीएफ/ए-3 कंटेनर और वेल्मेक 7.2 सॉफ्टवेयर सीलिंग।

### 1.3 राष्ट्रीय सांख्यिकी एवं जोखिम हीटमैप (Milestones & Regional Risk Heatmap)
![PrecisionX Milestones & Heatmap](docs/screenshots/Screenshot%20from%202026-10-22%2018-47-22.png)
- **राष्ट्रीय मील के पत्थर (Milestones):** 18,527+ सत्यापित उपकरण, 142 सक्रिय निरीक्षक, 98.4% राष्ट्रीय अनुपालन दर और 100% वेल्मेक 7.2 अखंडता।
- **क्षेत्रीय प्रवर्तन विसंगति हीटमैप (Regional Anomaly Heatmap):** मुंबई एपीएमसी यार्ड, दक्षिणी दिल्ली व्यापारिक केंद्र, अहमदाबाद कालूपुर मंडी आदि में वास्तविक समय उल्लंघन निगरानी।
- **सटीकता वर्ग अनुपालन:** Class I (विश्लेषणात्मक 99.4%), Class II (बुलियन 98.1%), Class III (वाणिज्यिक खुदरा 95.8%), Class IIII (धर्मकांटा / वेइब्रिज 96.2%)।

### 1.4 क्षेत्राधिकार निगरानी नोड्स एवं विफलता विश्लेषण (Monitored Nodes & Primary Failures)
![Monitored Nodes](docs/screenshots/Screenshot%20from%202026-10-22%2018-48-04.png)
- **प्रमुख क्षेत्राधिकार नोड्स:** बेंगलुरु अनाज मंडी, पुणे हड़पसर औद्योगिक क्षेत्र, अहमदाबाद कालूपुर मंडी, चेन्नई पोर्ट कंटेनर टर्मिनल, कोलकाता बड़ाबाजार, हैदराबाद बेगम बाजार।
- **विफलता के प्राथमिक कारण:** तालिका 6 एम.पी.ई. सहनशीलता उल्लंघन (52%), कोने का विलक्षणता भार विचलन (24%), शून्य रिटर्न सेंसर बहाव (15%), वायर सील छेड़छाड़ (9%)।

### 1.5 कोर तकनीकी स्तंभ एवं वैधानिक प्रकटीकरण (Core Engine Pillars & Statutory Disclosures)
![Core Engine Pillars](docs/screenshots/Screenshot%20from%202026-10-22%2018-48-27.png)
- **तकनीकी स्तंभ:** OIML R-76 MPE इंजन, Ed25519 क्रिप्टोग्राफी, PTB DCC & PDF/A-3, और WELMEC 7.2 विधिक प्रासंगिक सॉफ्टवेयर सीलिंग।
- **वैधानिक प्रकटीकरण:** धारा 44, विधिक मापविज्ञान अधिनियम 2009 के अंतर्गत तौल उपकरणों से अनधिकृत छेड़छाड़ गैर-जमानती दंडात्मक अपराध है।

---

## 2. बहु-भूमिका अभिगम नियंत्रण (Multi-Role Authentication & Access Gate)

### 2.1 बहु-भूमिका साइन-इन कार्ड (Multi-Role Sign-In Card)
![Inspector Sign-In](docs/screenshots/Screenshot%20from%202026-10-22%2018-46-49.png)
- **तीन अभिगम भूमिकाएं:**
  1. **Inspector / Officer:** पूर्ण OIML परीक्षण मॉड्यूल, एम.पी.ई. गणना और डिजिटल सीलिंग कार्यक्षेत्र।
  2. **Verified Citizen:** उपभोक्ता बिना लॉगिन के सीधे सार्वजनिक सत्यापन पोर्टल से क्यूआर कोड और वजन प्रमाणपत्र की प्रामाणिकता जांच सकते हैं।
  3. **Trader / Mandi:** व्यापारी अपने प्रतिष्ठान के तौल पैमानों का आवधिक सत्यापन शेड्यूल देख सकते हैं।
- **क्रेडेंशियल्स:** विभागीय ईमेल (), अधिकारी आईडी (), गुप्त पासफ़्रेज़, और प्रयोगशाला क्षेत्राधिकार चयन।

### 2.2 दो-चरणीय प्रमाणीकरण (Two-Factor Authentication - 2FA / TOTP)
![2FA Authentication](docs/screenshots/Screenshot%20from%202026-10-22%2018-49-39.png)
- **सुरक्षा चुनौती:** पंजीकृत मोबाइल नंबर पर 6-अंकीय ओटीपी कोड भेजा जाता है।
- **मूल्यांकन हेतु:** "Judge Demo Passcode: 784206" के पास **Auto-Fill Code** बटन दबाकर तुरंत कोड दर्ज करें और **Verify Passcode & Enter Portal** पर क्लिक करें।

### 2.3 हेडर एवं साइडबार टॉगल नियंत्रण (Sidebar Header Quick Controls)
![Sidebar Toggle Controls](docs/screenshots/Screenshot%20from%202026-10-22%2018-51-34.png)
- **मेनू खोलना (Turn ON):** शीर्ष हेडर में बाईं ओर स्थित ऐप आइकन (PrecisionX Logo) पर क्लिक करें।
- **मेनू बंद करना (Turn OFF):** साइडबार के शीर्ष पर दाईं ओर स्थित बाण बटन () पर क्लिक करें।

---

## 3. निरीक्षक कार्यक्षेत्र एवं प्रवर्तन कतार (Inspector Workbench & Verification Queue)

### 3.1 परिचालन डैशबोर्ड एवं सत्र अवलोकन (Operational Dashboard & Session Overview)
![Inspector Dashboard](docs/screenshots/Screenshot%20from%202026-10-22%2019-10-08.png)
- **सत्र स्थिति:** सत्र आईडी , समीक्षा जीवनचक्र , जीरो-एरर , और WELMEC 7.2 LRS सील ।
- **अधिकारी प्रोफ़ाइल:** निरीक्षक आर. वर्मा, आईडी , विधिक मापविज्ञान विभाग, महाराष्ट्र।
- **कार्य सारांश:** 4 सौंपे गए कार्य, 0 लंबित, 4 पूर्ण और सीलबंद।

### 3.2 सक्रिय सत्यापन कार्य कतार (Active Verification Task Queue)
![Verification Queue](docs/screenshots/Screenshot%20from%202026-10-22%2019-10-55.png)
- **कतारबद्ध प्रतिष्ठान:**
  - : एपेक्स फॉर्मूलेशन (Entris II Precision, Class II, 620g) - तत्काल (URGENT)
  - : श्री कृष्णा एग्रो ट्रेडर्स (DS-215 Commercial, Class III, 15000g) - उच्च प्राथमिकता
  - : झावेरी गोल्ड एंड ऑर्नामेंट्स (ME204 Analytical, Class I, 220g) - उच्च प्राथमिकता
  - : भारत फूड प्रोविजन्स (AW-30 Industrial Bench, Class III, 30000g) - सामान्य
- प्रत्येक कार्य के साथ प्रत्यक्ष प्रमाणपत्र देखने हेतु  लिंक उपलब्ध है।

### 3.3 राष्ट्रीय निगरानी एवं एआई एज ऑडिट कंसोल (AI Edge Surveillance Console)
![AI Edge Console](docs/screenshots/Screenshot%20from%202026-10-22%2019-12-08.png)
- **48 एज नोड्स कनेक्टेड:** सभी राज्य संदर्भ मानक प्रयोगशालाओं (RRSL) की लाइव टेलीमेट्री निगरानी।
- **99.82% सटीकता दर:** शून्य गलत-सकारात्मक जब्ती रिकॉर्ड। Ed25519 क्रिप्टोग्राफ़िक रूप से सीलबंद।

### 3.4 जिला जोखिम एवं विसंगति खुफिया कंसोल (District Risk & Anomaly Intelligence)
![District Risk Console](docs/screenshots/Screenshot%20from%202026-10-22%2019-16-25.png)
- **धारा 18 वैधानिक ऑडिट (Section 18 Audit):** जिला स्तर पर तौल उपकरणों में विसंगतियों की एआई निगरानी।
- **लाइव स्ट्रीम सिंक:**  तथा  बटन द्वारा स्वचालित विसंगति पहचान।
- **सत्यापित स्थिति:** 48 एज नोड्स, 99.82% सटीकता दर, और CSIR-NPLI IST समय मानक से ट्रेस करने योग्य Ed25519 क्रिप्टोग्राफिक सील।

### 3.5 प्रवर्तन प्रभाग वैधानिक अनुपालन कार्य (Enforcement Division Statutory Tasks)
![Enforcement Tasks](docs/screenshots/Screenshot%20from%202026-10-22%2019-17-24.png)
- **धारा 15 अनिवार्य सत्यापन:** धारा 15 विधिक मापविज्ञान अधिनियम 2009 के अंतर्गत वाणिज्यिक संस्थानों में तौल उपकरणों का वैधानिक सत्यापन।
- **त्वरित कार्य निष्पादन:**  पर क्लिक करके कतारबद्ध सभी उपकरणों का स्वतः सत्यापन और सीलिंग की जा सकती है।
- **नया कार्य अनुसूची:**  बटन द्वारा किसी भी नए प्रतिष्ठान का भौतिक सत्यापन शेड्यूल किया जा सकता है।

### 3.6 बहु-व्यापारी प्रतिष्ठान एवं सत्यापन स्थिति ग्रिड (Multi-Trader Verification Queue & In-Service Tasks)
![Multi-Trader Queue](docs/screenshots/Screenshot%20from%202026-10-22%2019-18-16.png)
- **संपूर्ण व्यापारी ग्रिड:** मुंबई एमआईडीसी, वाशी एपीएमसी मंडी और झावेरी बाजार के विभिन्न प्रतिष्ठानों की व्यापक सूची।
- **सत्यापन स्थिति:** प्रत्येक उपकरण का सटीकता वर्ग (Class I, II, III), मॉडल विनिर्देश, निर्धारित तिथि और  स्थिति स्पष्ट रूप से प्रदर्शित होती है।

---

## 4. उपकरण एवं प्रयोगशाला सेटअप (Instrument & Laboratory Setup)

### 4.1 उपकरण विवरण एवं पर्यावरणीय परिस्थितियां (NAWI OIML R-76 Setup & Conditions)
![Instrument Setup](docs/screenshots/Screenshot%20from%202026-10-22%2019-19-10.png)
- **उपकरण पैरामीटर (Instrument Parameters):**
  - निर्माता (Manufacturer): 
  - मॉडल (Model): 
  - सटीकता वर्ग (Accuracy Class): 
  - सीरियल नंबर: 
  - अधिकतम क्षमता (Max): 
  - न्यूनतम क्षमता (Min): 
  - सत्यापन पैमाना अंतराल ($): 
  - वास्तविक पैमाना अंतराल ($): 
- **पर्यावरणीय डेटा (Laboratory Conditions):**
  - तापमान: 
  - सापेक्ष आर्द्रता: 
  - वायुमंडलीय दबाव: 
  - प्रयोगशाला स्थान: 
- डेटा भरने के बाद **Proceed to Testing →** पर क्लिक करें।

---

## 5. फॉर्म 1: वजन निष्पादन परीक्षण (Form 1: Weighing Performance Test - Clause A.4.4)

### 5.1 क्लॉज A.4.4.3 शून्य संदर्भ रीडिंग (Zero Reference Reading & Drift Compensation)
![Form 1 Zero Reference](docs/screenshots/Screenshot%20from%202026-10-22%2019-13-17.png)
- **शून्य त्रुटि निर्धारण:**  = P_0 - L_0$ का उपयोग बाद के सभी लोड चरणों को संतुलित करने हेतु किया जाता है।
- **लाइव स्केल अंतर्ग्रहण:**  बटन द्वारा सीधे डिजिटल वेइंग स्केल से सीरियल डेटा प्राप्त किया जा सकता है।

### 5.2 वजन परीक्षण प्रविष्टि एवं लाइव स्केल अंतर्ग्रहण (Record Weighing Step & MT-SICS Ingest)
![Record Weighing Step](docs/screenshots/Screenshot%20from%202026-10-22%2019-21-15.png)
- **परीक्षण चरण प्रविष्टि:** चरण संख्या, लोड भार ($), प्रदर्शित संकेत ($), और अतिरिक्त लोड ($\Delta L$) दर्ज करें।
- **दिशा चयन (Direction):** भार बढ़ाते समय  और घटाते समय  चुनें।
- **सत्यापन स्थिति:** एआई मेट्रोलॉजी इंजन वास्तविक समय में OIML Table 6 के अनुसार सहिष्णुता की जांच करता है।

### 5.3 वजन अवलोकन तालिका एवं एम.पी.ई. मूल्यांकन (Accuracy Observation Table & Evaluation)
![Form 1 Steps](docs/screenshots/Screenshot%20from%202026-10-22%2019-19-42.png)
- **परीक्षण लोड श्रृंखला (Test Loads):**
  - चरण 1: संदर्भ भार , संकेत , त्रुटि , MPE  → **PASS**
  - चरण 2: संदर्भ भार , संकेत , त्रुटि , MPE  → **PASS**
  - चरण 3: संदर्भ भार , संकेत , त्रुटि , MPE  → **PASS**
  - चरण 4: संदर्भ भार , संकेत , त्रुटि , MPE  → **PASS**
  - चरण 5: संदर्भ भार , संकेत , त्रुटि , MPE  → **PASS**
- सभी चरण OIML तालिका 6 के अधिकतम अनुमेय त्रुटि गलियारे में उत्तीर्ण होने पर **Evaluate & Generate Report** सक्रिय होता है।

---

## 6. फॉर्म 3: कोना विलक्षणता परीक्षण (Form 3: Corner Eccentricity Test - Clause 3.6.2 & A.4.7)

### 6.1 पांच-बिंदु स्केल पैन स्कीमेटिक (Scale Pan 5-Point Schematic & 1/3 Max Load)
![Form 3 Eccentricity](docs/screenshots/Screenshot%20from%202026-10-22%2019-21-55.png)
- **परीक्षण भार:** /3 	ext{ Max} = 5000	ext{ g}$ (अनुमेय सहिष्णुता $\pm 5.0	ext{ g}$)।
- **लक्ष्य स्थान (Target Positions):**
  1. केंद्र (Center)
  2. आगे-बाएं (Front-Left)
  3. पीछे-बाएं (Back-Left)
  4. पीछे-दाएं (Back-Right)
  5. आगे-दाएं (Front-Right)

### 6.2 विलक्षणता अवलोकन तालिका एवं कोना त्रुटि गणना (Eccentricity Table & Corner Error Ec)
![Form 3 Table](docs/screenshots/Screenshot%20from%202026-10-22%2019-22-12.png)
- प्रत्येक कोने पर 5000g का भार रखकर अतिरिक्त लोड ($\Delta L$) दर्ज करें और **Submit Corner Reading** पर क्लिक करें। सिस्टम स्वतः विचलित त्रुटि ($) की गणना करता है।

---

## 7. फॉर्म 5: पुनरावृत्ति परीक्षण (Form 5: Repeatability Test - Clause 3.6.1 & A.4.10)

### 7.1 दोहरी श्रृंखला पुनरावृत्ति परीक्षण (Dual Series 50% & 100% Max Repeatability)
![Form 5 Repeatability](docs/screenshots/Screenshot%20from%202026-10-22%2019-22-38.png)
- **दोहरी श्रृंखला परीक्षण:**
  - **श्रृंखला A:** ~50% Max (,500	ext{ g}$) पर 10 क्रमिक वजन रीडिंग।
  - **श्रृंखला B:** 100% Max (5,000	ext{ g}$) पर 10 क्रमिक वजन रीडिंग।
- **वैधानिक आवश्यकता:**  \leq |MPE|$।
- न्यूनतम, अधिकतम एवं फैलाव (Spread) का वास्तविक समय में स्वतः सत्यापन किया जाता है।

---

## 8. फॉर्म 15: सॉफ्टवेयर परीक्षण एवं चेकसम (Form 15: Software Examination - WELMEC 7.2)

### 8.1 सॉफ्टवेयर अखंडता, SHA-256 एवं 6-बिंदु वेल्मेक चेकलिस्ट (WELMEC 7.2 LRS Kernel Audit)
![Form 15 Software Exam](docs/screenshots/Screenshot%20from%202026-10-22%2019-23-27.png)
- **सॉफ्टवेयर अखंडता सत्यापन:**
  - LRS कर्नेल मॉड्यूल: 
  - SHA-256 डाइजेस्ट: 
  - CRC-32 चेकसम: 
- **6-बिंदु वेल्मेक चेकलिस्ट:**
  - : सॉफ्टवेयर पहचान एवं संस्करण प्रदर्शन → **COMPLIANT**
  - : क्रिप्टोग्राफ़िक चेकसम / हैश अखंडता → **COMPLIANT**
  - : सॉफ्टवेयर पृथक्करण (विधिक प्रासंगिक बनाम गैर-प्रासंगिक) → **COMPLIANT**
  - : मेट्रोलॉजिकल समायोजन पैरामीटर सुरक्षा (हार्डवेयर जम्पर लॉक) → **COMPLIANT**
  - : ऑडिट ट्रेल / इवेंट काउंटर वृद्धि सत्यापन → **COMPLIANT**
  - : अचानक बिजली कटने पर डेटा प्रतिधारण एवं अखंडता → **COMPLIANT**

---

## 9. एम.पी.ई. तुरही वक्र सहनशीलता गलियारा (MPE Trumpet Tolerance Corridor - Table 6)

### 9.1 इंटरएक्टिव तुरही आवरण वक्र (Interactive Trumpet Curve Limits & Table 6 Brackets)
![Trumpet Curve Limits](docs/screenshots/Screenshot%20from%202026-10-22%2019-24-03.png)
- **OIML R 76-1 तालिका 6 चरणबद्ध कोष्ठक (Brackets):**
  - Bracket 1 (bash 	ext{ to } 500e$): $\pm 0.5e = \pm 2.5	ext{ g}$
  - Bracket 2 (00e 	ext{ to } 2000e$): $\pm 1.0e = \pm 5.0	ext{ g}$
  - Bracket 3 (000e 	ext{ to Max}$): $\pm 1.5e = \pm 7.5	ext{ g}$

### 9.2 वास्तविक समय विचलन एवं मार्जिन ट्रैकिंग (Real-Time Error Deviation & Corridor Plot)
![Trumpet Curve Corridor](docs/screenshots/Screenshot%20from%202026-10-22%2019-24-22.png)
- प्रत्येक रिकॉर्ड किए गए वजन का मान तुरही वक्र पर बिंदु के रूप में प्रदर्शित होता है।
- यदि कोई बिंदु लाल सहिष्णुता रेखा से बाहर जाता है, तो उपकरण स्वतः **REJECTED** के रूप में चिह्नित हो जाता है।

---

## 10. थोक सीएसवी डेटा अंतर्ग्रहण (Batch CSV Ingestion Engine)

### 10.1 प्रयोगशाला सीएसवी डेटा अंतर्ग्रहण एवं स्वचालित पार्सिंग (Batch CSV Ingestion Engine)
![CSV Batch Ingestion](docs/screenshots/Screenshot%20from%202026-10-22%2019-25-06.png)
- प्रयोगशाला मापन शीट या सीरियल डंप से सीधे डेटा आयात करने की सुविधा।
- **Load Sample CSV Template** बटन से मानक प्रारूप प्राप्त करें, रिकॉर्ड चिपकाएं, और **Execute Batch Ingestion** दबाएं।

---

## 11. डिजिटल भंडार, आईएसओ पीडीएफ/ए-3 एवं पीटीबी डीसीसी (Digital Repository & ISO 19005-3)

### 11.1 आईएसओ 19005-3 पीडीएफ/ए-3 कंटेनर एवं पीटीबी डीसीसी v3.2.1 सत्यापनकर्ता (PDF/A-3 & PTB DCC Verifier)
![ISO PDF/A-3 Verifier](docs/screenshots/Screenshot%20from%202026-10-22%2019-25-30.png)
- **कंटेनर सत्यापन:** प्रमाणित PDF/A-3 रिपोर्ट से PTB DCC v3.2.1 XML और SmartCom D-SI डेटासेट का निष्कर्षण और Ed25519 डिजिटल सील का 100% ऑफ़लाइन सत्यापन।
- **ड्रैग एवं ड्रॉप:** स्थानीय सिस्टम से फ़ाइल खींचकर सीधे सत्यापन क्षेत्र में छोड़ें।
- **जालसाजी परीक्षण:**  बटन दबाकर छेड़छाड़ की गई फ़ाइल का त्वरित पता लगाने की कार्यप्रणाली का प्रदर्शन करें।

### 11.2 डिजिटल मेट्रोलॉजी रिपॉजिटरी एवं टेस्ट रिपोर्ट खोज (Digital Metrology Repository Records)
![Digital Metrology Repository](docs/screenshots/Screenshot%20from%202026-10-22%2019-25-57.png)
- **दस्तावेज़ खोज एवं पुनर्प्राप्ति:** रिपोर्ट संख्या (), उपकरण नाम () या स्थिति (DRAFT, APPROVED, REJECTED) के आधार पर त्वरित खोज।
- **दोहरा प्रारूप डाउनलोड:** प्रत्येक सत्यापन हेतु अधिकृत मानव-पठनीय **PDF** और मशीन-पठनीय **XML** (PTB DCC 3.2.1) दोनों उपलब्ध हैं।

### 11.3 ऐतिहासिक परीक्षण रिपोर्ट, स्थिति फ़िल्टर एवं मास्टर पीडीएफ (Repository Search & Master Download)
![Digital Archive Filtered](docs/screenshots/Screenshot%20from%202026-10-22%2019-26-39.png)
- **Archive Current Test:** सक्रिय परीक्षण सत्र को सीधे राष्ट्रीय डिजिटल भंडार में स्थायी रूप से संग्रहीत करें।
- **Download Master PDF:** सम्पूर्ण परीक्षण रिपोर्ट का ISO 19005-3 दीर्घकालिक अभिलेखीय पीडीएफ तुरंत डाउनलोड करें।

---

## 12. विधिक मापविज्ञान समीक्षा एवं औपचारिक प्रमाणीकरण (Legal Metrology Review & Revision Audit Trail)

### 12.1 विधिक समीक्षा, सरकारी स्टाम्पिंग शुल्क एवं वैधता अवधि (Review & Formal Certification - OIML R 76-2)
![Review and Formal Certification](docs/screenshots/Screenshot%20from%202026-10-22%2019-27-16.png)
- **समीक्षक पहचान:** वैज्ञानिक डॉ. ए. के. शर्मा (), वरिष्ठ विधिक मापविज्ञान अधिकारी।
- **अनुसूची IX सरकारी स्टाम्पिंग शुल्क:** चतुर्थ संशोधन G.S.R. 568(E) के अनुसार Class III स्केल हेतु ₹500 का वैधानिक शुल्क।
- **पुनः सत्यापन वैधता अवधि:** 7वें संशोधन G.S.R. 905(E) के अंतर्गत 24 महीने (2-वर्षीय चक्र) की वैधता।
- **समय मानक एवं विधिक ट्रेसिबिलिटी:** CSIR-NPLI परमाणु भारतीय मानक समय (IST Rules 2026, G.S.R. 761(E))।
- **अनिवार्य साक्ष्य (Photographic Evidence Vault):** उपकरण नेमप्लेट, सीलिंग वायर और पैन की तस्वीरें SHA-256 हैश के साथ अपलोड करें।

### 12.2 एंटी-रोलबैक जीवनचक्र, संशोधन ऑडिट ट्रेल एवं जनरेटेड आर्टिफैक्ट्स (Anti-Rollback Lifecycle & Archival Artifacts)
![Anti-Rollback Audit Trail](docs/screenshots/Screenshot%20from%202026-10-22%2019-27-42.png)
- **अपरिवर्तनीय संशोधन श्रृंखला (Immutable Revision Chain):** WELMEC 7.2 और ISO/IEC 17025 के अनुरूप। पूर्व स्वीकृत संशोधन स्थायी रूप से फ्रीज हो जाते हैं।
- **Lock Revision 1 (Approve):** प्रथम संशोधन को अंतिम रूप से लॉक एवं स्वीकृत करें।
- **Amend Entry (Trigger Invalidation):** यदि किसी मान में परिवर्तन किया जाता है, तो पूर्व सील स्वतः अमान्य घोषित हो जाती है और नया संशोधन दर्ज करना अनिवार्य होता है।
- **चार जनरेटेड आर्टिफैक्ट्स:**
  1. Human-Readable HTML Report (OIML R 76-2:2007 Forms 0 to 15)
  2. Archival PDF/A-3 Report (Embedded PTB DCC XML & SHA-256 seal)
  3. Editable MS Word (.docx) (DoCA standard formatting)
  4. PTB DCC v3.2.1 XML (SmartCom D-SI international format)
- **डिजिटल सीलिंग:** **Digitally Sign & Issue Certificate** बटन दबाकर राष्ट्रीय विधिक रजिस्ट्री में प्रमाण पत्र जारी करें।

---

## 13. ऑफ़लाइन एड25519 क्रिप्टोग्राफ़िक क्यूआर कोड सत्यापन (Offline Ed25519 Cryptographic QR Verification)

### 13.1 डिजिटल सील एवं 100% ऑफ़लाइन क्यूआर सत्यापन (Ed25519 Offline Digital Seal Verification)
![Offline Ed25519 QR](docs/screenshots/Screenshot%20from%202026-10-22%2019-28-16.png)
- **प्रमाणपत्र विवरण:**
  - प्रमाणपत्र आईडी: 
  - हस्ताक्षरकर्ता: RRSL-Faridabad / Ministry of Consumer Affairs
  - सार्वजनिक कुंजी फिंगरप्रिंट: 
- **100% ऑफ़लाइन कार्यप्रणाली:** दूरदराज के क्षेत्रों या बिना इंटरनेट वाली मंडियों में फील्ड इंस्पेक्टर या नागरिक किसी भी सामान्य कैमरे से क्यूआर स्कैन करके तात्कालिक सत्यापन कर सकते हैं।
- **Simulate Forgery:** इस बटन पर क्लिक करने पर पेलोड में 1 बिट का परिवर्तन होता है और इंजन तुरंत **SIGNATURE INVALID - TAMPERING DETECTED** अलर्ट जारी करता है।

---

## 14. वैधानिक कानून, राजपत्र एवं विधिक मापविज्ञान कैलकुलेटर (Statutory Law, Gazette & Tools)

### 14.1 मंत्रालय वैधानिक उपकरण (Schedule IX Fee, Test Load Substitution, Jan Vishwas Penalties)
![Ministry Statutory Tools](docs/screenshots/Screenshot%20from%202026-10-22%2019-29-15.png)
- **Schedule IX Fee Calculator (G.S.R. 568(E)):** सटीकता वर्ग और अधिकतम क्षमता दर्ज करके सरकारी स्टाम्पिंग शुल्क की स्वतः गणना करें।
- **Test Load Substitution Engine (Clause 9(2)(ii)):** भारी धर्मकांटों (Weighbridges) पर 80% तक टेस्ट वेट प्रतिस्थापन की अनुमति। यदि पुनरावृत्ति त्रुटि $\Delta E \leq 0.2e$ है, तो 50,000 kg के धर्मकांटे पर केवल 10,000 kg (20%) मानक बांट की आवश्यकता होती है तथा 40,000 kg परिवहन भार की बचत होती है।
- **Jan Vishwas Penalties (Act 8 of 2026):** धारा 25, 26, 29, 30 और 36 के अंतर्गत गैर-आपराधिक सिविल शमन दंड की गणना।

### 14.2 विधिक मापविज्ञान राजपत्र अन्वेषक (Legal Metrology Gazette Explorer - 91 Official Acts)
![Gazette Explorer Grid](docs/screenshots/Screenshot%20from%202026-10-22%2019-30-04.png)
- **91 सत्यापित आधिकारिक राजपत्र:**
  - : सातवीं अनुसूची - गैर-स्वचालित तौल उपकरण (OIML R 76-1)
  - : अनुसूची IX सत्यापन शुल्क स्लैब एवं टेस्ट लोड प्रतिस्थापन
  - : 24-महीने (2-वर्ष) सत्यापन स्टाम्प वैधता का मानकीकरण
  - : सरकार द्वारा अनुमोदित परीक्षण केंद्र (GATC) NAWI परीक्षण दायरा
  - : जन विश्वास अधिनियम (प्रक्रियात्मक उल्लंघनों का वि-अपराधीकरण)
  - : वि-अपराधीकरण प्रवर्तन एवं न्यायनिर्णायक अधिकारी

### 14.3 प्रत्यक्ष आधिकारिक राजपत्र पीडीएफ दर्शक (Official Gazette Direct PDF Viewer)
![Gazette PDF Viewer](docs/screenshots/Screenshot%20from%202026-10-22%2019-30-31.png)
- किसी भी राजपत्र कार्ड पर **Open Official PDF** बटन दबाकर भारत के आधिकारिक राजपत्र की मुद्रित प्रति सीधे ब्राउज़र में पढ़ें और सत्यापित करें।

---

## 15. व्यवस्थापक नियंत्रण केंद्र (Admin Control Center & Director Authorization)

### 15.1 निदेशक प्राधिकरण द्वार (Lab Director Authorization Gate)
![Director Authorization Gate](docs/screenshots/Screenshot%20from%202026-10-22%2019-31-05.png)
- **सर्वोच्च सत्यापन स्तर:** राष्ट्रीय विधिक मापविज्ञान सीलिंग का अंतिम डिजिटल हस्ताक्षर केवल आरआरएसएल (RRSL) प्रयोगशाला निदेशक या अधिकृत वरिष्ठ वैज्ञानिक द्वारा ही किया जा सकता है।

### 15.2 निदेशक लॉगिन संवाद एवं जूरी क्रेडेंशियल्स (Director Login Modal & Fast-Auth)
![Director Login Modal](docs/screenshots/Screenshot%20from%202026-10-22%2019-31-23.png)
- **Load Demo Credentials (Dr. A. K. Sharma):** मूल्यांकन एवं जूरी डेमो हेतु 1-क्लिक प्री-फिल बटन।
- **Authenticate & Unlock:** क्लिक करने पर पूर्ण मास्टर प्रशासनिक अधिकार तथा राष्ट्रीय सीलिंग कुंजियां अनलॉक हो जाती हैं।

---

## 16. नेविगेशन साइडबार एवं निओन रेड थीम अनुकूलन (Sidebar Controls & Neon Red Theme)

### 16.1 पूर्ण वर्कबेंच साइडबार नेविगेशन मेनू (Full Workbench Sidebar Modules)
![Full Sidebar Navigation](docs/screenshots/Screenshot%20from%202026-10-22%2019-32-09.png)
- **श्रेणी 1: वर्कफ़्लो एवं पोर्टल:** Surveillance & AI Dashboard, Pending Tasks Queue, Instrument Setup, Guided Testing Suite.
- **श्रेणी 2: OIML R-76 मॉड्यूल:** Form 1 (Weighing), Form 3 (Eccentricity), Form 5 (Repeatability), Form 15 (Software), Trumpet Curve (MPE).
- **श्रेणी 3: सत्यापन एवं अनुपालन:** CSV Batch Ingestion, PDF/A-3 Vault & PTB DCC, Digital Certificate Repository, Review Report, Ministry Gazette & Acts, Admin Control Center.
- **सेटिंग्स एवं प्रदर्शन:** Language (हिंदी/English), Pick a Theme Color, Fullscreen Canvas (F11).

### 16.2 विस्तारित कार्यक्षेत्र कंसोल एवं निओन रेड थीम (Expanded Workbench Console & Neon Red Theme)
![Expanded Workbench Neon Red](docs/screenshots/Screenshot%20from%202026-10-22%2019-32-29.png)
- **विस्तारित कार्यक्षेत्र (Full View):** बाईं ओर संपूर्ण नेविगेशन पैनल और दाईं ओर लाइव टेलीमेट्री व परीक्षण कार्यक्षेत्र एक साथ सक्रिय।
- **नया "निओन रेड" थीम (Neon Red in Black & Blue Theme):**
  - **रंग संरचना (Color Composition):**
    - **प्राथमिक रंग (Primary):**  (चमकदार निओन रेड - बटन, सक्रिय टैब एवं बॉर्डर हाइलाइट)
    - **पृष्ठभूमि (Background):**  (गहरा जेट ब्लैक - आंखों के आराम हेतु)
    - **सतह एवं कार्ड (Surface & Card):**  और  (गहरे नीले-काले कंट्रास्ट कार्ड)
    - **द्वितीयक एक्सेंट (Accent):**  (इलेक्ट्रिक साइबर ब्लू - डेटा हाइलाइट्स एवं मेट्रिक्स)
    - **चमक व बॉर्डर (Glow & Border):**  (सॉफ्ट निओन रेड परिधि)
  - **सक्रिय करने की विधि:**
    1. शीर्ष हेडर में **Theme** बटन पर क्लिक करें या साइडबार में **🎨 Pick a Theme Color** पर क्लिक करें।
    2. पैलेट पिकर में पहले गोल स्वैच पर क्लिक करें (लाल-काला-नीला ट्राइ-कलर स्वैच)।
    3. पूरा पोर्टल तुरंत **Neon Red + Black + Blue** में परिवर्तित हो जाता है।

---

## 17. तकनीकी सहायता एवं संपर्क (Support & Verification Hotline)

- **राष्ट्रीय हेल्पलाइन:**  (टोल-फ्री)
- **तकनीकी सहायता डेस्क:**  (24x7 एक्टिव)
- **ईमेल:**  | 
- **आधिकारिक रिपॉजिटरी:** [GitHub - OIML-NAWI-METROLOGY-TESTER-R-76](https://github.com/mr-vishal-singh01/OIML-NAWI-METROLOGY-TESTER-R-76)
- **पोर्टल संस्करण:** PrecisionX v1.4 (SIH26035 Sovereign Release)
