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
        return jsonify({"error": "Vui lòng nhập tin nhắn"}), 400

    # Phân tích ý định (từ file ai_thinking.py của bạn)
    query_topic = analyze_intent(user_input)

    # Xử lý bằng Gemini
    result, error = deep_process(query_topic)

    if error:
        return jsonify({"error": error})

    return jsonify({
        "paragraphs": result["data"],
        "url": result["url"]
    })


if __name__ == "__main__":
    # Render yêu cầu chạy trên host 0.0.0.0 và port từ biến môi trường
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
