import os
import openai

openai.api_key = 'OPEN AI API KEY'

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="qual o tamanho do planeta terra",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
ret = response['choices'][0]['text']
print(ret)
