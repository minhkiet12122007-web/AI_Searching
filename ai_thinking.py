def analyze_intent(user_input):
    # Chuyển về chữ thường, xóa dấu chấm hỏi ở cuối
    clean_input = user_input.lower().replace("?", "").strip()

    print(f"[Thinking] Analyzing question: '{clean_input}'")

    # Trả về nguyên câu đã làm sạch để tìm cụm từ chính xác hơn
    return clean_input
