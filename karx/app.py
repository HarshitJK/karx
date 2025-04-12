from flask import Flask, render_template, request, jsonify
from main import SecureKarxController
import os
import logging

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
        result = karx.generate_code(prompt)
        
        if not result:
            return jsonify({'error': 'Failed to generate code'}), 500

        return jsonify({'code': result})
    except Exception as e:
        logger.error(f"Error generating code: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 