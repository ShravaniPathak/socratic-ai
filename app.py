import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from flask import send_file
from dotenv import load_dotenv

load_dotenv()  
print("Dotenv working")

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
print("Api key accessed")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("models/gemma-3-27b-it")
# print(model)

chat = model.start_chat(history=[])

def generate_socratic_response(query):
    instruction = "Answer using the Socratic method."
    message = f"{query}\n\n{instruction}"

    response = chat.send_message(message)

    print(chat.history)

    if not response or not response.text:
        return "<div class='response-item'>Sorry, I couldn't generate a response. Please try again.</div>"

    print (response)
    beautified_response = "<div class='response-item'>"
    beautified_response += f"<h3>Response for: {query}</h3>"
    
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit() and line[1] == '.':
            parts = line.split(' ', 1)
            number_part = parts[0]
            text_part = parts[1] if len(parts) > 1 else ''
            beautified_response += f"<strong>{number_part}</strong> {text_part}<br>"
        else:
            while '**' in line:
                start = line.index('**') + 2
                end = line.index('**', start)
                bold_text = line[start:end]
                line = line[:start-2] + f"<strong>{bold_text}</strong>" + line[end+2:]
            beautified_response += f"{line}<br>"
    
    beautified_response += "<hr></div>"
    
    return beautified_response

@app.route('/')
def home():
    return render_template('about.html')

@app.route('/getStarted')
def get_started():
    return render_template('getStarted.html')

@app.route('/heroImage')
def heroImage():
    return send_file('templates/hero image.png', mimetype='image/png')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['query']
    response = generate_socratic_response(user_input)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

