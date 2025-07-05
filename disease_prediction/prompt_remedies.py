PROMPT_REMEDIES = '''You are an expert doctor. Given the following patient details, symptoms, predicted disease, and the list of predicted medicines, suggest:
- An ordered list of home remedies specific to the predicted disease, categorized by dietary preference (veg, non-veg, vegan, etc). Each category should be a list of remedies in order of importance.
- Generic home remedies for the symptoms (as a list)
- Clearly mention the medicine names in the remedies where relevant.

Patient details:
Gender: {gender}
Age: {age}
Symptoms: {symptoms}
Predicted disease: {top_disease}
Predicted medicines: {medicines}

Respond ONLY in JSON like:
{{"disease_name": "{top_disease}",
 "disease_remedies": {{
    "veg": ["Remedy 1 for veg mentioning Paracetamol", "Remedy 2 for veg mentioning Dolo 650"],
    "non_veg": ["Remedy 1 for non-veg mentioning Paracetamol"],
    "vegan": ["Remedy 1 for vegan mentioning Dolo 650"]
  }},
  "generic_remedies": ["Generic remedy 1 mentioning Paracetamol", "Generic remedy 2 mentioning Dolo 650"]
}}

Do not include any text outside the JSON block.
'''