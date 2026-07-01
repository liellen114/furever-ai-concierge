from workflow import process_memory
from storage import load_timeline, load_review_queue

safe_note = "RuRu loved his first beach walk today. He was scared of the waves at first but became playful later."

sensitive_note = "RuRu stays alone every weekday from 8:10am to 6:30pm, and the spare key is under the front mat."

print("Processing safe note...")
safe_result = process_memory(safe_note)
print("Route:", safe_result["route"])

print("\nProcessing sensitive note...")
sensitive_result = process_memory(sensitive_note)
print("Route:", sensitive_result["route"])

print("\nTimeline:")
print(load_timeline())

print("\nReview Queue:")
print(load_review_queue())
