"""License Checker Module
This module validates a license file for a tool, checking its integrity,
expiry, machine lock, and product compatibility.
It uses Fernet encryption for secure storage and HMAC for signature verification.
It also retrieves the machine's MAC address to enforce machine-specific licensing."""

import os
import json
import hmac
import hashlib
import uuid
from datetime import datetime
from cryptography.fernet import Fernet


#constants
# 🔐 DO NOT EXPOSE THIS KEY — Cython compile this file!
FERNET_KEY = b'your-32-byte-fernet-secret-key=='  # secret key for Fernet encryption
HMAC_SECRET = b'your-hmac-signing-key'            # Separate secret for HMAC
EXPECTED_PRODUCT = "HFilePathManager" # same as the repo name of tool
LICENSE_FILE = "codiflow.lic"  # License file name


# 🧠 Get current machine's MAC address
def get_machine_id():
    """Get the MAC address of the current machine.

    Returns:
        str: The MAC address in the format XX:XX:XX:XX:XX:XX.
    """
    mac = uuid.getnode()
    return ':'.join(['{:02x}'.format((mac >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])

# ✅ Main license validator
def validate_license():
    """Validate the license file.

    Returns:
        dict: The license data if validation is successful.
    Raises:
        RuntimeError: If any validation check fails.
    """
    try:
        # Load encrypted license file
        lic_path = os.path.join(os.path.dirname(__file__), LICENSE_FILE)
        if not os.path.exists(lic_path):
            raise Exception("License file not found.")

        with open(lic_path, "rb") as f:
            encrypted_data = f.read()

        fernet = Fernet(FERNET_KEY)
        decrypted = fernet.decrypt(encrypted_data)
        license_data = json.loads(decrypted.decode())

        # ✅ 1. Verify HMAC Signature
        msg = f"{license_data['user']}_{license_data['expiry']}_{license_data['license_id']}"
        expected_sig = hmac.new(HMAC_SECRET, msg.encode(), hashlib.sha256).hexdigest()
        if license_data.get("signature") != expected_sig:
            raise Exception("License signature invalid or tampered.")

        # ✅ 2. Check Expiry
        expiry = datetime.strptime(license_data["expiry"], "%Y-%m-%d")
        if datetime.now() > expiry:
            raise Exception("License has expired.")

        # ✅ 3. Check Machine Lock (if present)
        machine_id = get_machine_id()
        if license_data.get("machine_id") and license_data["machine_id"] != machine_id:
            raise Exception("This license is not valid on this machine.")

        # ✅ 4. Product/Version match
        if license_data.get("product") != EXPECTED_PRODUCT:
            raise Exception("This license is not valid for this version of the tool.")

        return license_data  # Return full license info for UI
    except Exception as e:
        raise RuntimeError(f"License validation failed:\n{str(e)}")
