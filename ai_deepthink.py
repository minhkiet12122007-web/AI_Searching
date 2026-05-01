import google.generativeai as genai
import os

# Render sẽ đọc mã này từ bảng Environment Variables bạn vừa cài
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def deep_process(user_query):
    print(f"[Gemini] Đang trả lời câu hỏi: '{user_query}'...")
    try:
        # Kiểm tra nếu chưa có mã Key
        if not api_key:
            return None, "Lỗi: Chưa cấu hình GEMINI_API_KEY trên Render."

        model = genai.GenerativeModel('gemini-pro')

        # Yêu cầu Gemini trả lời
        response = model.generate_content(user_query)

        # Trả về kết quả (phải bọc trong [ ] để Frontend của bạn không bị lỗi)
        return {
            "data": [response.text],
            "url": "Nguồn: Trí tuệ nhân tạo Gemini"
        }, None

    except Exception as e:
        print(f"Lỗi: {str(e)}")
        return None, f"AI đang bận, bạn thử lại sau nhé! (Chi tiết: {str(e)})"
