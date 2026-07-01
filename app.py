import streamlit as st

from workflow import process_memory
from agents import story_agent, safety_agent
from storage import (
    load_timeline,
    load_review_queue,
    approve_review_item,
    reject_review_item,
    reset_demo_data,
    load_demo_data
)
from trace_logger import load_traces, clear_traces, log_trace


st.set_page_config(
    page_title="FurEver AI Concierge",
    page_icon="🐾",
    layout="wide"
)

st.title("🐾 FurEver AI Concierge")

st.subheader(
    "A privacy-aware multi-agent assistant that turns pet memories into timelines, stories, and sitter-safe care summaries."
)

st.markdown(
    """
    **Course concepts demonstrated in this prototype:**

    1. **Multi-agent workflow** — Memory Agent, Evaluation Agent, Story Agent, and Safety Agent work together.
    2. **Agent skills** — memory capture, timeline building, story generation, and trust scoring.
    3. **Human-in-the-loop** — sensitive or uncertain memories are paused for human review.
    4. **Safety-aware sharing** — only approved and sitter-safe information is used downstream.
    5. **Observability** — the app records trace logs showing which agent steps ran.

    **Workflow:**  
    User memory note → Memory Agent → Evaluation Agent → Decision Router → Timeline or Human Review → Story Agent / Safety Agent
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

        - The **Memory Agent** extracts a structured memory from the note.
        - The **Evaluation Agent** checks trust score and sensitivity.
        - The **Decision Router** decides whether the memory is safe to save or needs human review.
        """
    )

    note = st.text_area(
        "Write a memory about RuRu:",
        height=150,
        placeholder="Example: RuRu loved his first beach walk today. He was scared of the waves at first but became playful later."
    )

    if st.button("Process Memory"):
        if not note.strip():
            st.warning("Please enter a memory note first.")
        else:
            result = process_memory(note)

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
            st.caption("The Memory Agent converts the user note into a structured memory record.")
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