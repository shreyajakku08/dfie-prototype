# 🛡️ DFIE - Digital Footprint Intelligence Engine

> An elite, interactive cybersecurity tool designed to highlight the dangerous realities of open-source intelligence (OSINT) and identity trace mapping. Built for speed, impact, and education.

![DFIE Dashboard](https://img.shields.io/badge/Status-Hackathon_Prototype-purple.svg) ![Python](https://img.shields.io/badge/Backend-Flask-blue.svg) ![JS](https://img.shields.io/badge/Frontend-Vanilla_JS-yellow.svg)

---

## 🚀 The Core Vision
The **Digital Footprint Intelligence Engine (DFIE)** demonstrates how quickly a digital identity can be compromised utilizing only publicly available data spanning from credential leaks to active platform presences, and even embedded metadata in standard media files.

Unlike traditional OSINT scrapers that output unreadable JSON feeds in a terminal, **DFIE gamifies security** by automatically scoring threats into an interactive, visually stunning cyber-dashboard with remediation loops prioritizing human behavioral change.

## 🎯 Key Features

- **🌐 Deep Platform Reconnaissance**: Queries over known social media, developer, and forum platforms dynamically linking usernames directly to footprints.
- **🚨 Automated Breach Mapping**: Synchronizes known leak credentials against target endpoints identifying the exact vector of compromise.
- **🗺️ GPS EXIF Extraction**: Strips metadata directly from user-uploaded imagery to demonstrate the severe privacy implications of GPS-tagged media. Integrates zero-click Google Maps tracking.
- **🤖 AI Security Insight**: A simulated LLM-style heuristics engine evaluates the final matrix score and types out a summary judgment instantly based on threat levels.
- **✅ Gamified Remediation Engine**: Interactive Checklist tracking live points mitigated as users physically check off security tasks (e.g. changing passwords, rotating keys) culminating in a dynamic Dashboard Risk Score reduction.

## 💻 Tech Stack
* **Frontend**: Vanilla ES6+ Javascript, Native CSS3 (Glassmorphism UI), Chart.js, HTML5
* **Backend**: Python 3.x, Flask (RESTful Endpoints)
* **Libraries**: `requests`, `Pillow` (Exif parsing), `Werkzeug`

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shreyajakku08/dfie-prototype.git
   cd dfie-prototype
   ```

2. **Setup your Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Core Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Engine:**
   ```bash
   python app.py
   ```
   *Navigate to `http://localhost:5000` in your web browser to access the dashboard.*

---

## 🏆 Hackathon Pitch Script

When presenting DFIE to Judges, follow this flow for maximum WOW-factor:
1. **The Hook**: Explain the difference between *knowing* your data is online and *seeing* exactly how exposed it is visually.
2. **The Demo**: Type a fake email into the search bar. Point to the artificial "loading steps" tracking exactly where the intelligence is being sourced.
3. **The Reveal**: Let the dashboard initialize. Direct attention to the **AI Security Insight** typing itself onto the screen, summarizing the threat.
4. **The Shock Factor**: Upload an image containing EXIF data. Watch the layout turn **CRITICAL RED**, extracting exact coordinates to Google Maps.
5. **The Solution**: Don't just show problems; show solutions. Rapidly click through the **Remediation Checkboxes**, pointing back up to the **Digital Risk Score Gauge** visibly popping and decreasing live to a safe, secured level.

---

### *Disclaimer: Educational purposes only. DFIE simulates deep-scanning mechanisms for the benefit of digital hygiene and public safety education.*
