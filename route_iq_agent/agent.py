import json
import re
from datetime import date
from typing import Optional

from dotenv import load_dotenv
from google.adk.agents.callback_context import CallbackContext
from google.genai import types as genai_types

from .pipeline.sequential import create_routeiq_pipeline

load_dotenv()


def _sanitize_user_message(callback_context: CallbackContext) -> Optional[genai_types.Content]:
    """
    Before Agent 1 runs, intercept the user message and convert raw JSON input
    into a brace-free natural language string so ADK's template engine cannot
    mistake JSON keys for session state variables.

    If the message is not valid JSON (i.e. the user typed a plain question),
    return None to let ADK handle it normally.
    """
    user_message: str = callback_context.user_content.parts[0].text.strip()

    try:
        data = json.loads(user_message)
        if "rep" not in data or "clients" not in data:
            return None
    except (json.JSONDecodeError, AttributeError):
        return None

    rep = data["rep"]
    clients = data["clients"]
    today = date.today().isoformat()

    lines = [
        f"Sales rep: {rep.get('rep_name', 'Unknown')}",
        f"Start location: {rep.get('start_location', '')}",
        f"Start time: {rep.get('start_time', '09:00')}",
        f"Work hours: {rep.get('work_hours', '09:00-18:00')}",
        f"Max visits today: {rep.get('max_visits', 6)}",
        f"Today's date: {today}",
        "",
        "CRM Client List:",
    ]

    for i, c in enumerate(clients, 1):
        lines.append(
            f"  Client {i}:"
            f" name={c.get('client_name', '')},"
            f" address={c.get('address', '')},"
            f" last_visit={c.get('last_visit_date', '')},"
            f" stage={c.get('deal_stage', '')},"
            f" value_usd={c.get('deal_value_usd', 0)}"
        )

    sanitized_text = "\n".join(lines)

    return genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=sanitized_text)],
    )


pipeline = create_routeiq_pipeline()
pipeline.sub_agents[0].before_agent_callback = _sanitize_user_message

root_agent = pipeline