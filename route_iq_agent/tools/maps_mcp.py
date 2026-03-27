import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
import dotenv
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams 


MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp"

def create_maps_toolset() -> MCPToolset:
    """
    Creates and returns a Google Maps MCP toolset.

    The toolset exposes the following tools to the agent:
      - maps_geocode            : address → lat/lng coordinates
      - maps_reverse_geocode    : lat/lng → human-readable address
      - maps_distance_matrix    : travel times between multiple origins/destinations
      - maps_directions         : turn-by-turn directions for a route
      - maps_places             : search for businesses/points of interest
      - maps_place_details      : detailed info about a specific place

    Requires:
      GOOGLE_MAPS_API_KEY environment variable to be set.
    """
    # api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    # if not api_key:
    #     raise EnvironmentError(
    #         "GOOGLE_MAPS_API_KEY is not set. "
    #         "Copy .env.example to .env and fill in your key."
    #     )

    # return MCPToolset(
    #     connection_params=StdioServerParameters(
    #         command="npx",
    #         args=["-y", "@modelcontextprotocol/server-google-maps"],
    #         env={"GOOGLE_MAPS_API_KEY": api_key},
    #     )
    # )
