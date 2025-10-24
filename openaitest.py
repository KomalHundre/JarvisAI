import os
import Openai
from config import apikey

# Set OpenAI API key
Openai.api_key = apikey

# Ask OpenAI to generate an email
response = Openai.Completion.create(
    model="text-davinci-003",
    prompt="Write an email to my boss for resignation?",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

# Print the generated text
print(response['choices'][0]['text'].strip())
