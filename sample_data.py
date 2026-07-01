DEMO_SAFE_MEMORY = {
    "memory_id": "demo_mem_001",
    "title": "First Beach Walk",
    "pet_name": "RuRu",
    "date_or_time_period": "Spring 2026",
    "event_type": "outdoor memory",
    "description": "RuRu was nervous around the waves at first but became playful later.",
    "emotion": "curious and happy",
    "people_or_pets": ["RuRu"],
    "location": "beach",
    "care_relevance": "RuRu may enjoy calm outdoor play near water, but may need gentle reassurance at first.",
    "confidence": 0.88,
    "source_note": "RuRu loved his first beach walk. He was scared of the waves at first but became playful later.",
    "status": "approved"
}


DEMO_SAFE_MEMORY_2 = {
    "memory_id": "demo_mem_002",
    "title": "Favourite Toy",
    "pet_name": "RuRu",
    "date_or_time_period": "2026",
    "event_type": "comfort memory",
    "description": "RuRu relaxed quickly when he had his favourite soft toy nearby.",
    "emotion": "calm and comforted",
    "people_or_pets": ["RuRu"],
    "location": "home",
    "care_relevance": "A familiar soft toy may help RuRu feel more secure in new environments.",
    "confidence": 0.84,
    "source_note": "RuRu relaxed quickly when he had his favourite soft toy nearby.",
    "status": "approved"
}


DEMO_REVIEW_ITEM = {
    "review_id": "demo_review_001",
    "memory": {
        "memory_id": "demo_mem_sensitive_001",
        "title": "Daily Home Routine",
        "pet_name": "RuRu",
        "date_or_time_period": "weekdays",
        "event_type": "care routine",
        "description": "RuRu stays alone every weekday from 8:10am to 6:30pm, and the spare key is under the front mat.",
        "emotion": "unknown",
        "people_or_pets": ["RuRu"],
        "location": "home",
        "care_relevance": "This may help explain RuRu's routine, but it contains private home access information.",
        "confidence": 0.92,
        "source_note": "RuRu stays alone every weekday from 8:10am to 6:30pm, and the spare key is under the front mat.",
        "status": "needs_review"
    },
    "evaluation": {
        "trust_score": 0.92,
        "sensitivity": "high",
        "risk_flags": ["exact routine", "home access information"],
        "missing_information": [],
        "decision": "human_review",
        "reason": "The memory contains sensitive home routine and access information."
    },
    "review_status": "pending",
    "reviewer_notes": ""
}