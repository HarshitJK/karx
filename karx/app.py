from flask import Flask, render_template, request, jsonify
from main import SecureKarxController
import os
import logging
import requests
from config.api_config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/web.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize KARX controller
try:
    karx = SecureKarxController(access_token="your_access_token")  # Replace with your actual token
    logger.info("KARX controller initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize KARX controller: {str(e)}")
    raise

def generate_with_deepseek(prompt):
    """Generate code using DeepSeek API"""
    try:
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": DEEPSEEK_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI coding assistant. Generate code based on the user's prompt."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(
            f"{DEEPSEEK_API_URL}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            logger.error(f"DeepSeek API error: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error calling DeepSeek API: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        logger.info(f"Generating code for prompt: {prompt}")
        
        # Try DeepSeek API first
        result = generate_with_deepseek(prompt)
        
        # If DeepSeek fails, fall back to KARX
        if not result:
            result = karx.generate_code(prompt)
        
        if not result:
            return jsonify({'error': 'Failed to generate code'}), 500

        return jsonify({'code': result})
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 