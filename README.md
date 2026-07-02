# FurEver AI Concierge

## Track

Concierge Agents

## One-sentence summary

FurEver AI Concierge is a privacy-aware multi-agent assistant that turns pet memories into a structured life timeline, generates pet life stories, and creates sitter-safe care summaries using human-in-the-loop review for uncertain or sensitive information.

## Architecture

FurEver AI Concierge is structured as a privacy-aware multi-agent workflow.

The prototype currently uses local Python functions to simulate the agents. This keeps the demo stable while preserving the same architecture that could later be connected to Gemini, Google AI Studio, ADK, agents-cli, or a deployed agent runtime.

### Agent Workflow

User memory note  
→ Memory Agent  
→ Evaluation Agent  
→ Decision Router  
→ Approved Timeline or Human Review Queue  
→ Story Agent / Safety Agent  
→ Observable trace log

### Agent Graph

```text
┌────────────────────┐
│ User Memory Input   │
│ note / photo text   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Memory Agent        │
│ Extracts structured │
│ pet memory          │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Evaluation Agent    │
│ Scores confidence,  │
│ sensitivity, risk   │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Decision Router     │
│ Routes memory       │
└──────┬─────────┬───┘
       │         │
       ▼         ▼
┌─────────────┐  ┌────────────────────┐
│ Timeline    │  │ Human Review Queue  │
│ Approved    │  │ Edit / approve /    │
│ memories    │  │ reject memories     │
└──────┬──────┘  └─────────┬──────────┘
       │                   │
       │                   ▼
       │          ┌────────────────────┐
       │          │ Approved Timeline   │
       │          │ after human review  │
       │          └─────────┬──────────┘
       │                    │
       └──────────┬─────────┘
                  ▼
        ┌────────────────────┐
        │ Downstream Agents   │
        │ Story + Safety      │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Trace Log           │
        │ Observability       │
        └────────────────────┘

## Agents

### 1. Memory Agent

Role: Extracts structured pet memories from user notes.

Input example:
"RuRu loved his first beach walk today. He was scared of the waves at first but became playful later."

Output example:
- title: First Beach Walk
- pet_name: RuRu
- event_type: outdoor memory
- emotion: happy and playful
- care_relevance: RuRu may enjoy calm outdoor play near water
- confidence: 0.85

### 2. Evaluation Agent

Role: Checks confidence, sensitivity, and trust score.

The Evaluation Agent decides whether a memory should be saved automatically or sent to human review.

Output example:
- trust_score: 0.86
- sensitivity: low
- decision: save_to_timeline
- reason: The memory is clear and does not contain sensitive owner information.

Decision rule:
If trust_score is 0.75 or higher and sensitivity is low, save the memory to the timeline.
Otherwise, send the memory to human review.

### 3. Story Agent

Role: Generates a pet life story using only approved timeline memories.

The Story Agent should not use memories that are still waiting for human review.

Output example:
"RuRu’s story began with small moments of trust and curiosity. One of his happiest memories was his first beach walk, where he slowly became more confident around the waves and enjoyed playful outdoor time."

### 4. Safety Agent

Role: Creates a sitter-safe share card.

The Safety Agent removes or avoids sharing sensitive details before information is shared with a sitter.

The Safety Agent should remove or avoid:
- owner address
- phone number
- exact daily routine
- private medical details
- financial information
- unsafe sitter instructions

Output example:
"Sitter-safe care summary: RuRu enjoys calm outdoor play and may need reassurance around new environments. He responds well to gentle encouragement and familiar toys. Sensitive owner information has been removed."

## Decision Rule and Human Review Routing

FurEver AI Concierge uses a simple trust and safety routing rule.

After the Memory Agent extracts a structured memory, the Evaluation Agent checks:

- trust score
- confidence
- sensitivity level
- missing information
- whether the content is safe to save or share

The router then follows this rule:

```text
If trust_score >= 0.75 and sensitivity == "low":
    save the memory to the timeline
else:
    send the memory to the human review queue

## Human-in-the-loop

If a memory has low confidence or contains sensitive information, it is not saved automatically. Instead, it is sent to a review queue where the user can approve, edit, or reject it.

## Course Concepts Demonstrated

1. Multi-agent ADK graph workflow
2. Agent skills: memory capture, timeline building, story generation, trust scoring
3. Human-in-the-loop review
4. Deployment with agents-cli, if feasible
5. Observability with Cloud Trace, if feasible

## Technical Stack

This project uses a beginner-friendly stack:

- Python for the agent workflow
- Streamlit for the web app interface
- Local rule-based agent simulation for the current working prototype
- Gemini API integration plan for future AI agent responses
- Local JSON files for timeline and review queue storage
- GitHub for public code sharing
- Google AI Studio for prompt testing
- agents-cli / agent runtime for deployment if feasible
- Cloud Trace or local trace logs for observability evidence
- Optional photo/video uploads as supporting memory media
- Photo EXIF date extraction when metadata is available
- Manual date and location input for user confirmation

See `PROMPTS.md`, `GEMINI_INTEGRATION.md`, and `DEPLOYMENT.md` for the agent prompt design, future Gemini API integration plan, and deployment/fallback strategy.

## Why This Stack

The project focuses on demonstrating agent design rather than building a complex production system. Streamlit and local JSON storage allow the prototype to stay simple, while the multi-agent workflow demonstrates the core course concepts.

## Minimum Working Demo

The minimum working demo will show one complete agent workflow:

1. The user enters a pet memory note.
2. The Memory Agent extracts a structured memory.
3. The Evaluation Agent checks confidence, sensitivity, and trust score.
4. If the memory is safe and high confidence, it is saved to the timeline.
5. If the memory is uncertain or sensitive, it is sent to human review.
6. The user can approve or reject memories in the review queue.
7. The Story Agent generates a life story using only approved timeline memories.
8. The Safety Agent generates a sitter-safe share card with sensitive details removed.

## Media Memory Support

FurEver supports text-based memories with optional photo or video attachments.

The app is designed to encourage pet owners to organize meaningful memories, not simply use the app as a secondary photo album. For this reason, every memory requires:

- a written pet memory
- a date source

The date source can come from:

- a manually selected calendar date
- an approximate period entered by the user
- photo date metadata, if available from the uploaded image

Uploaded media is treated as supporting evidence for the written memory.

The current prototype extracts photo date metadata when available, but does not extract GPS/location metadata. GPS extraction is planned as a future improvement because it requires additional privacy controls and user confirmation.

## Demo Success Criteria

The demo is successful if it can show:

- One safe memory being saved automatically to the timeline.
- One sensitive or uncertain memory being routed to human review.
- One approved timeline being used to generate a pet life story.
- One sitter-safe share card being generated from approved information only.

## Out of Scope

To keep the capstone realistic within 18 hours, this project will not include:

- User login or account management
- Real sitter marketplace matching
- Real playdate scheduling
- Payments or booking system
- Maps or location tracking
- Full production database
- Mobile app
- Real social media sharing
- Complex photo album management
- Veterinary diagnosis or medical advice

## Setup Instructions

Clone the repository:

    git clone <your-repository-url>
    cd furever-ai-concierge

Install dependencies:

    python3 -m pip install -r requirements.txt

Run the app:

    python3 -m streamlit run app.py

Then open the local Streamlit URL shown in Terminal, usually:

    http://localhost:8501

## Demo Instructions

For a clean demo:

1. Open the app.
2. Go to Demo Controls.
3. Click Reset Demo Data.
4. Click Load Demo Data.
5. Go to Timeline to view approved RuRu memories.
6. Go to Human Review to review a sensitive memory.
7. Edit the sensitive memory and approve it.
8. Go to Life Story and generate RuRu's story.
9. Go to Sitter Share and generate a sitter-safe care card.
10. Go to Observability to inspect the trace log.

## Local Data Files

The app stores local demo data in:

    data/timeline.json
    data/review_queue.json
    data/trace_log.json

These files are ignored by Git because they are local runtime data.

## Environment Variables

A future Gemini-powered version can use:

    GOOGLE_API_KEY=your_api_key_here

Use .env.example as a template.

Do not commit real API keys to GitHub.