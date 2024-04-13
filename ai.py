from anthropic import Anthropic
from config import CONFIG
from anthropic.lib.streaming._messages import MessageStreamManager

client = Anthropic(
    api_key=CONFIG.claude_connection.get_secret_value(),
)

def get_ai():
    yield client
