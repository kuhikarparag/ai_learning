from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

# Import prompt templates from separate Python files
from prompt_medicine import PROMPT_MEDICINE
from prompt_disease import PROMPT_DISEASE
from prompt_remedies import PROMPT_REMEDIES

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise RuntimeError('GEMINI_API_KEY environment variable not set.')
genai.configure(api_key=GEMINI_API_KEY)


def gemini_predict(prompt):
    """Generates content using Gemini model with the provided prompt and returns parsed JSON."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        # Extract JSON from response
        if response.text:
            # Use regex to extract JSON block
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            else:
                print("No JSON found in response:", response.text)
                return None
        else:
            print("Empty response from Gemini")
            return None

    except Exception as e:
        print(f'Gemini API error: {e}')
        return None


def safe_format_prompt(prompt_template, **kwargs):
    """Safely format prompt template with provided arguments."""
    try:
        # Ensure all values are strings and handle None values
        safe_kwargs = {}
        for key, value in kwargs.items():
            if value is None:
                safe_kwargs[key] = ''
            else:
                safe_kwargs[key] = str(value).strip()
        # Defensive: remove any accidental double quotes in keys
        for k in list(safe_kwargs.keys()):
            if k.startswith('"') and k.endswith('"'):
                safe_kwargs[k.strip('"')] = safe_kwargs.pop(k)
        return prompt_template.format(**safe_kwargs)
    except KeyError as e:
        print(f"Missing template variable: {e}. Provided: {list(kwargs.keys())}")
        print(f"Prompt template: {prompt_template}")
        return None
    except Exception as e:
        print(f"Prompt formatting error: {e}")
        return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("Starting prediction process...")

        # Get form data with default values
        gender = request.form.get('gender', '').strip()
        age = request.form.get('age', '').strip()
        symptoms = request.form.get('symptoms', '').strip()

        # Validate input
        if not all([gender, age, symptoms]):
            return jsonify({
                'error': 'Missing required fields: gender, age, or symptoms',
                'success': False
            })

        print(f"Input data - Gender: {gender}, Age: {age}, Symptoms: {symptoms}")

        # 1. Medicine prediction
        prompt_medicine = safe_format_prompt(PROMPT_MEDICINE, gender=gender, age=age, symptoms=symptoms)
        if not prompt_medicine:
            return jsonify({'error': 'Failed to format medicine prompt', 'success': False})

        med_result = gemini_predict(prompt_medicine)
        medicines = med_result.get('medicines', []) if med_result else []
        print(f"Medicine prediction completed: {len(medicines)} medicines found")

        # 2. Disease prediction
        prompt_disease = safe_format_prompt(PROMPT_DISEASE, gender=gender, age=age, symptoms=symptoms)
        if not prompt_disease:
            return jsonify({'error': 'Failed to format disease prompt', 'success': False})

        disease_result = gemini_predict(prompt_disease)
        diseases = disease_result.get('diseases', []) if disease_result else []
        print(f"Disease prediction completed: {len(diseases)} diseases found")

        # 3. Remedies prediction (use top disease if available)
        top_disease = diseases[0]['name'] if diseases else 'general symptoms'
        # Prepare medicine names as a comma-separated string for the remedies prompt
        medicine_names = ', '.join([m['name'] for m in medicines if 'name' in m])
        prompt_remedies = safe_format_prompt(
            PROMPT_REMEDIES,
            gender=gender,
            age=age,
            symptoms=symptoms,
            top_disease=top_disease,
            medicines=medicine_names
        )
        if not prompt_remedies:
            return jsonify({'error': 'Failed to format remedies prompt', 'success': False})

        remedies_result = gemini_predict(prompt_remedies)
        # Defensive: ensure remedies_result is a dict
        if not isinstance(remedies_result, dict):
            remedies_result = {}
        # Parse disease_remedies by dietary category if present
        disease_name = remedies_result.get('disease_name', top_disease)
        disease_remedies = remedies_result.get('disease_remedies', {})
        generic_remedies = remedies_result.get('generic_remedies', [])
        dietary_recommendations = remedies_result.get('dietary_recommendations', [])
        lifestyle_modifications = remedies_result.get('lifestyle_modifications', [])
        natural_treatments = remedies_result.get('natural_treatments', [])

        print("Remedies prediction completed")

        return jsonify({
            'medicines': medicines,
            'diseases': diseases,
            'disease_name': disease_name,
            'disease_remedies': disease_remedies,
            'generic_remedies': generic_remedies,
            'dietary_recommendations': dietary_recommendations,
            'lifestyle_modifications': lifestyle_modifications,
            'natural_treatments': natural_treatments,
            'success': True
        })

    except Exception as e:
        print(f'Server error: {e}')
        return jsonify({'error': str(e), 'success': False})


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Medical prediction API is running'})


if __name__ == '__main__':
    app.run(debug=True)