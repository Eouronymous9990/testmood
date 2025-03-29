from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TEXT_ANALYTICS_ENDPOINT = "https://fluffy-soundscapegen.cognitiveservices.azure.com"
TEXT_ANALYTICS_KEY = "6ukghamsjcYiKjWsSQgkgPIT5VVEyRo7y2z4o2iwPKy2sypft2opJQQJ99BBACYeBjFXJ3w3AAAEACOGMRNT"

OPENAI_ENDPOINT = "https://openchatbot23.openai.azure.com/"
OPENAI_KEY = "G8pjrKrYklUPdmHMrZcACUGsSYvCcQ8sGrpVqMWwjNJYMj3gVaRwJQQJ99BBACYeBjFXJ3w3AAABACOGpDDW"
OPENAI_DEPLOYMENT_NAME = "gpt-4"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        user_input = request.json.get('text')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
            
        sentiment = analyze_sentiment(user_input)
        print(f"Sentiment: {sentiment}")
        
        theme = generate_theme(sentiment)
        print(f"Generated Theme: {theme}")
        
        return jsonify({'theme': theme})
        
    except Exception as e:
        print(f"Error in /generate: {str(e)}")
        return jsonify({"error": str(e)}), 500

def analyze_sentiment(text):
    headers = {
        'Ocp-Apim-Subscription-Key': TEXT_ANALYTICS_KEY,
        'Content-Type': 'application/json',
    }
    body = {
        'documents': [{
            'id': '1',
            'language': 'en',
            'text': text
        }]
    }
    response = requests.post(
        f"{TEXT_ANALYTICS_ENDPOINT}/text/analytics/v3.1/sentiment",
        headers=headers,
        json=body
    )
    response.raise_for_status()
    return response.json()['documents'][0]['sentiment']

def generate_theme(sentiment):
    prompt = f"Suggest a single-word soundscape theme for someone feeling {sentiment}. Examples: ocean, forest, rain. Only return the keyword."
    
    headers = {
        'Content-Type': 'application/json',
        'api-key': OPENAI_KEY
    }
    body = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 15,
        "temperature": 0.7
    }
    
    response = requests.post(
        f"{OPENAI_ENDPOINT}/openai/deployments/{OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version=2023-12-01-preview",
        headers=headers,
        json=body
    )
    response.raise_for_status()

    print("OpenAI Response:", response.json())
    
    return response.json()['choices'][0]['message']['content'].strip().lower()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
