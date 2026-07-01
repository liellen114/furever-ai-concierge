def memory_agent(note):
    """
    Fake Memory Agent.
    Converts a user note into a structured pet memory.
    Later, this function can be replaced with a Gemini call.
    """
    return {
        "memory_id": "mem_001",
        "title": "Pet Memory",
        "pet_name": "RuRu",
        "date_or_time_period": "unknown",
        "event_type": "general memory",
        "description": note,
        "emotion": "unknown",
        "people_or_pets": ["RuRu"],
        "location": "unknown",
        "care_relevance": "This memory may help understand RuRu's personality and care preferences.",
        "confidence": 0.80,
        "source_note": note,
        "status": "pending"
    }


def evaluation_agent(memory):
    """
    Fake Evaluation Agent.
    Checks whether the memory contains sensitive information.
    """
    note = memory.get("source_note", "").lower()

    sensitive_keywords = [
        "address",
        "phone",
        "spare key",
        "key under",
        "password",
        "alone every day",
        "home every day",
        "8:10am",
        "6:30pm"
    ]

    risk_flags = []
    for keyword in sensitive_keywords:
        if keyword in note:
            risk_flags.append(keyword)

    if risk_flags:
        return {
            "trust_score": 0.90,
            "sensitivity": "high",
            "risk_flags": risk_flags,
            "missing_information": [],
            "decision": "human_review",
            "reason": "The memory may contain sensitive home routine, access, or private owner information."
        }

    return {
        "trust_score": 0.85,
        "sensitivity": "low",
        "risk_flags": [],
        "missing_information": [],
        "decision": "save_to_timeline",
        "reason": "The memory appears clear and does not contain sensitive owner information."
    }


def story_agent(timeline):
    """
    Fake Story Agent.
    Generates a simple life story from approved timeline memories.
    """
    if not timeline:
        return "No approved memories are available yet."

    story_parts = []
    for memory in timeline:
        title = memory.get("title", "Untitled Memory")
        description = memory.get("description", "")
        story_parts.append(f"{title}: {description}")

    return "RuRu's life story is built from approved memories only. " + " ".join(story_parts)


def safety_agent(timeline):
    """
    Fake Safety Agent.
    Creates a sitter-safe care card from approved memories only.
    """
    if not timeline:
        return {
            "pet_name": "RuRu",
            "summary": "No approved care information is available yet.",
            "safety_note": "Sensitive owner information is not shared."
        }

    care_tips = []
    for memory in timeline:
        care_relevance = memory.get("care_relevance", "")
        if care_relevance:
            care_tips.append(care_relevance)

    return {
        "pet_name": "RuRu",
        "temperament": "Gentle, playful, affectionate, and sometimes cautious in new environments.",
        "care_tips": care_tips,
        "do_not_share": [
            "owner address",
            "phone number",
            "exact daily routine",
            "home access information"
        ],
        "safety_note": "This sitter-safe card only uses approved memories and removes sensitive owner information."
    }