import tracker
from unittest.mock import patch, MagicMock
from tracker import send_telegram_message


@patch("tracker.TELEGRAM_TOKEN", "test-token")
@patch("tracker.TELEGRAM_CHAT_ID", "test-chat-id")
@patch("tracker.requests.post")
def test_sends_to_correct_url(mock_post):
    mock_post.return_value = MagicMock(json=lambda: {"ok": True})
    send_telegram_message("hello")
    called_url = mock_post.call_args[0][0]
    assert called_url == "https://api.telegram.org/bottest-token/sendMessage"


@patch("tracker.TELEGRAM_TOKEN", "test-token")
@patch("tracker.TELEGRAM_CHAT_ID", "test-chat-id")
@patch("tracker.requests.post")
def test_payload_contains_chat_id_and_text(mock_post):
    mock_post.return_value = MagicMock(json=lambda: {"ok": True})
    send_telegram_message("price dropped!")
    payload = mock_post.call_args[1]["json"]
    assert payload["chat_id"] == "test-chat-id"
    assert payload["text"] == "price dropped!"


@patch("tracker.TELEGRAM_TOKEN", "test-token")
@patch("tracker.TELEGRAM_CHAT_ID", "test-chat-id")
@patch("tracker.requests.post")
def test_uses_post_method(mock_post):
    mock_post.return_value = MagicMock(json=lambda: {"ok": True})
    send_telegram_message("hello")
    mock_post.assert_called_once()
