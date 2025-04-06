import streamlit as st
import random
import string

def password_generator(lenght,digit,special_character):
    letter = string.ascii_letters

    if digit:
        letter += string.digits

    if special_character:
        letter += string.punctuation
    
    return ''.join(random.choice(letter) for _ in range(lenght))

st.title("Password Generator")

lenght = st.slider("Select the lenght of password", 8,32,17)

digit = st.checkbox("include digits")

special_character = st.checkbox("include special characters")

if st.button("Generate Password"):
    password = password_generator(lenght,digit,special_character)

    st.write(f"Your password is: {password}")



