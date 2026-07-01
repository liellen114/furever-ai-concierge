from agents import memory_agent, evaluation_agent
from storage import save_memory_to_timeline, save_memory_to_review_queue
from trace_logger import log_trace


def process_memory(note):
    """
    Runs the basic agent workflow:
    User note -> Memory Agent -> Evaluation Agent -> Routing decision -> Storage.
    """

    log_trace(
        step="workflow_start",
        status="started",
        details={"input_type": "text_note"}
    )

    memory = memory_agent(note)

    log_trace(
        step="memory_agent",
        status="success",
        details={
            "pet_name": memory.get("pet_name"),
            "title": memory.get("title"),
            "confidence": memory.get("confidence")
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