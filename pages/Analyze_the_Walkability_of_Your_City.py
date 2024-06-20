import streamlit as st
from openai import OpenAI
from PIL import Image
import openai
import os
import base64
import requests

openai.api_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()

st.markdown("# How Walkable is Your City? 📊")
st.sidebar.markdown("# Analyze the Walkability of Your City")

st.write("")
st.write("Capture the essence of your city to uncover potential barriers to walkability. Share an image to shed light on areas that may hinder pedestrian-friendly experiences in San Jose and receive tailored recommendations to enhance the city's walkability. Our AI-powered tool will analyze the image and provide insights on how to improve the urban landscape for a more vibrant and accessible community. Let's work together to make San Jose a more walkable city!")

st.write("")
st.write("**Notice of Consent:** By submitting an image, you agree to share it with our AI model for analysis. The image will be used solely for the purpose of providing insights on walkability and will not be stored or shared with third parties.")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
st.write("*"*40)

uploaded_file = st.file_uploader("**Submit an Image of Your City Below:**", type=['jpg', 'png', 'jpeg'])
if uploaded_file is not None:
    # Convert the file to an image
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Save the image to the "images" folder
    image_path = os.path.join(script_dir, "images", uploaded_file.name)
    uploaded_image.save(image_path)

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    # Create a placeholder for the status message
    status_message = st.empty()
    status_message.write("Analyzing the image...")

    payload = {
      "model": "gpt-4-turbo",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "What’s in this image? The answer to this first question should be titled in a larger font and bolded 'Analysis of the Image' followed by a new line\
                How can it contribute to the level of walkability in a city? The answer to this second question should be \
                  titled in a larger font and bolded 'Contributions to Walkability' followed by a new line\
                    What can be done to improve these features in the photo to make a city more pedestrian friendly?\
                      The answer to this third question should be titled in a larger font and bolded 'Improvements for Pedestrian Friendliness' followed by a new line"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers = headers, json=payload)

# Print the entire response
    chat_response = response.json()['choices'][0]['message']['content']
    
    # Split the chat response into lines
    lines = chat_response.split('  ')

    # Join the lines with newline characters
    chat_response = '\n'.join(lines)

    st.write(chat_response)

    # Create a button for reporting the issue
    if st.button('Report this issue'):
        # Write the chat response to the "results.txt" file
        with open('results.txt', 'a') as f:
            f.write(chat_response + '\n')

        st.write("Thank you for reporting the issue. Our team will review the feedback and take appropriate action. If it appears that the issue is severe enough, we will file a report to your local government to bring awareness to this issue.")
