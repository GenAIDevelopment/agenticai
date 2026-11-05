import os
from pathlib import Path
from dotenv import load_dotenv
from agents import (
    Agent, ItemHelpers, RunResult, RunResultStreaming,
    AgentUpdatedStreamEvent, RawResponsesStreamEvent,
    RunItemStreamEvent, StreamEvent,
)

load_dotenv()
MODEL_NAME = os.getenv('OPENAI_MODEL', 'gpt-5.6-luna')
MAX_TURNS = 3

def base_agent(**args) -> Agent:
    settings = {
        "name" : "Tutor",
        "instructions": "You are a helpful tutor",
        "model": MODEL_NAME
    }
    settings.update(args)
    return Agent(**settings)

def parse_event(event: StreamEvent) -> None:
    # ~ SystemMessage(init)
    if isinstance(event, AgentUpdatedStreamEvent): 
        print(f"agent started {event.new_agent.name}")

    # ~ Assistant Message
    elif isinstance(event, RunItemStreamEvent):
        if event.item.type == "message_output_item":
            print(ItemHelpers.text_message_output(event.item))
        elif event.item.type == "tool_call_item":
            print(f"[tool call] {getattr(event.item.raw_item, 'name', '')}")

def print_result(result: RunResult | RunResultStreaming) -> None:
    usage = result.context_wrapper.usage
    print(f"requests: {usage.requests}")
    print(f"tokens = {usage.input_tokens} in / {usage.output_tokens} out")
    print(f"last response id: {result.last_response_id}")


def load_project_instructions(filename: str = "AGENTS.md") -> str:
    for folder in [Path.cwd(), *Path.cwd().parents]:
        candidate: Path = folder / filename
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    return ""

