from src.translator import query_llm_robust

def test_chinese():
    is_english, translated_content = query_llm_robust("这个项目太有趣了")
    assert is_english == False
    assert translated_content == "This project is so much fun!"


def test_llm_normal_response():
    is_english, translated_content = query_llm_robust("यह हिंदी में संदेश है")
    assert is_english == False
    assert translated_content == "This is a Hindi message"


def test_llm_gibberish_response():
    is_english, translated_content = query_llm_robust("asldkfjaslkdfj")
    assert is_english == False
    assert translated_content == "[Translation unavailable]"


def test_spanish_translation():
    is_english, translated_content = query_llm_robust(
        "Esta es un mensaje en español")
    assert is_english == False
    assert translated_content == "This is a Spanish message"


def test_portuguese_translation():
    is_english, translated_content = query_llm_robust(
        "Esta é uma mensagem em português")
    assert is_english == False
    assert translated_content == "This is a Portuguese message"


def test_japanese_translation():
    is_english, translated_content = query_llm_robust("これは日本語のメッセージです")
    assert is_english == False
    assert translated_content == "This is a Japanese message"


def test_korean_translation():
    is_english, translated_content = query_llm_robust("이것은 한국어 메시지입니다")
    assert is_english == False
    assert translated_content == "This is a Korean message"


def test_german_translation():
    is_english, translated_content = query_llm_robust(
        "Dies ist eine Nachricht auf Deutsch")
    assert is_english == False
    assert translated_content == "This is a German message"
