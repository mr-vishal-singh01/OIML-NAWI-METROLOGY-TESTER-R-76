# PrecisionX — OIML R-76 Sovereign Legal Metrology Workbench
## उपयोगकर्ता मार्गदर्शिका एवं परिचालन नियमावली (User Manual & How-to-Use Guide)

**National Sovereign Metrology Verification & Automated Sealing Platform**  
*Under the Statutory Mandate of Section 15, Legal Metrology Act, 2009 & OIML R 76-1:2006 (E)*  
*Ministry of Consumer Affairs, Food & Public Distribution | Department of Consumer Affairs, Government of India*

---

## विषय सूची (Table of Contents)

1. [प्रणाली अवलोकन (System Overview & Public Telemetry)](#1-प्रणाली-अवलोकन-system-overview--public-telemetry)
2. [भूमिका आधारित अभिगम द्वार (Multi-Role Authentication & Access Gate)](#2-भूमिका-आधारित-अभिगम-द्वार-multi-role-authentication--access-gate)
3. [निरीक्षक कार्यक्षेत्र एवं सत्यापन कतार (Inspector Workbench & Verification Queue)](#3-निरीक्षक-कार्यक्षेत्र-एवं-सत्यापन-कतार-inspector-workbench--verification-queue)
4. [उपकरण एवं प्रयोगशाला सेटअप (Instrument & Laboratory Setup)](#4-उपकरण-एवं-प्रयोगशाला-सेटअप-instrument--laboratory-setup)
5. [फॉर्म 1: वजन निष्पादन परीक्षण (Form 1: Weighing Performance Test - Clause A.4.4)](#5-फॉर्म-1-वजन-निष्पादन-परीक्षण-form-1-weighing-performance-test---clause-a44)
6. [फॉर्म 3: कोना विलक्षणता परीक्षण (Form 3: Corner Eccentricity Test - Clause 3.6.2 & A.4.7)](#6-फॉर्म-3-कोना-विलक्षणता-परीक्षण-form-3-corner-eccentricity-test---clause-362--a47)
7. [फॉर्म 5: पुनरावृत्ति परीक्षण (Form 5: Repeatability Test - Clause 3.6.1 & A.4.10)](#7-फॉर्म-5-पुनरावृत्ति-परीक्षण-form-5-repeatability-test---clause-361--a410)
8. [फॉर्म 15: सॉफ्टवेयर परीक्षण एवं चेकसम (Form 15: Software Examination - WELMEC 7.2)](#8-फॉर्म-15-सॉफ्टवेयर-परीक्षण-एवं-चेकसम-form-15-software-examination---welmec-72)
9. [एम.पी.ई. तुरही वक्र सहनशीलता गलियारा (MPE Trumpet Tolerance Corridor - Table 6)](#9-एमपीई-तुरही-वक्र-सहनशीलता-गलियारा-mpe-trumpet-tolerance-corridor---table-6)
10. [थोक सीएसवी डेटा अंतर्ग्रहण (Batch CSV Ingestion Engine)](#10-थोक-सीएसवी-डेटा-अंतर्ग्रहण-batch-csv-ingestion-engine)
11. [डिजिटल भंडार एवं आईएसओ पीडीएफ/ए-3 (Digital Repository & ISO 19005-3 PDF/A-3)](#11-डिजिटल-भंडार-एवं-आईएसओ-पीडीएफए-3-digital-repository--iso-19005-3-pdfa-3)
12. [ऑफ़लाइन एड25519 क्यूआर कोड सत्यापन (Offline Ed25519 Cryptographic QR Verification)](#12-ऑफ़लाइन-एड25519-क्यूआर-कोड-सत्यापन-offline-ed25519-cryptographic-qr-verification)
13. [विधिक मापविज्ञान राजपत्र अन्वेषक (Legal Metrology Gazette Explorer - 91 Acts)](#13-विधिक-मापविज्ञान-राजपत्र-अन्वेषक-legal-metrology-gazette-explorer---91-acts)
14. [व्यवस्थापक नियंत्रण केंद्र (Admin Control Center & Lab Director Authorization)](#14-व्यवस्थापक-नियंत्रण-केंद्र-admin-control-center--lab-director-authorization)
15. [नेविगेशन साइडबार एवं थीम अनुकूलन (Sidebar Controls & Neon Red Theme Customization)](#15-नेविगेशन-साइडबार-एवं-थीम-अनुकूलन-sidebar-controls--neon-red-theme-customization)

---

## 1. प्रणाली अवलोकन (System Overview & Public Telemetry)

पोर्टल के लैंडिंग पृष्ठ पर राष्ट्रीय विधिक मापविज्ञान प्रभाग का आधिकारिक सार्वजनिक दृश्य उपलब्ध है।

### 1.1 मुख्य पृष्ठ एवं सूचना पट्टिका (Hero Masthead & Advisory Ticker)
![Portal Hero Masthead](screenshots/Screenshot%20from%202026-10-22%2018-45-49.png)
- **शीर्ष बैनर (Top Header):** भारत सरकार का प्रतीक, मंत्रालय का नाम, स्मार्ट इंडिया हैकाथॉन 2026 (SIH26035) बैनर और लाइव सर्वर सिंक स्थिति।
- **ताज़ा समाचार टिकर (What's New Ticker):** विधिक मापविज्ञान अधिनियम, आवश्यक वस्तु अधिनियम और नवीनतम सरकारी अधिसूचनाएं स्वचालित रूप से स्क्रॉल होती हैं। इसे पॉज/प्ले बटन से नियंत्रित किया जा सकता है।
- **त्वरित नियंत्रण (Quick Controls):** भाषा बदलने हेतु `🌐 हिंदी / English` टॉगल, थीम पैलेट पिकर `🎨 Theme` और फ़ुलस्क्रीन `⛶ Fullscreen` बटन शीर्ष पर उपलब्ध हैं।

### 1.2 प्रेसिजनएक्स का वैधानिक अधिदेश (Statutory Mandate: What is PrecisionX?)
![What is PrecisionX](screenshots/Screenshot%20from%202026-10-22%2018-46-13.png)
- **उद्देश्य:** धारा 15 विधिक मापविज्ञान अधिनियम 2009 और OIML R 76-1:2006 मानक के अंतर्गत गैर-स्वचालित तौल उपकरणों (NAWI) का वास्तविक समय सत्यापन।
- **सुरक्षा विशेषताएं:** Ed25519 डिजिटल हस्ताक्षर, पीटीबी डीसीसी (PTB DCC) एक्सएमएल स्कीमा, आईएसओ 19005-3 पीडीएफ/ए-3 कंटेनर और वेल्मेक 7.2 सॉफ्टवेयर सीलिंग।

### 1.3 राष्ट्रीय सांख्यिकी एवं जोखिम हीटमैप (Milestones & Regional Risk Heatmap)
![PrecisionX Milestones & Heatmap](screenshots/Screenshot%20from%202026-10-22%2018-47-22.png)
- **मील के पत्थर (Milestones):** 18,527+ सत्यापित उपकरण, 142 सक्रिय निरीक्षक, 98.4% राष्ट्रीय अनुपालन दर और 100% वेल्मेक 7.2 अखंडता।
- **क्षेत्रीय प्रवर्तन विसंगति हीटमैप (Regional Anomaly Heatmap):** मुंबई एपीएमसी यार्ड, दक्षिणी दिल्ली व्यापारिक केंद्र आदि में वास्तविक समय उल्लंघन निगरानी।
- **सटीकता वर्ग अनुपालन:** Class I (विश्लेषणात्मक 99.4%), Class II (बुलियन 98.1%), Class III (वाणिज्यिक खुदरा 95.8%), Class IIII (धर्मकांटा / वेइब्रिज 96.2%)।

### 1.4 क्षेत्राधिकार निगरानी नोड्स एवं विफलता विश्लेषण (Monitored Nodes & Primary Failures)
![Monitored Nodes](screenshots/Screenshot%20from%202026-10-22%2018-48-04.png)
- **प्रमुख क्षेत्राधिकार नोड्स:** बेंगलुरु अनाज मंडी, पुणे हड़पसर औद्योगिक क्षेत्र, अहमदाबाद कालूपुर मंडी, चेन्नई पोर्ट कंटेनर टर्मिनल, कोलकाता बड़ाबाजार, हैदराबाद बेगम बाजार।
- **विफलता के प्राथमिक कारण:** तालिका 6 एम.पी.ई. सहनशीलता उल्लंघन (52%), कोने का विलक्षणता भार विचलन (24%), शून्य रिटर्न सेंसर बहाव (15%), वायर सील छेड़छाड़ (9%)।

### 1.5 कोर तकनीकी स्तंभ एवं वैधानिक प्रकटीकरण (Core Engine Pillars)
![Core Engine Pillars](screenshots/Screenshot%20from%202026-10-22%2018-48-27.png)
- **तकनीकी स्तंभ:** OIML R-76 MPE इंजन, Ed25519 क्रिप्टोग्राफी, PTB DCC & PDF/A-3, और WELMEC 7.2 विधिक प्रासंगिक सॉफ्टवेयर सीलिंग।
- **वैधानिक प्रकटीकरण:** धारा 44, विधिक मापविज्ञान अधिनियम 2009 के अंतर्गत अनधिकृत छेड़छाड़ दंडनीय अपराध है।

---

## 2. भूमिका आधारित अभिगम द्वार (Multi-Role Authentication & Access Gate)

### 2.1 बहु-भूमिका लॉगिन कार्ड (Multi-Role Sign-In Card)
![Inspector Sign-In](screenshots/Screenshot%20from%202026-10-22%2018-46-49.png)
- **तीन अभिगम भूमिकाएं:**
  1. **Inspector / Officer:** पूर्ण OIML परीक्षण मॉड्यूल, एम.पी.ई. गणना और डिजिटल सीलिंग कार्यक्षेत्र।
  2. **Verified Citizen:** उपभोक्ता बिना लॉगिन के सीधे सार्वजनिक सत्यापन पोर्टल से क्यूआर कोड और वजन प्रमाणपत्र की प्रामाणिकता जांच सकते हैं।
  3. **Trader / Mandi:** व्यापारी अपने प्रतिष्ठान के तौल पैमानों का आवधिक सत्यापन शेड्यूल देख सकते हैं।
- **क्रेडेंशियल्स:** विभागीय ईमेल (`inspector@metrology.gov.in`), अधिकारी आईडी (`GOV-IN-7842`), गुप्त पासफ़्रेज़, और प्रयोगशाला क्षेत्राधिकार चयन।

### 2.2 दो-चरणीय प्रमाणीकरण (Two-Factor Authentication - 2FA/TOTP)
![2FA Authentication](screenshots/Screenshot%20from%202026-10-22%2018-49-39.png)
- **सुरक्षा चुनौती:** पंजीकृत मोबाइल नंबर पर 6-अंकीय ओटीपी कोड भेजा जाता है।
- **मूल्यांकन हेतु:** "Judge Demo Passcode: 784206" के पास **Auto-Fill Code** बटन दबाकर तुरंत कोड दर्ज करें और **Verify Passcode & Enter Portal** पर क्लिक करें।

### 2.3 हेडर एवं साइडबार नियंत्रण (Sidebar Header Controls)
![Sidebar Toggle Controls](screenshots/Screenshot%20from%202026-10-22%2018-51-34.png)
- **मेनू खोलना (Turn ON):** शीर्ष हेडर में बाईं ओर स्थित ऐप आइकन (PrecisionX Logo) पर क्लिक करें।
- **मेनू बंद करना (Turn OFF):** साइडबार के शीर्ष पर दाईं ओर स्थित बाण बटन (`<<`) पर क्लिक करें।

---

## 3. निरीक्षक कार्यक्षेत्र एवं सत्यापन कतार (Inspector Workbench & Verification Queue)

### 3.1 परिचालन डैशबोर्ड एवं सत्र अवलोकन (Operational Dashboard)
![Inspector Dashboard](screenshots/Screenshot%20from%202026-10-22%2019-10-08.png)
- **सत्र स्थिति:** सत्र आईडी `SESS-2026-001 #1`, समीक्षा जीवनचक्र `DRAFT`, जीरो-एरर `0 g`, और WELMEC 7.2 LRS सील `SHA-256 VALID`।
- **अधिकारी प्रोफ़ाइल:** निरीक्षक आर. वर्मा, आईडी `GOV-IN-7842`, विधिक मापविज्ञान विभाग, महाराष्ट्र।
- **कार्य सारांश:** 4 सौंपे गए कार्य, 0 लंबित, 4 पूर्ण और सीलबंद।

### 3.2 सक्रिय सत्यापन कतार (Verification Task Queue)
![Verification Queue](screenshots/Screenshot%20from%202026-10-22%2019-10-55.png)
- **कतारबद्ध प्रतिष्ठान:**
  - `TSK-2026-0104`: एपेक्स फॉर्मूलेशन (Entris II Precision, Class II, 620g) - तत्काल (URGENT)
  - `TSK-2026-0101`: श्री कृष्णा एग्रो ट्रेडर्स (DS-215 Commercial, Class III, 15000g) - उच्च प्राथमिकता
  - `TSK-2026-0102`: झावेरी गोल्ड एंड ऑर्नामेंट्स (ME204 Analytical, Class I, 220g) - उच्च प्राथमिकता
  - `TSK-2026-0103`: भारत फूड प्रोविजन्स (AW-30 Industrial Bench, Class III, 30000g) - सामान्य
- प्रत्येक कार्य के साथ प्रत्यक्ष प्रमाणपत्र देखने हेतु `Cert TR-2026-xxxx` लिंक उपलब्ध है।

### 3.3 राष्ट्रीय निगरानी एवं एआई एज ऑडिट कंसोल (AI Edge Surveillance Console)
![AI Edge Console](screenshots/Screenshot%20from%202026-10-22%2019-12-08.png)
- **48 एज नोड्स कनेक्टेड:** सभी राज्य संदर्भ मानक प्रयोगशालाओं (RRSL) की लाइव टेलीमेट्री निगरानी।
- **99.82% सटीकता दर:** शून्य गलत-सकारात्मक जब्ती रिकॉर्ड। Ed25519 क्रिप्टोग्राफ़िक रूप से सीलबंद।

---

## 4. उपकरण एवं प्रयोगशाला सेटअप (Instrument & Laboratory Setup)

### 4.1 उपकरण विवरण एवं पर्यावरणीय परिस्थितियां (NAWI OIML R-76 Setup)
![Instrument Setup](screenshots/Screenshot%20from%202026-10-22%2019-19-10.png)
- **उपकरण पैरामीटर (Instrument Parameters):**
  - निर्माता (Manufacturer): `ABC`
  - मॉडल (Model): `ABC-123`
  - सटीकता वर्ग (Accuracy Class): `Class III (Medium)`
  - सीरियल नंबर: `1-125 210-EB-123-1`
  - अधिकतम क्षमता (Max): `30 kg`
  - न्यूनतम क्षमता (Min): `0.2 kg`
  - सत्यापन पैमाना अंतराल ($e$): `0.01 kg`
  - वास्तविक पैमाना अंतराल ($d$): `0.01 kg`
- **पर्यावरणीय डेटा (Laboratory Conditions):**
  - तापमान: `23.2 °C`
  - सापेक्ष आर्द्रता: `50.0 %`
  - वायुमंडलीय दबाव: `1013.25 hPa`
  - प्रयोगशाला स्थान: `GATC Lab, Mumbai`
- डेटा भरने के बाद **Proceed to Testing →** पर क्लिक करें।

---

## 5. फॉर्म 1: वजन निष्पादन परीक्षण (Form 1: Weighing Performance Test - Clause A.4.4)

### 5.1 शून्य संदर्भ रीडिंग एवं सहिष्णुता स्थिति (Clause A.4.4.3 Zero Reference)
![Form 1 Zero Reference](screenshots/Screenshot%20from%202026-10-22%2019-13-17.png)
- **शून्य त्रुटि निर्धारण:** $E_0 = P_0 - L_0$ का उपयोग बाद के सभी लोड चरणों को संतुलित करने हेतु किया जाता है।
- **लाइव स्केल अंतर्ग्रहण:** `Live Ingest from Scale (MT-SICS)` बटन द्वारा सीधे डिजिटल वेइंग स्केल से सीरियल डेटा प्राप्त किया जा सकता है।

### 5.2 वजन परीक्षण चरण एवं एम.पी.ई. मूल्यांकन (Accuracy Observation Table)
![Form 1 Steps](screenshots/Screenshot%20from%202026-10-22%2019-19-42.png)
- **परीक्षण लोड श्रृंखला (Test Loads):**
  - चरण 1: संदर्भ भार `0.1 kg`, संकेत `0.1 kg`, त्रुटि `+0.000 kg`, MPE `±0.005 kg` → **PASS**
  - चरण 2: संदर्भ भार `2.5 kg`, संकेत `2.5 kg`, त्रुटि `+0.000 kg`, MPE `±0.005 kg` → **PASS**
  - चरण 3: संदर्भ भार `5.0 kg`, संकेत `5.001 kg`, त्रुटि `+0.001 kg`, MPE `±0.010 kg` → **PASS**
  - चरण 4: संदर्भ भार `10.0 kg`, संकेत `10.002 kg`, त्रुटि `+0.002 kg`, MPE `±0.010 kg` → **PASS**
  - चरण 5: संदर्भ भार `15.0 kg`, संकेत `15.003 kg`, त्रुटि `+0.003 kg`, MPE `±0.015 kg` → **PASS**
- सभी चरण OIML तालिका 6 के अधिकतम अनुमेय त्रुटि गलियारे में उत्तीर्ण होने पर **Evaluate & Generate Report** सक्रिय होता है।

---

## 6. फॉर्म 3: कोना विलक्षणता परीक्षण (Form 3: Corner Eccentricity Test - Clause 3.6.2 & A.4.7)

### 6.1 पांच-बिंदु पैन स्कीमेटिक (Scale Pan 5-Point Schematic)
![Form 3 Eccentricity](screenshots/Screenshot%20from%202026-10-22%2019-21-55.png)
- **परीक्षण भार:** $1/3 \text{ Max} = 5000\text{ g}$ (अनुमेय सहिष्णुता $\pm 5.0\text{ g}$)।
- **लक्ष्य स्थान (Target Positions):**
  1. केंद्र (Center)
  2. आगे-बाएं (Front-Left)
  3. पीछे-बाएं (Back-Left)
  4. पीछे-दाएं (Back-Right)
  5. आगे-दाएं (Front-Right)

### 6.2 विलक्षणता अवलोकन तालिका (Eccentricity Table)
![Form 3 Table](screenshots/Screenshot%20from%202026-10-22%2019-22-12.png)
- प्रत्येक कोने पर 5000g का भार रखकर अतिरिक्त लोड ($\Delta L$) दर्ज करें और **Submit Corner Reading** पर क्लिक करें। सिस्टम स्वतः विचलित त्रुटि ($E_c$) की गणना करता है।

---

## 7. फॉर्म 5: पुनरावृत्ति परीक्षण (Form 5: Repeatability Test - Clause 3.6.1 & A.4.10)

![Form 5 Repeatability](screenshots/Screenshot%20from%202026-10-22%2019-22-38.png)
- **दोहरी श्रृंखला परीक्षण:**
  - **श्रृंखला A:** ~50% Max ($7,500\text{ g}$) पर 10 क्रमिक वजन रीडिंग।
  - **श्रृंखला B:** 100% Max ($15,000\text{ g}$) पर 10 क्रमिक वजन रीडिंग।
- **वैधानिक आवश्यकता:** $(I_{\max} - I_{\min}) \leq |MPE|$।
- न्यूनतम, अधिकतम एवं फैलाव (Spread) का वास्तविक समय में स्वतः सत्यापन किया जाता है।

---

## 8. फॉर्म 15: सॉफ्टवेयर परीक्षण एवं चेकसम (Form 15: Software Examination - WELMEC 7.2)

![Form 15 Software Exam](screenshots/Screenshot%20from%202026-10-22%2019-23-27.png)
- **सॉफ्टवेयर अखंडता सत्यापन:**
  - LRS कर्नेल मॉड्यूल: `src/core/nawi_engine.py`
  - SHA-256 डाइजेस्ट: `3037aee5eb6271388fca6fa3079c69e1ddf7e6f4911bbe04e7bb3f99d18d8712`
  - CRC-32 चेकसम: `F0C00FCD`
- **6-बिंदु वेल्मेक चेकलिस्ट:**
  - `SW-01`: सॉफ्टवेयर पहचान एवं संस्करण प्रदर्शन → **COMPLIANT**
  - `SW-02`: क्रिप्टोग्राफ़िक चेकसम / हैश अखंडता → **COMPLIANT**
  - `SW-03`: सॉफ्टवेयर पृथक्करण (विधिक प्रासंगिक बनाम गैर-प्रासंगिक) → **COMPLIANT**
  - `SW-04`: मेट्रोलॉजिकल समायोजन पैरामीटर सुरक्षा (हार्डवेयर जम्पर लॉक) → **COMPLIANT**
  - `SW-05`: ऑडिट ट्रेल / इवेंट काउंटर वृद्धि सत्यापन → **COMPLIANT**
  - `SW-06`: अचानक बिजली कटने पर डेटा प्रतिधारण एवं अखंडता → **COMPLIANT**

---

## 9. एम.पी.ई. तुरही वक्र सहनशीलता गलियारा (MPE Trumpet Tolerance Corridor - Table 6)

### 9.1 इंटरएक्टिव तुरही आवरण वक्र (Interactive Trumpet Curve)
![Trumpet Curve Limits](screenshots/Screenshot%20from%202026-10-22%2019-24-03.png)
- **OIML R 76-1 तालिका 6 चरणबद्ध कोष्ठक (Brackets):**
  - Bracket 1 ($0 \text{ to } 500e$): $\pm 0.5e = \pm 2.5\text{ g}$
  - Bracket 2 ($500e \text{ to } 2000e$): $\pm 1.0e = \pm 5.0\text{ g}$
  - Bracket 3 ($2000e \text{ to Max}$): $\pm 1.5e = \pm 7.5\text{ g}$

### 9.2 वास्तविक समय विचलन एवं मार्जिन ट्रैकिंग (Tolerance Margin Tracking)
![Trumpet Curve Corridor](screenshots/Screenshot%20from%202026-10-22%2019-24-22.png)
- प्रत्येक रिकॉर्ड किए गए वजन का मान तुरही वक्र पर बिंदु के रूप में प्रदर्शित होता है।
- यदि कोई बिंदु लाल सहिष्णुता रेखा से बाहर जाता है, तो उपकरण स्वतः **REJECTED** के रूप में चिह्नित हो जाता है।

---

## 10. थोक सीएसवी डेटा अंतर्ग्रहण (Batch CSV Ingestion Engine)

![CSV Batch Ingestion](screenshots/Screenshot%20from%202026-10-22%2019-25-06.png)
- प्रयोगशाला मापन शीट या सीरियल डंप से सीधे डेटा आयात करने की सुविधा।
- **Load Sample CSV Template** बटन से मानक प्रारूप प्राप्त करें, रिकॉर्ड चिपकाएं, और **Execute Batch Ingestion** दबाएं।

---

## 11. डिजिटल भंडार एवं आईएसओ पीडीएफ/ए-3 (Digital Repository & ISO 19005-3 PDF/A-3)

![Digital Repository](screenshots/Screenshot%20from%202026-10-22%2019-26-39.png)
- **दस्तावेज़ खोज एवं पुनर्प्राप्ति:** रिपोर्ट संख्या, उपकरण नाम या स्थिति (DRAFT, APPROVED, REJECTED) के आधार पर खोजें।
- **दोहरा डाउनलोड:** प्रत्येक सत्यापन हेतु वैध **PDF** और मशीन-पठनीय **XML** (PTB DCC 3.2.1) दोनों उपलब्ध हैं।
- **Master PDF Download:** सम्पूर्ण परीक्षण रिपोर्ट का ISO 19005-3 दीर्घकालिक अभिलेखीय पीडीएफ डाउनलोड करें।

---

## 12. ऑफ़लाइन एड25519 क्यूआर कोड सत्यापन (Offline Ed25519 Cryptographic QR Verification)

### 12.1 डिजिटल हस्ताक्षर एवं क्यूआर कोड निर्माण (Digital Seal Generation)
![Ed25519 Offline QR](screenshots/Screenshot%20from%202026-10-22%2019-28-16.png)
- **प्रमाणपत्र आईडी:** `OIML-RRSL-SESS-2026-001-R1`
- **हस्ताक्षरकर्ता प्राधिकरण:** RRSL-Faridabad / Ministry of Consumer Affairs
- **Ed25519 फिंगरप्रिंट:** `SHA256:9f1522395e39d0c669ce7a593641b35a5ec4db9f66006623d5f606d98cec974d`
- **100% ऑफ़लाइन सत्यापन:** बिना किसी इंटरनेट कनेक्शन के किसी भी सामान्य कैमरा या फील्ड टर्मिनल से क्यूआर स्कैन किया जा सकता है।

### 12.2 फील्ड इंस्पेक्टर सत्यापन टूल एवं जालसाजी परीक्षण (Forgery Simulation)
- फील्ड इंस्पेक्टर टूल में क्यूआर पेलोड दर्ज करके **Verify Cryptographic Signature** पर क्लिक करें।
- **Simulate Forgery:** इस बटन पर क्लिक करने पर पेलोड में 1 बिट का बदलाव होता है और क्रिप्टोग्राफिक इंजन तुरंत **SIGNATURE INVALID - TAMPERING DETECTED** घोषित कर देता है।

---

## 13. विधिक मापविज्ञान राजपत्र अन्वेषक (Legal Metrology Gazette Explorer - 91 Acts)

### 13.1 राजपत्र ग्रिड एवं फ़िल्टर (Gazette Explorer Grid)
![Gazette Explorer](screenshots/Screenshot%20from%202026-10-22%2019-30-04.png)
- **91 सत्यापित राजपत्र:**
  - `G.S.R. 71(E) / 2011`: सातवीं अनुसूची - गैर-स्वचालित तौल उपकरण (OIML R 76-1)
  - `G.S.R. 568(E) / 2026`: अनुसूची IX सत्यापन शुल्क स्लैब एवं टेस्ट लोड प्रतिस्थापन
  - `G.S.R. 905(E) / 2025`: 24-महीने (2-वर्ष) सत्यापन स्टाम्प वैधता का मानकीकरण
  - `G.S.R. 346(E) / 2026`: सरकार द्वारा अनुमोदित परीक्षण केंद्र (GATC) NAWI परीक्षण दायरा
  - `Act No. 18 of 2023`: जन विश्वास अधिनियम (प्रक्रियात्मक उल्लंघनों का वि-अपराधीकरण)
  - `Act No. 8 of 2026 / S.O. 2103(E)`: वि-अपराधीकरण प्रवर्तन एवं न्यायनिर्णायक अधिकारी

### 13.2 प्रत्यक्ष पीडीएफ अभिलेख (Official Gazette Documents)
![Gazette PDF Viewer](screenshots/Screenshot%20from%202026-10-22%2019-30-31.png)
- किसी भी राजपत्र कार्ड पर **Open Official PDF** बटन दबाकर राजपत्र की आधिकारिक मुद्रित प्रति तुरंत पढ़ें।

---

## 14. व्यवस्थापक नियंत्रण केंद्र (Admin Control Center & Lab Director Authorization)

### 14.1 निदेशक प्राधिकरण आवश्यकता (Director Authorization Gate)
![Admin Control Center](screenshots/Screenshot%20from%202026-10-22%2019-31-05.png)
- विधिक मापविज्ञान सीलिंग का अंतिम डिजिटल हस्ताक्षर केवल आरआरएसएल (RRSL) प्रयोगशाला निदेशक या वरिष्ठ वैज्ञानिक द्वारा ही अधिकृत किया जा सकता है।

### 14.2 निदेशक लॉगिन संवाद (Director Login Modal)
![Director Login Modal](screenshots/Screenshot%20from%202026-10-22%2019-31-23.png)
- **Load Demo Credentials (Dr. A. K. Sharma):** जूरी डेमो हेतु 1-क्लिक प्री-फिल बटन।
- **Authenticate & Unlock:** क्लिक करने पर पूर्ण मास्टर प्रशासनिक अधिकार अनलॉक हो जाते हैं।

---

## 15. नेविगेशन साइडबार एवं थीम अनुकूलन (Sidebar Controls & Neon Red Theme Customization)

### 15.1 पूर्ण साइडबार नेविगेशन मेनू (Full Workbench Sidebar)
![Sidebar Modules](screenshots/Screenshot%20from%202026-10-22%2019-32-09.png)
- **श्रेणी 1: वर्कफ़्लो एवं पोर्टल:** Surveillance & AI Dashboard, Pending Tasks Queue, Instrument Setup, Guided Testing Suite.
- **श्रेणी 2: OIML R-76 मॉड्यूल:** Form 1 (Weighing), Form 3 (Eccentricity), Form 5 (Repeatability), Form 15 (Software), Trumpet Curve (MPE).
- **श्रेणी 3: सत्यापन एवं अनुपालन:** CSV Batch Ingestion, PDF/A-3 Vault & PTB DCC, Digital Certificate Repository, Review Report, Ministry Gazette & Acts, Admin Control Center.
- **सेटिंग्स एवं प्रदर्शन:** Language (हिंदी/English), Pick a Theme Color, Fullscreen Canvas (F11).

### 15.2 विस्तारित कार्यक्षेत्र कंसोल (Expanded Workbench Console)
![Expanded Workbench](screenshots/Screenshot%20from%202026-10-22%2019-32-29.png)
- बाईं ओर संपूर्ण नेविगेशन पैनल और दाईं ओर लाइव टेलीमेट्री व कार्यक्षेत्र खुला रहता है।

### 15.3 नया "निओन रेड" थीम (Neon Red in Black & Blue Theme)
उपयोगकर्ता की मांग पर प्रेसिजनएक्स में **Neon Red (निओन रेड)** थीम को ब्लैक और ब्लू के साथ जोड़ा गया है:
- **रंग संरचना (Color Composition):**
  - **प्राथमिक रंग (Primary):** `#ff003f` (चमकदार निओन रेड - बटन, सक्रिय टैब एवं बॉर्डर हाइलाइट)
  - **पृष्ठभूमि (Background):** `#050508` (गहरा जेट ब्लैक - आंखों के आराम हेतु)
  - **सतह एवं कार्ड (Surface & Card):** `#0a0c16` और `#121726` (गहरे नीले-काले कंट्रास्ट कार्ड)
  - **द्वितीयक एक्सेंट (Accent):** `#00d2ff` (इलेक्ट्रिक साइबर ब्लू - डेटा हाइलाइट्स एवं मेट्रिक्स)
  - **चमक व बॉर्डर (Glow & Border):** `rgba(255, 0, 63, 0.40)` (सॉफ्ट निओन रेड परिधि)
- **कैसे सक्रिय करें (How to Activate):**
  1. हेडर में **Theme** बटन पर क्लिक करें या साइडबार में **🎨 Pick a Theme Color** पर क्लिक करें।
  2. पॉपओवर ग्रिड में पहले गोल स्वैच पर क्लिक करें (जिसमें ऊपर लाल, नीचे-बाएं काला और नीचे-दाएं नीला रंग है)।
  3. पूरा पोर्टल तुरंत **Neon Red + Black + Blue** में परिवर्तित हो जाता है और यह प्राथमिकता स्वचालित रूप से सहेजी जाती है।

---

## 16. तकनीकी सहायता एवं संपर्क (Support & Verification Hotline)

- **राष्ट्रीय हेल्पलाइन:** `1800-11-1955` (टोल-फ्री)
- **तकनीकी सहायता डेस्क:** `+91-11-23385566` (24x7 एक्टिव)
- **ईमेल:** `support@precisionx.gov.in` | `inspector@metrology.gov.in`
- **पोर्टल संस्करण:** PrecisionX v1.4 (SIH26035 Sovereign Release)
