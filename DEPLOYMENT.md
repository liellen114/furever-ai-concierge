# FurEver AI Concierge — Deployment Notes

This document describes the deployment plan and fallback strategy for FurEver AI Concierge.

## Current Public Project Link

The current public project link is the GitHub repository:

    https://github.com/liellen114/furever-ai-concierge

The app can be run locally from this repository using the setup instructions in `README.md`.

## Current Working Deployment Mode

The current prototype runs as a local Streamlit app:

    python3 -m streamlit run app.py

This local app demonstrates:

- multi-agent workflow
- human-in-the-loop review
- timeline storage
- story generation
- safety-aware sitter sharing
- observability trace logs
- demo reset/load controls

## Why Local Streamlit Is Used

The current version prioritizes a stable capstone demo.

The app uses local Python functions to simulate agent behavior and local JSON files for runtime data. This keeps the demo reliable and avoids dependency failures during evaluation.

## Planned Agent Runtime Deployment

A future version may be deployed using:

- agents-cli
- Google agent runtime
- Gemini API
- Cloud Trace

The intended deployment architecture is:

    User
    → Streamlit or web interface
    → Agent workflow
    → Memory Agent
    → Evaluation Agent
    → Human Review Router
    → Timeline storage
    → Story Agent / Safety Agent
    → Cloud Trace observability

## agents-cli Deployment Status

agents-cli / agent runtime deployment is planned as a future deployment path.

The current repository is structured to support this future path because it separates:

- app interface: `app.py`
- agent logic: `agents.py`
- workflow routing: `workflow.py`
- local storage: `storage.py`
- trace logging: `trace_logger.py`
- prompt design: `PROMPTS.md`
- Gemini integration plan: `GEMINI_INTEGRATION.md`

## Fallback Submission Strategy

If agents-cli deployment is not feasible within the capstone timeline, the fallback submission is:

1. Public GitHub repository
2. Local Streamlit run instructions
3. Demo video showing the app running
4. README architecture explanation
5. Observability evidence from the local trace log

This fallback still demonstrates the required course concepts:

- multi-agent workflow
- agent skills
- human-in-the-loop review
- safety-aware sharing
- observability
- deployment readiness through public GitHub packaging

## Local Run Command

After cloning the repository and installing dependencies, run:

    python3 -m streamlit run app.py

Then open:

    http://localhost:8501

## Notes for Reviewers

The app does not require a real API key for the current demo mode.

Gemini integration is documented in `GEMINI_INTEGRATION.md`, but the working prototype uses local demo agents for reliability.