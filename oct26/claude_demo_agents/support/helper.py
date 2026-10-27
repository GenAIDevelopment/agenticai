from claude_agent_sdk import (
    ClaudeAgentOptions, 
    Message, 
    AssistantMessage, 
    UserMessage, 
    SystemMessage,
    ResultMessage
)
from claude_agent_sdk.types import TextBlock

MODEL_NAME = 'claude-haiku-4-5'


def base_options(**arguments) -> ClaudeAgentOptions:
    settings = {
        'model': MODEL_NAME,
        'max_turns': 3
    }
    settings.update(arguments)
    options = ClaudeAgentOptions(**settings)
    return options


def parse_message(message: Message):
    if isinstance(message, SystemMessage):
        print(f"subtype: {message.subtype}")

    elif isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block,TextBlock):
                print(block.text)

    elif isinstance(message, ResultMessage):
        print(f"duration: {message.duration_ms} ms")
        print(f"cost in usd: {message.total_cost_usd} ms")
        print(f"session id: {message.session_id}")

