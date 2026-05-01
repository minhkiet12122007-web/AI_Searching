import google.generativeai as genai
import os

# Lấy API Key từ Environment Variable trên Render (để bảo mật)
# Hoặc dán trực tiếp: genai.configure(api_key="AIzaSy...")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def deep_process(user_query):
    print(f"[Gemini] Processing query: '{user_query}'...")
    try:
        # Sử dụng model Gemini 1.5 Flash (nhanh và miễn phí)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Yêu cầu AI trả lời kèm nguồn thông tin
        prompt = f"Hãy trả lời câu hỏi sau một cách chi tiết bằng tiếng Việt: {user_query}. " \
            f"Nếu có thông tin từ internet, hãy tổng hợp lại."

        response = model.generate_content(prompt)

        if not response.text:
            return None, "AI không thể tạo câu trả lời vào lúc này."

        # Trả về định dạng giống cũ để bạn không phải sửa frontend
        return {
            "data": [response.text],
            "url": "Nguồn: Google Gemini AI"
        }, None

    except Exception as e:
        return None, f"Lỗi kết nối AI: {str(e)}"
