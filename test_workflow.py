from workflow import process_memory

safe_note = "RuRu loved his first beach walk today. He was scared of the waves at first but became playful later."

sensitive_note = "RuRu stays alone every weekday from 8:10am to 6:30pm, and the spare key is under the front mat."

print("=== SAFE MEMORY TEST ===")
safe_result = process_memory(safe_note)
print(safe_result)

print("\n=== SENSITIVE MEMORY TEST ===")
sensitive_result = process_memory(sensitive_note)
print(sensitive_result)