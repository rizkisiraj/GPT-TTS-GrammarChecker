from openai import OpenAI
client = OpenAI(api_key="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")

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "[Hi, how are you, it's nice to be here, yes i finna go to there] From these list, determine what can i improve on my english speaking skill. DON'T TELL ME ABOUT THE CAPITALS AND PUNCTUATION, I DON'T NEED IT. MAKE IT SIMPLE"
    }
  ],
  temperature=0.8,
  max_tokens=128,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)
print(response.choices[0].message.content)