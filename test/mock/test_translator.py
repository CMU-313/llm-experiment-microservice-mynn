from mock import patch
from unittest.mock import patch, MagicMock
from src.translator import client, query_llm_robust

@patch.object(client, "chat")
def test_unexpected_language(mock_chat):
    # simulate irrelevant text response
    mock_chat.return_value = MagicMock()
    mock_chat.return_value.message.content = "I don't understand your request"

    result = query_llm_robust("Hier ist dein erstes Beispiel.")
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)
    assert result[1].lower() == "hier ist dein erstes beispiel."


@patch.object(client, "chat")
def test_missing_message_field(mock_chat):
    # simulate response missing .message
    mock_chat.return_value = None

    result = query_llm_robust("Bonjour, je m'appelle Alice.")
    assert isinstance(result, tuple)
    assert result[0] is False
    assert result[1].lower() == "bonjour, je m'appelle alice."


@patch.object(client, "chat")
def test_non_string_response(mock_chat):
    # simulate model returning dict instead of text
    fake_response = MagicMock()
    fake_response.message.content = {"invalid": "dict"}
    mock_chat.return_value = fake_response

    result = query_llm_robust("Ciao!")
    assert isinstance(result, tuple)
    assert not result[0]
    assert result[1].lower() == "ciao!"


@patch.object(client, "chat", side_effect=RuntimeError("Model timeout"))
def test_model_timeout(mock_chat):
    # simulate exception raised by model call
    result = query_llm_robust("Hola, ¿cómo estás?")
    assert isinstance(result, tuple)
    assert result[0] is False
    assert result[1].lower() == "hola, ¿cómo estás?"

def test_normal_input():
    # control case: normal input should still return tuple and string
    result = query_llm_robust("Bonjour, comment ça va?")
    assert isinstance(result, tuple)
    assert isinstance(result[0], bool)
    assert isinstance(result[1], str)