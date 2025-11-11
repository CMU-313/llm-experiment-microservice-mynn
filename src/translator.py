import os
from ollama import chat, ChatResponse, Client

# Get OLLAMA_HOST, if specified, or default to localhost:11434.
OLLAMA_URL = os.getenv("OLLAMA_HOST", "localhost:11434")
MODEL_NAME = "llama3.1:8b"

# Initialize the OpenAI client
client = Client(host=OLLAMA_URL)


def get_translation(post: str) -> str:
    context = """
       You are a language translator.
       Translate the input text and reply only with the English translation of that text.
       If the input text cannot be translated or is gibberish, simply return the
       input text.
   """
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": context.strip()},
                {"role": "user", "content": post}
            ]
        )

        translation = response.message.content
        if not translation:
            return "[Translation unfound]"
        return translation

    except Exception as e:
        return f"[Error: {str(e)}]"


def get_language(post: str) -> str:
    context = """
        You are a language classifier.
        Detect the language of the input text and reply only with the English name of that language.
    """

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": context.strip()},
                {"role": "user", "content": post}
            ]
        )
        detected_lang = response.message.content.strip().capitalize()

        if not detected_lang:
            return "[Language undetected]"
        return detected_lang

    except Exception as e:
        return f"[Error: {str(e)}]"


def query_llm(post: str) -> tuple[bool, str]:
    if not post or not isinstance(post, str) or not post.strip():
        return (False, "[Invalid Input]")

    lang = get_language(post).strip().lower()

    if "english" in lang:
        return (True, post)

    translation = get_translation(post).strip()

    if not translation:
        translation = post
    return (False, translation)


def query_llm_robust(post: str) -> tuple[bool, str]:
    MAX_LEN = 4096
    try:
        print(f"Received Post: {post}")

        # input validation
        if not isinstance(post, str) or not post.strip():
            print(f"Invalid input: {post}")
            return (False, "[Invalid input]")

        if len(post) > MAX_LEN:
            post = post[:MAX_LEN]  # truncate to safe length

        # language detection
        try:
            lang = get_language(post)
            lang = lang.strip().lower() if isinstance(lang, str) else ""
        except Exception as e:
            print(f"Error in language detection: {str(e)}")
            return (False, post)

        print(f"Language: {lang}")

        if "english" in lang:
            return (True, post)

        # translation
        try:
            translation = get_translation(post)
            if not isinstance(translation, str):
                translation = ""
            translation = translation.strip().replace("\x00", "")
        except Exception as e:
            print(f"Error in translation: {str(e)}")
            return (False, post)

        print(f"Translation: {translation}")

        # if translation empty or suspicious, return original
        if not translation or len(translation) > MAX_LEN:
            print(f"Translation is empty or too long: {translation}")
            return (False, post)

        # secondary check: ensure translation is in English
        try:
            translated_lang = get_language(translation)
            translated_lang = translated_lang.strip().lower(
            ) if isinstance(translated_lang, str) else ""
            if "english" not in translated_lang:
                print(f"Translation is not in English: {translated_lang}")
                # model didn’t translate properly — fallback to original
                return (False, post)
        except Exception as e:
            print(f"Error in language check: {str(e)}")
            # if language check fails, still fallback safely
            return (False, post)

        # successful case
        print(f"Translation is in English: {translation}")
        return (False, translation)

    except Exception as e:
        # last-resort fallback
        print(f"Last-resort fallback error: {str(e)}")
        return (False, post)
