import os
from openai import AzureOpenAI

deployment_name = "gpt-4o-mini"  # デプロイ名
model_name = "gpt-4o-mini"  # モデル名

client = AzureOpenAI(
  api_key =api_key,  
  api_version = "2023-05-15",
  azure_endpoint =api_base
)

response = client.chat.completions.create(
    model=model_name , # model = "deployment_name".
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)
#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)