import streamlit as st

from workflow import process_memory
from agents import story_agent, safety_agent
from storage import (
    load_timeline,
    load_review_queue,
    approve_review_item,
    reject_review_item,
    reset_demo_data,
    load_demo_data,
    save_uploaded_media,
    extract_photo_date
)
from trace_logger import load_traces, clear_traces, log_trace


st.set_page_config(
    page_title="FurEver AI Concierge",
    page_icon="🐾",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #fffaf3;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.4rem;
    }

    .furever-hero {
        background: linear-gradient(135deg, #fff2d8 0%, #f7e8ff 100%);
        padding: 1.5rem;
        border-radius: 22px;
        border: 1px solid #ead7c3;
        margin-bottom: 1.2rem;
    }

    .furever-card {
        background-color: white;
        padding: 1rem 1.2rem;
        border-radius: 18px;
        border: 1px solid #ead7c3;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(80, 60, 40, 0.05);
    }

    .small-muted {
        color: #6f6259;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="furever-hero">
        <h1>🐾 FurEver AI Concierge</h1>
        <h3>A privacy-aware multi-agent assistant for pet memories, life stories, and sitter-safe care sharing.</h3>
        <p class="small-muted">
        Upload a text memory, photo, or video. FurEver extracts structured memories, checks sensitivity,
        routes uncertain content to human review, and creates approved timeline stories and sitter-safe summaries.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Agents", "4+")
col2.metric("Review", "Human-in-loop")
col3.metric("Storage", "Local JSON")
col4.metric("Evidence", "Trace logs")

st.markdown(
    """
    **Workflow:**  
    User memory note / media → Memory Agent → Evaluation Agent → Decision Router → Timeline or Human Review → Story Agent / Safety Agent
    """
)

tab_add, tab_timeline, tab_review, tab_story, tab_share, tab_trace, tab_demo = st.tabs([
    "Add Memory",
    "Timeline",
    "Human Review",
    "Life Story",
    "Sitter Share",
    "Observability",
    "Demo Controls"
])

st.sidebar.header("Agent Settings")

agent_mode = st.sidebar.selectbox(
    "Agent mode",
    ["Local demo agents", "Gemini API later"],
    index=0
)

st.sidebar.caption(
    "Local demo agents keep the prototype reliable. Gemini API mode is documented for future deployment."
)

with tab_add:
    st.header("Add a Pet Memory")

    st.markdown(
        """
        This tab demonstrates the first part of the agent workflow.

        Users must write a memory and provide a date. They can optionally attach a photo or video as supporting media.

        - The **Memory Agent** extracts a structured memory from the note.
        - The **Evaluation Agent** checks trust score and sensitivity.
        - The **Decision Router** decides whether the memory is safe to save or needs human review.
        """
    )

    st.markdown('<div class="furever-card">', unsafe_allow_html=True)

    note = st.text_area(
        "Write a memory about RuRu: *",
        height=150,
        placeholder="Example: RuRu loved his first beach walk today. He was scared of the waves at first but became playful later."
    )

    col_date, col_location = st.columns(2)

    with col_date:
        memory_date = st.date_input(
            "Memory date *",
            value=None,
            help="Optional. Choose the exact date if you know it."
        )

        memory_period = st.text_input(
            "Or enter an approximate period *",
            placeholder="Example: Summer 2025, puppy stage, first week at home"
        )

    with col_location:
        memory_location = st.text_input(
            "Location",
            placeholder="Example: beach, home, park, vet clinic"
        )

        uploaded_file = st.file_uploader(
        "Optional: add a supporting photo or video",
        type=["png", "jpg", "jpeg", "mp4", "mov"]
    )
    st.caption(
        "Media is optional. FurEver requires a written memory and date so the app supports memory organization, not just photo storage."
    )

    suggested_photo_date = None

    if uploaded_file is not None:
        suggested_photo_date = extract_photo_date(uploaded_file)

        st.caption("Preview of uploaded memory attachment:")

        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file, use_container_width=True)
        elif uploaded_file.type.startswith("video"):
            st.video(uploaded_file)

        if suggested_photo_date:
            st.info(
                f"Suggested date from photo metadata: {suggested_photo_date}. "
                "You can still choose a different date manually."
            )
        elif uploaded_file.type.startswith("image"):
            st.warning(
                "No photo date metadata was found. Please enter the memory date manually if you know it."
            )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Process Memory"):
        missing_required_fields = []

        if not note.strip():
            missing_required_fields.append("written pet memory")

        has_manual_date = memory_date is not None
        has_approximate_period = memory_period.strip() != ""
        has_metadata_date = suggested_photo_date is not None

        if not has_manual_date and not has_approximate_period and not has_metadata_date:
            missing_required_fields.append("memory date")

        if missing_required_fields:
            st.warning(
                "These mandatory fields contain missing information: "
                + ", ".join(missing_required_fields)
                + ". Please complete them before processing the memory."
            )
        else:
            media_metadata = None

            if uploaded_file is not None:
                media_metadata = save_uploaded_media(uploaded_file)

            note_for_agent = note.strip()
          
            if memory_date is not None:
                user_date_value = memory_date.isoformat()
                user_date_source = "user_provided"
            elif memory_period.strip():
                user_date_value = memory_period.strip()
                user_date_source = "user_provided_approximate"
            elif suggested_photo_date:
                user_date_value = suggested_photo_date
                user_date_source = "media_metadata"
            else:
                user_date_value = None
                user_date_source = "unknown"

            result = process_memory(
                note_for_agent,
                media_metadata=media_metadata,
                user_date=user_date_value,
                user_location=memory_location.strip() if memory_location.strip() else None,
                user_date_source=user_date_source
            )

            st.success("Memory processed by the agent workflow.")

            st.subheader("Routing Decision")
            st.write("Route:", result["route"])

            if result["route"] == "timeline":
                st.info(
                    "Decision: This memory was considered safe and high-confidence, so it was saved directly to the approved timeline."
                )
            else:
                st.warning(
                    "Decision: This memory was uncertain or sensitive, so it was paused and sent to human review."
                )

            st.subheader("Memory Agent Output")
            st.caption("The Memory Agent converts the user note and optional media attachment into a structured memory record.")
            st.json(result["memory"])

            st.subheader("Evaluation Agent Output")
            st.caption("The Evaluation Agent checks trust score, sensitivity, and risk flags.")
            st.json(result["evaluation"])

with tab_timeline:
    st.header("Approved Timeline")

    st.markdown(
        """
        The timeline contains **approved memories only**.

        Memories can enter the timeline in two ways:

        - Automatically, if the Evaluation Agent marks them as low-sensitivity and high-confidence.
        - Manually, after human review and approval.

        This means downstream agents, such as the Story Agent and Safety Agent, only use memories that passed the approval process.
        """
    )

    timeline = load_timeline()

    if not timeline:
        st.info("No approved memories yet.")
    else:
        for memory in timeline:
            st.markdown("---")
            st.subheader(memory.get("title", "Untitled Memory"))

            st.write("Pet:", memory.get("pet_name", "Unknown"))
            st.write("Date or time period:", memory.get("date_or_time_period", "Unknown"))
            st.write("Event type:", memory.get("event_type", "Unknown"))
            st.write("Description:", memory.get("description", ""))

            media = memory.get("media")
            if media:
                st.write("Attached media:", media.get("filename"))

                if media.get("file_type", "").startswith("image"):
                    st.image(media.get("file_path"), use_container_width=True)
                elif media.get("file_type", "").startswith("video"):
                    st.video(media.get("file_path"))

            st.write("Emotion:", memory.get("emotion", "Unknown"))
            st.write("Care relevance:", memory.get("care_relevance", ""))
            st.write("Confidence:", memory.get("confidence", "Unknown"))
            st.write("Status:", memory.get("status", ""))

            if memory.get("reviewer_notes"):
                st.write("Reviewer notes:", memory.get("reviewer_notes"))


with tab_review:
    st.header("Human Review Queue")

    st.markdown(
        """
        This tab demonstrates the **human-in-the-loop** checkpoint.

        If the Evaluation Agent detects sensitive or uncertain information, the memory is not saved automatically.

        A human reviewer can:
        - inspect the original agent-generated memory
        - review the Evaluation Agent's risk flags and reasoning
        - edit the title, description, and care relevance
        - remove sensitive details before approval
        - approve the edited version or reject the memory
        """
    )

    review_queue = load_review_queue()

    if not review_queue:
        st.info("No memories waiting for review.")
    else:
        for item in review_queue:
            st.markdown("---")
            st.subheader(item.get("review_id", "Review Item"))

            st.write("Original Memory:")
            st.json(item.get("memory", {}))

            st.write("Evaluation:")
            st.json(item.get("evaluation", {}))

            st.markdown("### Human Review Action")

            current_memory = item.get("memory", {})

            media = current_memory.get("media")
            if media:
                st.write("Attached media:", media.get("filename"))

                if media.get("file_type", "").startswith("image"):
                    st.image(media.get("file_path"), use_container_width=True)
                elif media.get("file_type", "").startswith("video"):
                    st.video(media.get("file_path"))

            edited_title = st.text_input(
                "Edit title",
                value=current_memory.get("title", ""),
                key=f"title_{item['review_id']}"
            )

            edited_description = st.text_area(
                "Edit description",
                value=current_memory.get("description", ""),
                key=f"description_{item['review_id']}"
            )

            edited_care_relevance = st.text_area(
                "Edit care relevance",
                value=current_memory.get("care_relevance", ""),
                key=f"care_{item['review_id']}"
            )

            reviewer_notes = st.text_area(
                "Reviewer notes",
                value="",
                placeholder="Example: Removed sensitive home routine before approval.",
                key=f"notes_{item['review_id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Approve Edited Memory {item['review_id']}"):
                    edited_memory = current_memory.copy()
                    edited_memory["title"] = edited_title
                    edited_memory["description"] = edited_description
                    edited_memory["care_relevance"] = edited_care_relevance

                    approve_review_item(
                        item["review_id"],
                        edited_memory=edited_memory,
                        reviewer_notes=reviewer_notes
                    )

                    st.success("Edited memory approved and moved to timeline.")
                    st.rerun()

            with col2:
                if st.button(f"Reject {item['review_id']}"):
                    reject_review_item(item["review_id"])
                    st.warning("Memory rejected and removed from review queue.")
                    st.rerun()


with tab_story:
    st.header("RuRu's Life Story")

    st.markdown(
        """
        The **Story Agent** generates RuRu's life story using approved timeline memories only.

        Memories still waiting for human review are not used. This shows how the human-in-the-loop checkpoint controls what downstream agents can access.
        """
    )

    timeline = load_timeline()

    if not timeline:
        st.info("No approved memories yet. Add or approve memories first.")
    else:
        if st.button("Generate Life Story"):
            log_trace(
                step="story_agent",
                status="success",
                details={"approved_memory_count": len(timeline)}
            )
            story = story_agent(timeline)
            st.write(story)


with tab_share:
    st.header("Sitter-Safe Share Card")

    st.markdown(
        """
        The **Safety Agent** creates a limited sitter-safe care summary.

        It uses approved memories only and avoids sharing sensitive owner information such as addresses, exact routines, contact details, or home access information.

        This demonstrates safety-aware information sharing: the app can help a sitter understand RuRu's care needs without exposing private owner details.
        """
    )

    timeline = load_timeline()

    if not timeline:
        st.info("No approved memories yet. Add or approve memories first.")
    else:
        if st.button("Generate Sitter-Safe Card"):
            log_trace(
                step="safety_agent",
                status="success",
                details={"approved_memory_count": len(timeline)}
            )
            share_card = safety_agent(timeline)
            st.json(share_card)

        st.caption(
            "This card is generated from approved memories only. Sensitive owner information is not shared."
        )

with tab_trace:
    st.header("Observability: Local Agent Trace Log")

    st.markdown(
        """
        This tab demonstrates a local observability layer for the agent workflow.

        Each trace event records:

        - which agent step ran
        - whether it succeeded
        - what routing decision was made
        - relevant metadata such as trust score, sensitivity, risk flags, and memory count

        This helps show how the multi-agent workflow can be inspected, debugged, and explained.

        In a full deployment, this local trace log could be connected to Cloud Trace or another production observability tool.
        """
    )

    traces = load_traces()

    if not traces:
        st.info("No trace events yet. Process a memory to generate traces.")
    else:
        st.json(traces)

    if st.button("Clear Trace Log"):
        clear_traces()
        st.success("Trace log cleared.")
        st.rerun()

with tab_demo:
    st.header("Demo Controls")

    st.markdown(
        """
        Use these controls to prepare a clean and reliable demo.

        - **Reset Demo Data** clears the timeline and review queue.
        - **Load Demo Data** loads approved RuRu memories and one sensitive memory for human review.
        - **Clear Trace Log** clears the observability log.
        """
    )

    if st.button("Reset Demo Data"):
        reset_demo_data()
        clear_traces()
        st.success("Timeline, review queue, and trace log have been reset.")
        st.rerun()

    if st.button("Load Demo Data"):
        load_demo_data()
        clear_traces()
        st.success("Demo data loaded. Timeline has approved memories and Human Review has one sensitive item.")
        st.rerun()