PROMPT_DISEASE = '''You are an expert doctor. Given the following patient details and symptoms, predict the top 3 most likely diseases. For each disease, provide:
- Confidence percentage (0-100)
- A detailed info link (Wikipedia or trusted source)

Patient details:
Gender: {gender}
Age: {age}
Symptoms: {symptoms}

Respond ONLY in JSON like:
{{"diseases":[{{"name":"Disease 1","confidence":70,"info_url":"https://en.wikipedia.org/wiki/Disease_1"}},{{"name":"Disease 2","confidence":20,"info_url":"https://en.wikipedia.org/wiki/Disease_2"}},{{"name":"Disease 3","confidence":10,"info_url":"https://en.wikipedia.org/wiki/Disease_3"}}]}}

Do not include any text outside the JSON block.
'''