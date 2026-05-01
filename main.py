from flask import Flask, render_template, request, jsonify
from ai_thinking import analyze_intent
from ai_deepthink import deep_process

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Chạy logic AI của bạn
    topics = analyze_intent(user_input)
    result, error = deep_process(topics)

    if error:
        return jsonify({"error": error})

    # Trả về toàn bộ dữ liệu để Frontend xử lý việc hiển thị thêm (Read more)
    return jsonify({
        "paragraphs": result["data"],
        "url": result["url"]
    })


if __name__ == "__main__":
    app.run(debug=True)
