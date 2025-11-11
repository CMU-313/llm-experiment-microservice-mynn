from src.translator import query_llm_robust
from sentence_transformers import SentenceTransformer, util
st_model = SentenceTransformer('all-MiniLM-L6-v2')

def eval_single_response_complete(expected_answer: tuple[bool, str], llm_response: tuple[bool, str]) -> float:
  '''Compares an LLM response to the expected answer from the evaluation dataset using one of the text comparison metrics.'''
  # unpack both expected and response
  expected_is_english, expected_text = expected_answer
  response_is_english, response_text = llm_response

  # 1. correctness for language detection (binary 1 or 0)
  lang_score = 1.0 if expected_is_english == response_is_english else 0.0

  # 2. translation similarity (semantic comparison)
  embeddings = model.encode([expected_text, response_text], convert_to_tensor=True)
  trans_score = util.cos_sim(embeddings[0], embeddings[1]).item()
  trans_score = max(0.0, min(1.0, trans_score))  # clamp to [0,1]

  # 3. combine both with weights (half for each)
  total_score = (lang_score * 0.5) + (trans_score * 0.5)
  return total_score

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
