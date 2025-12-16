"""CodiFlowSystems License Maker
This script generates an encrypted license file for a client using their email,
expiry date, MAC address, and tool name.
It uses the cryptography library to handle encryption."""


import sys
import json
import uuid
import os
from datetime import datetime
import hmac
import hashlib
from cryptography.fernet import Fernet


# ---------- CONFIG FILES ----------
FERNET_KEY_PATH = "secret.key"
HMAC_KEY_PATH = "hmac.key"

# ---------- ONE-TIME KEY SETUP ----------
def generate_keys():
    """Generate Fernet and HMAC keys if they do not exist.
    """
    if not os.path.exists(FERNET_KEY_PATH):
        with open(FERNET_KEY_PATH, "wb") as f:
            f.write(Fernet.generate_key())
        print("✅ Fernet encryption key generated.")
    if not os.path.exists(HMAC_KEY_PATH):
        hmac_key = uuid.uuid4().hex.encode()
        with open(HMAC_KEY_PATH, "wb") as f:
            f.write(hmac_key)
        print("✅ HMAC signature key generated.")


# ---------- SIGN LICENSE ----------
def generate_signature(hmac_key, license_data):
    """Generate a HMAC signature for the license data.
    This ensures the integrity and authenticity of the license.
    
    Args:
        hmac_key (bytes): The HMAC key used for signing.
        license_data (dict): The license data to sign.
    Returns:
        str: The HMAC signature as a hexadecimal string.
    """
    msg = f"{license_data['user']}_{license_data['expiry']}_{license_data['license_id']}"
    return hmac.new(hmac_key, msg.encode(), hashlib.sha256).hexdigest()


# ---------- MAIN LICENSE CREATOR ----------
def generate_license(
        user_email: str,
        mac_id: str,
        expiry_date: str,
        tool_name: str,
        lic_type: str
):
    """Generate a license file for the given user.
    Encrypts the license data and saves it to a file.

    Args:
        user_email (str): The email of the user.
        mac_id (str): The MAC address of the user's machine.
        expiry_date (str): The expiry date of the license in YYYY-MM-DD format.
        tool_name (str): The name of the tool for which the license is generated.
        lic_type (str): The type of license (e.g., "yearly", "monthly").
    Returns:
        None: Writes the encrypted license to a file.
    """
    # Ensure keys are generated
    generate_keys()
    # Load keys
    with open(FERNET_KEY_PATH, "rb") as f:
        fernet_key = f.read()
    with open(HMAC_KEY_PATH, "rb") as f:
        hmac_key = f.read()
    # Create Fernet instance
    fernet = Fernet(fernet_key)
    # Generate license data
    license_data = {
        "user": user_email,
        "product": tool_name,
        "license_id": str(uuid.uuid4()),
        "issued": datetime.now().strftime("%Y-%m-%d"),
        "expiry": expiry_date,
        "type": lic_type,  # you can change to "monthly", etc.
        "features": ["archive_project", "json_export", "usd_support"],
        "machine_id": mac_id,
        "licensor": "CodiFlowSystems",
        "contact_email": "codiflowsystems@gmail.com",
        "license_key": fernet_key.decode(),
    }
    # Generate HMAC signature
    if not hmac_key:
        raise ValueError("HMAC key is missing. Please generate keys first.")
    license_data["signature"] = generate_signature(hmac_key, license_data)
    # Encrypt the license data
    if not fernet_key:
        raise ValueError("Fernet key is missing. Please generate keys first.")
    encrypted = fernet.encrypt(json.dumps(license_data).encode())
    # Save the encrypted license to a file
    user = user_email.split("@")[0].replace(".", "_")
    license_output = f"{user}_{tool_name}.lic"
    with open(license_output, "wb") as f:
        f.write(encrypted)
    # Output success message
    print(f"✅ License generated and encrypted for: {user_email}")
    print(f"📂 Saved as: {license_output}")

# 🔁 Generate license
# generate_license("client@studio.com", "2025-06-30", "00:1A:2B:3C:4D:5E", "CodiFlowTool")

# Run via command-line
if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: "
            "python3 generate_license.py <email> "
            "<expiry_date YYYY-MM-DD> <client_mac_address> <tool_name> <license_type>"
        )
        sys.exit(1)
    u_email = sys.argv[1]
    expiry = sys.argv[2]
    client_mac_address = sys.argv[3]
    tool = sys.argv[4]
    lic_t = sys.argv[5]
    #  Generate keys if not present
    generate_license(u_email, expiry, client_mac_address, tool, lic_t)
