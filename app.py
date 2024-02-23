# import os
# from flask import Flask, request, jsonify, render_template
# import google.generativeai as genai
# from dotenv import load_dotenv
# from system_messages import persona

# load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# genai.configure(api_key=GEMINI_API_KEY)

# model = genai.GenerativeModel('gemini-pro')

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask_question():
#     # print("fgggg", request.json)
#     query = request.json['query']

#     if not query.strip():
#         return jsonify({"error": "User query cannot be empty"}), 400

#     messages = [{'role': 'user', 'parts': [persona]}]
#     response = model.generate_content(messages)
#     messages.append({'role': 'model', 'parts': [response.text]})
#     messages.append({'role': 'user', 'parts': [query]})
#     response = model.generate_content(messages)
#     return jsonify({'response': str(response.text)})

# if __name__ == "__main__":
    
#     app.run(host="0.0.0.0", port=8000, debug=True)
import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
from system_messages import persona

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        query = request.json['query']
        
        if not query.strip():
            return jsonify({"error": "User query cannot be empty"}), 400
        
        messages = [{'role': 'user', 'parts': [persona]}]
        response = model.generate_content(messages)
        messages.append({'role': 'model', 'parts': [response.text]})
        messages.append({'role': 'user', 'parts': [query]})
        response = model.generate_content(messages)
        return jsonify({'response': str(response.text)})
    
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

# if __name__ == "__main__":
#     # Set debug to False for production
#     app.debug = False
#     # Run the app using a production-ready server like Gunicorn
#     app.run(host="0.0.0.0", port=8000)
    
if __name__ == '__main__':
    app.run(debug=False, load_dotenv=True)
