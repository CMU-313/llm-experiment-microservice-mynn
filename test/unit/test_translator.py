from src.translator import query_llm_robust
from sentence_transformers import SentenceTransformer, util
st_model = SentenceTransformer('all-MiniLM-L6-v2')

complete_eval_set = [
    # --- Unintelligible / malformed posts ---
    {"post": "asldkfjaslkdfj", "expected_answer": (False, "asldkfjaslkdfj")},
    {"post": "1234567890", "expected_answer": (False, "1234567890")},

    # --- Non-English posts ---
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": (False, "Here is your first example.")},
    {"post": "Bonjour, comment allez-vous aujourd'hui?", "expected_answer": (False, "Hello, how are you today?")},
    {"post": "Hola, me llamo Carlos.", "expected_answer": (False, "Hello, my name is Carlos.")},
    {"post": "Ciao! Come stai?", "expected_answer": (False, "Hi! How are you?")},

    # --- English posts ---
    {"post": "This is my first post on the forum!", "expected_answer": (True, "This is my first post on the forum!")},
    {"post": "Can anyone help me install the new update?", "expected_answer": (True, "Can anyone help me install the new update?")}
]

def eval_single_response_complete(expected_answer: tuple[bool, str], llm_response: tuple[bool, str]) -> float:
  '''Compares an LLM response to the expected answer from the evaluation dataset using one of the text comparison metrics.'''
  # unpack both expected and response
  expected_is_english, expected_text = expected_answer
  response_is_english, response_text = llm_response

  # 1. correctness for language detection (binary 1 or 0)
  lang_score = 1.0 if expected_is_english == response_is_english else 0.0

  # 2. translation similarity (semantic comparison)
  embeddings = st_model.encode([expected_text, response_text], convert_to_tensor=True)
  trans_score = util.cos_sim(embeddings[0], embeddings[1]).item()
  trans_score = max(0.0, min(1.0, trans_score))  # clamp to [0,1]

  # 3. combine both with weights (half for each)
  total_score = (lang_score * 0.5) + (trans_score * 0.5)
  return total_score

def test_comprehensive():
    for sample in complete_eval_set:
        post = sample["post"]
        expected = sample["expected_answer"]
        response = query_llm_robust(post)
        score = float(eval_single_response_complete(expected, response))
        assert(score >= 0.8)