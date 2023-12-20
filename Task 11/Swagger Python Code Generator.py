# to run app use the following code:
# streamlit run Web_scraping.py
# put the link, for example: https://petstore.swagger.io/v2/swagger.json
# the app takes the link, scrapes json data from the given URL
# creates request, sends to ChatGPT, shows response in the streamlit app

import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# Initialize OpenAI client
client = OpenAI(api_key="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")


def generate_python_code(url):
    # Fetch Swagger JSON from the provided URL
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error: Unable to fetch Swagger JSON from the provided URL. Status Code: {response.status_code}"

    page = response.content
    page = BeautifulSoup(page, 'html.parser')  # change type
    swagger_content = response.text
    prompt = f"Generate a Python class to handle API calls based on the Swagger JSON:\n{swagger_content}\n\n"
    prompt += "Our class should have methods like 'health_check()', 'post_whisper_task(audio_url, whisper_model, language)', and 'get_whisper_output(transaction_id)'.\n"
    prompt += "_base_url = 'custom url'\n\n"
    prompt += 'also in __init__ function we must have headers'
    prompt += '/gw1/whisper/v1/health before all endpoints must be added /gw1'
    prompt += "self.headers = {'x-app-authorization': api_key} header must be like this"

    # Define the chat messages
    messages = [
        {"role": "system", "content": "You are a Python code generator."},
        {"role": "user", "content": prompt},
    ]

    # Set the temperature value, higher value of temperature creates more random answers
    temperature = 0.0

    # Call the OpenAI API to generate Python code based on the chat messages and temperature
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        temperature=temperature
    )

    # Extract the generated Python code from the OpenAI API response
    generated_response = response.choices[0].message.content.strip()
    return generated_response


def main():
    st.title("Swagger Python Code Generator")

    # Get URL input from the user
    url = st.text_input("Enter Swagger JSON URL:")

    # Display submit button
    if st.button("Generate Python Code"):
        if url:
            # Display wait message
            with st.spinner("Generating Python Code. Please wait..."):
                # Generate Python code based on the provided URL
                generated_code = generate_python_code(url)

            # Display the generated code in the app
            st.code(generated_code, language='python')


if __name__ == "__main__":
    main()
