# FurEver AI Concierge — Gemini Integration Plan

The current prototype uses local Python functions to simulate a multi-agent workflow. This keeps the capstone demo stable and easy to run.

A future version can connect the Memory Agent, Evaluation Agent, Story Agent, and Safety Agent to Gemini through Google AI Studio or the Gemini API.

---

## Why Gemini Is Optional in This Prototype

The current app already demonstrates the core agent architecture:

- Memory Agent
- Evaluation Agent
- Decision Router
- Human-in-the-loop review
- Timeline storage
- Story Agent
- Safety Agent
- Observability trace logging

Gemini can improve the natural-language extraction and generation quality, but the workflow logic does not depend on Gemini.

---

## Environment Variable

A Gemini-powered version would use:

```bash
GOOGLE_API_KEY=your_api_key_here