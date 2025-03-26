from flask import Flask, request, jsonify
import os
import asyncio
from flask_cors import CORS
from main import AIUseCaseGenerator
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/proposal', methods=['POST'])
def generate_proposal():
    data = request.get_json()
    company_name = data.get("company_name", "").strip()
    if not company_name:
        return jsonify({"error": "Missing or empty 'company_name' in request body."}), 400

    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        return jsonify({"error": "Missing GOOGLE_API_KEY in environment variables."}), 500

    generator = AIUseCaseGenerator(google_api_key)

    try:
        # Run the async proposal generation synchronously
        proposal = asyncio.run(generator.generate_proposal(company_name))
        return jsonify(proposal)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000 by default
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))