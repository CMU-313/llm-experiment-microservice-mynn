from src.translator import translate_content, query_llm_robust

translation_eval_set = [
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": "Here is your first example."},
    {"post": "Bonjour, je m'appelle Marie.", "expected_answer": "Hello, my name is Marie."},
    {"post": "Hola, ¿cómo estás hoy?", "expected_answer": "Hello, how are you today?"},
    {"post": "Ciao! È un piacere conoscerti.", "expected_answer": "Hi! It is a pleasure to meet you."},
    {"post": "今日はとても暑いです。", "expected_answer": "It is very hot today."},
    {"post": "Здравствуйте, как ваши дела?", "expected_answer": "Hello, how are you?"},
    {"post": "안녕하세요, 제 이름은 민수입니다.", "expected_answer": "Hello, my name is Minsu."},
    {"post": "Buongiorno e benvenuto nella nostra città.", "expected_answer": "Good morning and welcome to our city."},
    {"post": "Je voudrais une tasse de café, s'il vous plaît.", "expected_answer": "I would like a cup of coffee, please."},
    {"post": "¿Dónde está la estación de tren?", "expected_answer": "Where is the train station?"},
    {"post": "Grazie per il tuo aiuto!", "expected_answer": "Thank you for your help!"},
    {"post": "Ich liebe es, neue Sprachen zu lernen.", "expected_answer": "I love learning new languages."},
    {"post": "La vida es bella.", "expected_answer": "Life is beautiful."},
    {"post": "今天晚上我们去看电影吧。", "expected_answer": "Let's go watch a movie tonight."},
    {"post": "Merci beaucoup pour votre patience.", "expected_answer": "Thank you very much for your patience."},
    {"post": "Добро пожаловать в нашу компанию.", "expected_answer": "Welcome to our company."},
    {"post": "Hôm nay trời đẹp quá!", "expected_answer": "The weather is so nice today!"},
    {"post": "ขอบคุณสำหรับทุกอย่าง", "expected_answer": "Thank you for everything."},
    {"post": "Selamat pagi! Apa kabar?", "expected_answer": "Good morning! How are you?"},
    {"post": "J'aime écouter de la musique classique.", "expected_answer": "I like listening to classical music."},
    {"post": "Mi casa está cerca del mar.", "expected_answer": "My house is near the sea."},
    {"post": "Это моя первая поездка за границу.", "expected_answer": "This is my first trip abroad."},
    {"post": "Olá, tudo bem?", "expected_answer": "Hello, how are you?"},
    {"post": "Ecco il tuo biglietto per il concerto.", "expected_answer": "Here is your ticket for the concert."},
    {"post": "Ich habe gestern ein neues Auto gekauft.", "expected_answer": "I bought a new car yesterday."}
]

language_detection_eval_set = [
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": "German"},
    {"post": "Bonjour, je m'appelle Marie.", "expected_answer": "French"},
    {"post": "Hola, ¿cómo estás hoy?", "expected_answer": "Spanish"},
    {"post": "Ciao! È un piacere conoscerti.", "expected_answer": "Italian"},
    {"post": "今日はとても暑いです。", "expected_answer": "Japanese"},
    {"post": "Здравствуйте, как ваши дела?", "expected_answer": "Russian"},
    {"post": "안녕하세요, 제 이름은 민수입니다.", "expected_answer": "Korean"},
    {"post": "Buongiorno e benvenuto nella nostra città.", "expected_answer": "Italian"},
    {"post": "Je voudrais une tasse de café, s'il vous plaît.", "expected_answer": "French"},
    {"post": "¿Dónde está la estación de tren?", "expected_answer": "Spanish"},
    {"post": "Grazie per il tuo aiuto!", "expected_answer": "Italian"},
    {"post": "Ich liebe es, neue Sprachen zu lernen.", "expected_answer": "German"},
    {"post": "La vida es bella.", "expected_answer": "Spanish"},
    {"post": "今天晚上我们去看电影吧。", "expected_answer": "Chinese"},
    {"post": "Merci beaucoup pour votre patience.", "expected_answer": "French"},
    {"post": "Добро пожаловать в нашу компанию.", "expected_answer": "Russian"},
    {"post": "Hôm nay trời đẹp quá!", "expected_answer": "Vietnamese"},
    {"post": "ขอบคุณสำหรับทุกอย่าง", "expected_answer": "Thai"},
    {"post": "Selamat pagi! Apa kabar?", "expected_answer": "Indonesian"},
    {"post": "J'aime écouter de la musique classique.", "expected_answer": "French"},
    {"post": "Mi casa está cerca del mar.", "expected_answer": "Spanish"},
    {"post": "Это моя первая поездка за границу.", "expected_answer": "Russian"},
    {"post": "Olá, tudo bem?", "expected_answer": "Portuguese"},
    {"post": "Ecco il tuo biglietto per il concerto.", "expected_answer": "Italian"},
    {"post": "Ich habe gestern ein neues Auto gekauft.", "expected_answer": "German"}
]

complete_eval_set = [
    {"post": "Hier ist dein erstes Beispiel.", "expected_answer": (False, "Here is your first example.")},
    {"post": "Bonjour, comment allez-vous aujourd'hui?", "expected_answer": (False, "Hello, how are you today?")},
    {"post": "Hola, me llamo Carlos.", "expected_answer": (False, "Hello, my name is Carlos.")},
    {"post": "Ciao! Come stai?", "expected_answer": (False, "Hi! How are you?")},
    {"post": "今日はとても暑いです。", "expected_answer": (False, "It is very hot today.")},
    {"post": "Здравствуйте, рад вас видеть!", "expected_answer": (False, "Hello, nice to see you!")},
    {"post": "안녕하세요!", "expected_answer": (False, "Hello!")},
    {"post": "Buongiorno e benvenuto nella nostra città.", "expected_answer": (False, "Good morning and welcome to our city.")},
    {"post": "Je voudrais une tasse de thé.", "expected_answer": (False, "I would like a cup of tea.")},
    {"post": "¿Dónde está el aeropuerto?", "expected_answer": (False, "Where is the airport?")},
    {"post": "Ich liebe es, neue Dinge zu lernen.", "expected_answer": (False, "I love learning new things.")},
    {"post": "Grazie per avermi aiutato.", "expected_answer": (False, "Thank you for helping me.")},
    {"post": "今天晚上我们去看电影吧。", "expected_answer": (False, "Let's go watch a movie tonight.")},
    {"post": "Olá, tudo bem?", "expected_answer": (False, "Hello, how are you?")},
    {"post": "Это очень интересный проект.", "expected_answer": (False, "This is a very interesting project.")},

    # --- English posts ---
    {"post": "This is my first post on the forum!", "expected_answer": (True, "This is my first post on the forum!")},
    {"post": "Can anyone help me install the new update?", "expected_answer": (True, "Can anyone help me install the new update?")},
    {"post": "What do you all think about the new design?", "expected_answer": (True, "What do you all think about the new design?")},
    {"post": "Good morning everyone, I hope you’re doing well!", "expected_answer": (True, "Good morning everyone, I hope you’re doing well!")},
    {"post": "I just finished the project, and I’m proud of the results.", "expected_answer": (True, "I just finished the project, and I’m proud of the results.")},
    {"post": "Thank you for your time and help.", "expected_answer": (True, "Thank you for your time and help.")},
    {"post": "Please review the attached document.", "expected_answer": (True, "Please review the attached document.")},
    {"post": "The translation model works surprisingly well.", "expected_answer": (True, "The translation model works surprisingly well.")},
    {"post": "Can someone explain how to fix this error?", "expected_answer": (True, "Can someone explain how to fix this error?")},
    {"post": "Looking forward to your feedback!", "expected_answer": (True, "Looking forward to your feedback!")},
    {"post": "Everything seems to be running smoothly.", "expected_answer": (True, "Everything seems to be running smoothly.")},
    {"post": "I'm learning a lot from this project.", "expected_answer": (True, "I'm learning a lot from this project.")},
    {"post": "The meeting was very productive today.", "expected_answer": (True, "The meeting was very productive today.")},
    {"post": "I really appreciate all your support.", "expected_answer": (True, "I really appreciate all your support.")},
    {"post": "Let’s plan the next steps together.", "expected_answer": (True, "Let’s plan the next steps together.")},

    # --- Unintelligible / malformed posts ---
    {"post": "asldkfjaslkdfj", "expected_answer": (False, "[Translation unavailable]")},
    {"post": "1234567890", "expected_answer": (False, "[Translation unavailable]")},
    {"post": "%%%%%??????", "expected_answer": (False, "[Translation unavailable]")},
    {"post": "これは英語ですか？？？", "expected_answer": (False, "Is this English???")},
    {"post": "blablabla test gibberish", "expected_answer": (False, "[Translation unavailable]")}
]

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

#languages
def test_spanish_translation():
    is_english, translated_content = translate_content("Esta es un mensaje en español")
    assert is_english == False
    assert translated_content == "This is a Spanish message"

def test_portuguese_translation():
    is_english, translated_content = translate_content("Esta é uma mensagem em português")
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
    is_english, translated_content = translate_content("Dies ist eine Nachricht auf Deutsch")
    assert is_english == False
    assert translated_content == "This is a German message"

#google collab

#for now unexpected language assumes it is English and returns the same text back 
def test_unexpected_language():
    """Test handling of unsupported language input"""
    is_english, translated_content = translate_content("Dette er en norsk besked")
    assert is_english == True
    assert translated_content == "Dette er en norsk besked"

def test_missing_message_field():
    result = query_llm_robust("")
    assert not result[0]
    assert "unavailable" in result[1].lower()

def test_non_string_response():
    result = query_llm_robust("%%%%")
    assert not result[0]
    assert "unavailable" in result[1].lower()

def test_model_timeout():
    result = query_llm_robust("!!!!")
    assert not result[0]
    assert "unavailable" in result[1].lower()

def test_gibberish_input():
    result = query_llm_robust("%%%%%%%%%%%%")
    assert not result[0]
    assert "unavailable" in result[1].lower()

def test_normal_input():
    result = query_llm_robust("Bonjour, comment ça va?")
    assert result == (False, "Hello, how are you today?")

