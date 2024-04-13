from anthropic import Anthropic
from config import CONFIG

client = Anthropic(
    api_key=CONFIG.claude_connection.get_secret_value(),
)

def get_ai():
    yield client


def get_stream_with_log(client: Anthropic, message_log: list[dict[str, str]]):
    # claude-3-sonnet-20240229
    stream = client.messages.stream(
        max_tokens=1024,
        messages=message_log,
        model="claude-3-sonnet-20240229"
    )
    return stream
