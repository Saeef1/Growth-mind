import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import json
import os
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac
import time

User_DATA_FILE = "secure.json"
SALT = b"secure_salt_value"

failed_attempts = 0
LOCKED = 60

st.title("Secure Login System")

if "authenticate_user" not in st.session_state:
    st.session_state["authenticate_user"] = None
    st.session_state["failed_attempts"] = 0
    st.session_state["locked"] = 0

def load_data():
    if os.path.exists(User_DATA_FILE):
        try:
            with open(User_DATA_FILE, "r") as file:
                content = file.read()
                if not content.strip():  # If file is empty
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            st.warning("Error loading data. File may be corrupted. Initializing new data file.")
            # Create a new empty data file
            with open(User_DATA_FILE, "w") as file:
                json.dump({}, file)
            return {}
    else:
        # Create the file if it doesn't exist
        with open(User_DATA_FILE, "w") as file:
            json.dump({}, file)
        return {}

def encode_bytes(obj):
    if isinstance(obj, bytes):
        return urlsafe_b64encode(obj).decode('utf-8')
    return obj

def save_data(data):
    try:
        serializable_data = {}
        for user, info in data.items():
            serializable_data[user] = {
                "password": encode_bytes(info["password"]),
                "data": info["data"]
            }
        # Write to a temporary file first
        temp_file = User_DATA_FILE + ".tmp"
        with open(temp_file, "w") as file:
            json.dump(serializable_data, file)
        # Atomic rename
        os.replace(temp_file, User_DATA_FILE)
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        raise

def passKey_hash(passkey):
    key = pbkdf2_hmac(
        'sha256',
        passkey.encode(),
        SALT,
        100000
    )
    return urlsafe_b64encode(key)

def password_hash(password):
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        SALT,
        100000
    )
    return urlsafe_b64encode(key).decode('utf-8')

def encrypt_data(data,key):
    chiper = Fernet(passKey_hash(key))
    return chiper.encrypt(data.encode()).decode()

def decrypt_data(encrypt_data,key):
    try:
        chiper = Fernet(passKey_hash(key))
        return chiper.decrypt(encrypt_data.encode()).decode()
    except:
        return None

stored_data = load_data()

menu = ["Home","Register","Login","Store","Retrive"]
if st.session_state["authenticate_user"]:
    menu.append("Logout")

choice = st.sidebar.selectbox("Navigation",menu)

if choice == "Home":
    st.subheader("Home")
    st.markdown("welcome to the secure login system")
    st.markdown("Please register or login to access secure features.")

elif choice == "Register":
    st.subheader("Register")
    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Registered"):
        if user_name and password:
            if user_name in stored_data:
                st.warning("User already exists")
            else:
                stored_data[user_name] = {
                    "password" : password_hash(password),
                    "data" : []
                }
                save_data(stored_data)
                st.success("User registered successfully")
        
        else:
            st.error("Please fill in all fields")
elif choice == "Login":
    st.subheader("Login")

    if time.time() < st.session_state["locked"]:
       remaining = int(st.session_state["locked"] - time.time()) 
       st.error(f"Account locked. Try again in {remaining} seconds.")
       st.stop()

    user_name = st.text_input("Username")
    password = st.text_input("Password", type="password")       

    if st.button("Login"):
        if user_name in stored_data and stored_data[user_name]["password"] == password_hash(password):
            st.session_state["authenticate_user"] = user_name
            st.session_state["failed_attempts"] = 0
            st.success(f'Welcome {user_name}')
        
        else:
            st.session_state["failed_attempts"] += 1
            remaining = 3 - st.session_state["failed_attempts"]
            st.warning(f"Invalid credentials. {remaining} attempts left.")
            if st.session_state["failed_attempts"] >= 3:
                 
                st.session_state["locked"] = time.time() + LOCKED
                st.error("too many attempts fail. try agian after 60 sec. ")
                st.stop()
elif choice == "Store":
    if not st.session_state["authenticate_user"]:
        st.warning("Please login to access this feature.")
    else:
        st.subheader("Store Data")
        data = st.text_area("Data to store")
        passkey = st.text_input("passkey", type = "password")

        if st.button("encrypt and save"):
            if data and passkey:
                encrypt = encrypt_data(data,passkey)
                stored_data[st.session_state["authenticate_user"]]["data"].append(encrypt)
                save_data(stored_data)
                st.success("Data stored successfully")
            else:
                st.error("please fill in all fields")

elif choice == "Retrive":
    if not st.session_state["authenticate_user"]:
        st.warning("Please login to access this feature.")
    else:
        st.subheader("Retrive Data")
        user_data = stored_data.get(st.session_state["authenticate_user"], {}).get("data",[])

        if not user_data:
            st.info('No data found')
        else:
            for i, data in enumerate(user_data):
                st.code(data, language="text")
            
            encrypted_input = st.text_area("Enter encrypted data to decrypt")
            passkey = st.text_input("passkey", type = "password")

            if st.button("Decrypt"):

                result = decrypt_data(encrypted_input,passkey)

                if not result:
                    st.error("Decryption failed. Please check the passkey.")
                else:
                    st.success(f"decrypted data: {result}")

elif choice == "Logout":
    st.session_state["authenticate_user"] = None
    st.session_state["failed_attempts"] = 0
    st.success("Logged out successfully")