import streamlit as st
import dotenv
import os
from openai import AzureOpenAI

dotenv.load_dotenv()
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(api_key=AOAI_KEY, azure_endpoint=AOAI_ENDPOINT, api_version="2024-05-01-preview")

st.title("WELCOME")
st.header("Enter the information of the conditions of your water into the boxes below")

st.subheader("Microbiological Parameters")
e_coli_level = st.text_input("What is the level of E.coli in the water? (CFU/100mL)")
enterococci_level = st.text_input("What is the level of Enterococci in the water? (CFU/100mL)")
pathogens = st.text_input("What Pathogens were in the water? (If none write NONE)")

st.subheader("Chemical Parameters")
ph_level = st.text_input("What is the pH level of the water?")
chlorine_present = st.radio("Is there Chlorine in the water?", ["Yes", "No (Natural water body)"])
nitrogen_concentration = st.text_input("What is the concentration of nitrogen? (mg/L)")
phosphorus_concentration = st.text_input("What is the concentration of phosphorus? (mg/L)")
pesticides = st.text_input("What pesticides were detected? (mg/L) Type NONE if none")
herbicides = st.text_input("What herbicides were detected? (mg/L) Type NONE if none")

if st.button("Submit"):
    user_input = (
        f"E.coli level: {e_coli_level} CFU/100mL\n"
        f"Enterococci level: {enterococci_level} CFU/100mL\n"
        f"Pathogens: {pathogens}\n"
        f"pH level: {ph_level}\n"
        f"Chlorine present: {chlorine_present}\n"
        f"Nitrogen concentration: {nitrogen_concentration} mg/L\n"
        f"Phosphorus concentration: {phosphorus_concentration} mg/L\n"
        f"Pesticides detected: {pesticides}\n"
        f"Herbicides detected: {herbicides}"
    )

    st.session_state.messages = [
        {"role": "system", "content": "You are an AI that determines if the water is safe for swimming given the information provided by the user."},
        {"role": "user", "content": user_input}
    ]

    with st.spinner("Processing..."):
        response = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=st.session_state.messages,
            stream=False,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.95,
        )
    
    response_content = response.choices[0].message.content
    st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})

import datetime 

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText


#def send_email(subject, body, to_email):

# Email account credentials

   # sender_email = "me@gmail.com"

#sender_password = "" # Replace with your actual email password or app-specific password


# Set up the server and login

#server = smtplib.SMTP('smtp.gmail.com', 587)

#server.starttls() # Secure the connection

#server.login(sender_email, sender_password)


# Create the email

#msg = MIMEMultipart()

#msg['From'] = sender_email

#msg['To'] = to_email

#msg['Subject'] = subject

#msg.attach(MIMEText(body, 'plain'))


# Send the email

#server.send_message(msg)

#server.quit()


# Usage

subject = "Recreational Water Safety Information"

body = """Dear Wayland Community,

"""


gptResponse = response_content

body = body + gptResponse;


body = body + """

Sincerely,

Wayland Community Health Department

"""


to_email = "wayland-community@gmail.com"


# settting up email needs an email server; so I am skipping email. Instead I am just writing to a file of what we get from AI (GPT) 

# send_email(subject, body, to_email)


file_name = "recreational-water-report-" + datetime.datetime.now().strftime("%B%d,%Y at %I;%M;%Sp") + ".txt"


with open(file_name, "w") as file:

    file.write(body)