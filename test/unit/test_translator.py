from src.translator import translate_content, query_llm_robust


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"


def test_llm_normal_response():
    is_english, translated_content = translate_content("यह हिंदी में संदेश है")
    assert is_english == False
    assert translated_content == "This is a Hindi message"


def test_llm_gibberish_response():
    is_english, translated_content = translate_content("asldkfjaslkdfj")
    assert is_english == False
    assert translated_content == "[Translation unavailable]"


def test_spanish_translation():
    is_english, translated_content = translate_content(
        "Esta es un mensaje en español")
    assert is_english == False
    assert translated_content == "This is a Spanish message"


def test_portuguese_translation():
    is_english, translated_content = translate_content(
        "Esta é uma mensagem em português")
    assert is_english == False
    assert translated_content == "This is a Portuguese message"


def test_japanese_translation():
    is_english, translated_content = translate_content("これは日本語のメッセージです")
    assert is_english == False
    assert translated_content == "This is a Japanese message"


def test_korean_translation():
    is_english, translated_content = translate_content("이것은 한국어 메시지입니다")
    assert is_english == False
    assert translated_content == "This is a Korean message"


def test_german_translation():
    is_english, translated_content = translate_content(
        "Dies ist eine Nachricht auf Deutsch")
    assert is_english == False
    assert translated_content == "This is a German message"
