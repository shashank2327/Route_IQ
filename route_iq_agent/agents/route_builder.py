from pathlib import Path
from google.adk.agents import LlmAgent
from ..tools.maps_mcp import create_maps_toolset

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "route_builder.txt"


def create_route_builder_agent() -> LlmAgent:
    """
    Agent 2 — Route Builder

    Responsibilities:
    - Geocode every client address using the Google Maps MCP
    - Fetch live traffic-aware travel times via distance_matrix
    - Compute an optimized stop order (nearest-neighbour)
    - Attach realistic ETAs (30 min per visit + actual drive time)
    - Drop any stops that push past the rep's work hours end time
    - Retrieve full directions for the complete route

    Tools: Google Maps MCP server (geocode, distance_matrix, directions)
    """
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    return LlmAgent(
        name="route_builder",
        model="gemini-2.5-flash",
        instruction=system_prompt,
        description=(
            "Builds a traffic-aware optimized route using Google Maps, "
            "with arrival times and directions for each client stop."
        ),
        tools=[create_maps_toolset()],
    )