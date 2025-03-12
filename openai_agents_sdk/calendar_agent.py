# Output types
from pydantic import BaseModel
from agents import Agent, Runner
from constants import MODEL_GPT_4o_MINI
import asyncio

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

calendar_agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
    model=MODEL_GPT_4o_MINI,
)

async def main():
    prompt = "Meeting with the director of Finding Nemo at monday 3pm next week"
    result = await Runner.run(calendar_agent, prompt)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

"""
name='Meeting with the director of Finding Nemo' 
date='next Monday at 3:00 PM' 
participants=['director of Finding Nemo']
"""