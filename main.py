from flask import Flask, render_template, request, jsonify
from ai_thinking import analyze_intent
from ai_deepthink import deep_process
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message"}), 400

    topics = analyze_intent(user_input)
    result, error = deep_process(topics)

    if error:
        return jsonify({"error": error})

    return jsonify({
        "paragraphs": result["data"],
        "url": result["url"]
    })


if __name__ == "__main__":
    # Sử dụng port từ môi trường hoặc mặc định 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
