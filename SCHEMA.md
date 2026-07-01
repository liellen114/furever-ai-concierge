# FurEver AI Concierge - Data Schema

This file defines the data structures used by the FurEver AI Concierge multi-agent workflow.

The goal is to keep the app simple, explainable, and beginner-friendly.

---

## 1. Pet Profile Schema

The pet profile stores basic information about one pet.

Fields:

* pet_name
* species
* breed
* age
* sex
* personality_notes
* care_notes

Example:

{
"pet_name": "RuRu",
"species": "Dog",
"breed": "Bernedoodle",
"age": "4 years old",
"sex": "Male",
"personality_notes": "Gentle, playful, affectionate, and sometimes cautious in new environments.",
"care_notes": "Enjoys calm walks, familiar toys, and gentle reassurance."
}

---

## 2. Memory Schema

The Memory Agent turns an unstructured note into this structured format.

Fields:

* memory_id
* title
* pet_name
* date_or_time_period
* event_type
* description
* emotion
* people_or_pets
* location
* care_relevance
* confidence
* source_note
* status

Example:

{
"memory_id": "mem_001",
"title": "First Beach Walk",
"pet_name": "RuRu",
"date_or_time_period": "today",
"event_type": "outdoor memory",
"description": "RuRu was nervous around the waves at first but became playful later.",
"emotion": "happy and playful",
"people_or_pets": ["RuRu"],
"location": "beach",
"care_relevance": "RuRu may enjoy calm outdoor play near water, but may need reassurance at first.",
"confidence": 0.85,
"source_note": "RuRu loved his first beach walk today. He was scared of the waves at first but became playful later.",
"status": "approved"
}

---

## 3. Evaluation Schema

The Evaluation Agent checks confidence, sensitivity, and trust score.

Fields:

* trust_score
* sensitivity
* risk_flags
* missing_information
* decision
* reason

Possible sensitivity values:

* low
* medium
* high

Possible decisions:

* save_to_timeline
* human_review

Example:

{
"trust_score": 0.86,
"sensitivity": "low",
"risk_flags": [],
"missing_information": [],
"decision": "save_to_timeline",
"reason": "The memory is clear and does not contain sensitive owner information."
}

---

## 4. Human Review Item Schema

If a memory is uncertain or sensitive, it goes into the review queue.

Fields:

* review_id
* memory
* evaluation
* review_status
* reviewer_notes

Possible review_status values:

* pending
* approved
* rejected

Example:

{
"review_id": "review_001",
"memory": {
"title": "Daily Home Routine",
"pet_name": "RuRu",
"description": "RuRu stays alone on weekdays and the spare key location was mentioned.",
"confidence": 0.92
},
"evaluation": {
"trust_score": 0.92,
"sensitivity": "high",
"risk_flags": ["exact routine", "home access information"],
"decision": "human_review",
"reason": "The memory contains sensitive home routine and access information."
},
"review_status": "pending",
"reviewer_notes": ""
}

---

## 5. Timeline Schema

The timeline is a list of approved memories only.

Example:

[
{
"memory_id": "mem_001",
"title": "First Beach Walk",
"pet_name": "RuRu",
"date_or_time_period": "today",
"event_type": "outdoor memory",
"description": "RuRu was nervous around the waves at first but became playful later.",
"emotion": "happy and playful",
"care_relevance": "RuRu may enjoy calm outdoor play near water, but may need reassurance at first.",
"confidence": 0.85,
"status": "approved"
}
]

---

## 6. Sitter-Safe Share Card Schema

The Safety Agent creates a limited profile that can be shared with a sitter.

Fields:

* pet_name
* temperament
* likes
* dislikes
* care_tips
* comfort_tips
* do_not_share
* safety_note

Example:

{
"pet_name": "RuRu",
"temperament": "Gentle, playful, affectionate, and sometimes cautious in new environments.",
"likes": ["calm walks", "familiar toys", "gentle encouragement"],
"dislikes": ["loud sounds", "sudden changes"],
"care_tips": ["Use a calm voice.", "Give reassurance near unfamiliar places.", "Allow time for RuRu to adjust to new people or settings."],
"comfort_tips": ["Bring a familiar toy.", "Avoid rushing him into new environments.", "Use predictable routines when possible."],
"do_not_share": ["owner address", "exact daily routine", "private contact details"],
"safety_note": "This card only includes information useful for safe pet care. Sensitive owner information has been removed."
}

---

## 7. Decision Rule

The Evaluation Agent and router use this rule:

If trust_score is 0.75 or higher and sensitivity is low, save the memory to the timeline.

Otherwise, send the memory to the human review queue.

This rule demonstrates human-in-the-loop safety control.
