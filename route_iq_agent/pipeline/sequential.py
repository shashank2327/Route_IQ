from google.adk.agents import SequentialAgent

from ..agents.prioritizer import create_prioritizer_agent
from ..agents.route_builder import create_route_builder_agent


def create_routeiq_pipeline() -> SequentialAgent:
    """
    Assembles the RouteIQ SequentialAgent pipeline.

    Execution order:
      1. visit_prioritizer  — scores & selects clients, adds talking points
      2. route_builder      — geocodes, optimizes, and schedules the route

    The output of visit_prioritizer is automatically passed as context
    to route_builder by the ADK SequentialAgent runtime.

    The route builder agent then prepare a optomised route to that client.
    """
    return SequentialAgent(
        name="routeiq_pipeline",
        description=(
            "End-to-end field sales route optimizer: "
            "prioritizes client visits then builds a traffic-aware daily schedule."
        ),
        sub_agents=[
            create_prioritizer_agent(),
            create_route_builder_agent(),
        ],
    )