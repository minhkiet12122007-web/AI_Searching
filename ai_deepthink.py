import google.generativeai as genai
import os

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


def deep_process(user_query):
    print(f"[Gemini] Đang xử lý: '{user_query}'...")
    try:
        if not api_key:
            return None, "Lỗi: Chưa có API Key trên Render."

        # CHIÊU CUỐI: Tự tìm model có hỗ trợ generateContent
        available_models = [m.name for m in genai.list_models(
        ) if 'generateContent' in m.supported_generation_methods]

        if not available_models:
            return None, "Lỗi: Không tìm thấy model nào khả dụng cho Key này."

        # Ưu tiên lấy gemini-1.5-flash nếu có, không thì lấy cái đầu tiên trong danh sách
        target_model = next(
            (m for m in available_models if '1.5-flash' in m), available_models[0])

        print(f"[Gemini] Đang dùng model: {target_model}")

        model = genai.GenerativeModel(target_model)
        response = model.generate_content(user_query)

        return {
            "data": [response.text],
            "url": f"Nguồn: {target_model}"
        }, None

    except Exception as e:
        print(f"Lỗi hệ thống: {str(e)}")
        return None, f"Lỗi: {str(e)}"
