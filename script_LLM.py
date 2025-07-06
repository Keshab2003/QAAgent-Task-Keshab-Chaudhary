import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

with open("recruter_transcript.txt") as f:
    transcript = f.read()

# Use the new OpenAI API format
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a QA tester."},
        {"role": "user", "content": f"Generate frontend test cases based on this video transcript:\n{transcript}"}
    ]
)

print(response.choices[0].message.content)
