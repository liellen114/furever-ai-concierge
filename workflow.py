from agents import memory_agent, evaluation_agent
from storage import save_memory_to_timeline, save_memory_to_review_queue
from trace_logger import log_trace


def process_memory(note, media_metadata=None, user_date=None, user_location=None, user_date_source="unknown"):
    log_trace(
        step="workflow_start",
        status="started",
        details={
            "input_type": "text_note_with_optional_media",
            "has_media": media_metadata is not None,
            "has_user_date": user_date is not None,
            "has_user_location": user_location is not None
        }
    )

    memory = memory_agent(note)

    if user_date:
        memory["date_or_time_period"] = user_date
        memory["date_confidence"] = user_date_source
    else:
        memory["date_confidence"] = memory.get("date_confidence", "unknown")

    if user_location:
        memory["location"] = user_location

    if media_metadata is not None:
        memory["media"] = media_metadata
        memory["source_type"] = "text_and_media"
    else:
        memory["media"] = None
        memory["source_type"] = "text_only"

    log_trace(
        step="memory_agent",
        status="success",
        details={
            "pet_name": memory.get("pet_name"),
            "title": memory.get("title"),
            "confidence": memory.get("confidence"),
            "date_or_time_period": memory.get("date_or_time_period"),
            "location": memory.get("location"),
            "has_media": media_metadata is not None
        }
    )

    evaluation = evaluation_agent(memory)

    log_trace(
        step="evaluation_agent",
        status="success",
        details={
            "trust_score": evaluation.get("trust_score"),
            "sensitivity": evaluation.get("sensitivity"),
            "decision": evaluation.get("decision"),
            "risk_flags": evaluation.get("risk_flags")
        }
    )

    if evaluation["decision"] == "save_to_timeline":
        memory["status"] = "approved"
        route = "timeline"
        save_memory_to_timeline(memory)

        log_trace(
            step="decision_router",
            status="routed_to_timeline",
            details={"reason": evaluation.get("reason")}
        )
    else:
        memory["status"] = "needs_review"
        route = "review_queue"
        save_memory_to_review_queue(memory, evaluation)

        log_trace(
            step="decision_router",
            status="routed_to_human_review",
            details={"reason": evaluation.get("reason")}
        )

    log_trace(
        step="workflow_complete",
        status="success",
        details={"route": route}
    )

    return {
        "memory": memory,
        "evaluation": evaluation,
        "route": route
    }