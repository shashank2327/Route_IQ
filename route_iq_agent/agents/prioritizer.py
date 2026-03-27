from pathlib import Path
from google.adk.agents import LlmAgent

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "prioritizer.txt"


def create_prioritizer_agent() -> LlmAgent:
    """
    Agent 1 — Visit Prioritizer

    Responsibilities:
    - Score each client by deal stage urgency, days since last visit, and deal value
    - Select the top N clients that fit within the rep's day
    - Generate deal-stage-specific talking points for each selected client
    - Explain why deprioritized clients were skipped

    Tools: None — pure LLM reasoning over CRM data.
    """
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    return LlmAgent(
        name="visit_prioritizer",
        model="gemini-2.5-flash",
        instruction=system_prompt,
        description=(
            "Analyzes CRM data to select and rank the best clients "
            "to visit today, with talking points for each visit."
        ),
    )