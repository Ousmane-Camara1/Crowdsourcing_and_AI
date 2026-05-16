# Trust-Centric Voice AI Survey Prototype

## roject Overview
This repository contains the functional, interactive voice AI survey prototype developed for **Track 2: Trust and Response**. The objective of this system is to evaluate how real-time interaction design, consent framing, and conversational logic affect survey uptake and data honesty.

This software represents **Part II: Functional Design**, translating the human-centered trust factors from Part I (Legitimacy, Transparency, Autonomy, Privacy, Psychological Safety, Cognitive Ease) into executable logic gates. 

---

## 📂 Repository Structure
```text
trust_survey_project/
├── data/
│   ├── community_health.json          # Modular data schema for health track
│   └── university_mental_health.json  # Data schema for campus case example
├── logs/
│   └── dropoff_metrics.csv            # Automated trust & telemetry data logs
├── app.py                             # Gradio web application dashboard
├── main.py                            # Core AI survey loop & adaptive workflows
├── utils.py                           # Hardware STT/TTS audio pipelines (Kokoro AI)
└── requirements.txt                   # Software dependency manifest
