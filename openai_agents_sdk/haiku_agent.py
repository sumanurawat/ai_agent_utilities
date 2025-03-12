from agents import Agent, ModelSettings, function_tool, Runner
from constants import MODEL_GPT_4o_MINI
import asyncio

def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

haiku_agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model=MODEL_GPT_4o_MINI,
    tools=[function_tool(get_weather)],
)

async def main():
    city = "Berlin"
    result = await Runner.run(haiku_agent, city)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

"""
Berlin's sun shines bright,  
Golden rays dance on the streets,  
Joy fills the warm air.
"""