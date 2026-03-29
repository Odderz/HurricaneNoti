from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import tools

root_agent = Agent(
    name="HurricaneNoti",
    model="gemini-2.5-flash-lite",
    description="A multi-agent hurricane safety system for US residents.",
    instruction="""You are HurricaneNoti, a hurricane safety assistant for anyone in the United States.
    When a user first messages you, greet them and ask:
    1. What is your zip code?
    2. How many miles radius for emergency resources? (default 5 miles)
    Then:
    1. Call get_storm_data
    2. Call get_location_info with their zip code
    3. Call get_safety_recommendation with zip code and storm details
    4. Call get_nearby_resources with zip code and radius_miles
    5. Ask if they want an email alert, if yes call send_alert_email
    6. Summarize everything clearly.""",
    tools=[
        tools.get_storm_data,
        tools.get_location_info,
        tools.get_safety_recommendation,
        tools.get_nearby_resources,
        tools.send_alert_email,
    ],
)