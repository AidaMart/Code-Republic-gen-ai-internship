# Some necessary links:
# https://platform.openai.com/docs/quickstart?context=python
# https://github.com/ahmeterenodaci/easygoogletranslate
# https://cloud.google.com/translate/docs/languages
# https://www.deepl.com/en/docs-api

# Description
# Run the python script, it will take input from you, where you can ask your question in Armenian
# for example,  Խնդրում եմ պատմեք ինձ Հարրի Փոթերի մասին:
# the program will translate the request into English, will use gpt3.5 to generate answer in English
# at the end the response will be again translated back to Armenian and you can see the results!

import warnings
warnings.filterwarnings("ignore")
from openai import OpenAI
from easygoogletranslate import EasyGoogleTranslate

client = OpenAI(api_key="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")

armenian_input = input("Please provide the armenian input: ")

translator_arm_to_en = EasyGoogleTranslate(
    source_language='hy',
    target_language='en',
    timeout=10
)
english_input = translator_arm_to_en.translate(armenian_input)
print("Here is english translation: ", english_input)

response = client.chat.completions.create(
  model="gpt-3.5-turbo-1106",
  #response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": english_input}
  ]
)

translator_en_to_arm = EasyGoogleTranslate(
    source_language='en',
    target_language='hy',
    timeout=10
)
armenian_output = translator_en_to_arm.translate(response.choices[0].message.content)
print("Here is the response: ", armenian_output)

#print(response.choices[0].message.content)

