# PC_TOOLS_AUTOMATION
Al personal tools and automation scripts.


## 1. Bootstrap (`bootstrap`)
**Purpose:**
Bootstrap your workstation with all required tools and configurations.
### Step-by-Step Guide:
1. **Navigate to Bootstrap Tool:**
    - Enter the `bootstrap` directory.
2. **Run Bootstrap Script:**
    - Run the bootstrap script as per your standard (this might be `./bootstrap.sh` or a similar command, adapting parameters as needed).
    - The script will process files in your source directory, producing an encrypted/obfuscated version in an output or `dist` directory.


---
## 2. Deployment Encryption (`deploy_encryptor`)
**Purpose:**
Secure the tool’s source code before distribution by encrypting or obfuscating it, ensuring intellectual property protection.
### Step-by-Step Guide:
1. **Preparation:**
    - Complete all development and license integration steps prior to encryption.
    - Ensure the latest license checker and related modules are present in your codebase.
2. **Navigate to Encryption Tool:**
    - Enter the `deploy_encryptor` directory.
3. **Encrypt Tool for Deployment:**
    - Run the relevant encryption/deployment script as per your standard (this might be `python3 encrypt_tool.py <src_dir> <output_dir>` or a similar command, adapting parameters as needed).
    - The script will process files in your source directory, producing an encrypted/obfuscated version in an output or `dist` directory.
4. **Quality Check:**
    - Test the produced encrypted version to verify normal operation and license enforcement.
5. **Distribution:**
    - Deliver only the encrypted build (not the original source) to the client, alongside any required license/key files.


---
## 3. License File Generation \& Integration (`license_maker`)
**Purpose:**
Create secure, client-specific license files and integrate license checking into your tool.
### Step-by-Step Guide:
1. **Trigger Licensing Post-Development:**
    - Once the tool is ready and requested by a client, gather necessary client details:
        - Email
        - License expiry date (YYYY-MM-DD format)
        - Client's MAC address
        - Tool name
        - License type (e.g., trial, full, subscription)
2. **Navigate to License Tool:**
    - Go to the `license_maker` directory.
3. **Generate License and Key Files:**
    ```bash
    python3 generate_license.py <client_email> <expiry_date YYYY-MM-DD> <client_mac_address> <tool_name> <license_type>
    ```
    - This will create `hmac.key` and `secret.key` files in the `license_maker` directory.
4. **Integrate Keys and License Checker:**
    - Open the generated keys.
    - Copy their contents into the relevant constants inside `license_checker.py` (in the same directory).
5. **Deploy License Checker:**
    - Copy the updated `license_checker.py` into your tool’s `src` directory.
    - In your tool’s core code, import and invoke `license_checker.py` functions before running any major process, ensuring only licensed clients can operate the tool.


---
## 4. Project Initialization (`project_initiator`)
**Purpose:**
Streamline the creation of new tool repositories with all required directories and templates.
### Step-by-Step Guide:
1. **New Repository Creation:**
    - On the organization GitHub (CodiFlowSystems), create a new repository.
    - Use the desired tool or project name as the repository name.
2. **Initialize Project Structure:**
    - Navigate to the `project_initiator` directory in your local system.
    - Prepare your configuration `json_file_path` specifying directory and file templates.
    - Choose or create the destination directory (`dest_dir_path`) for project files.
3. **Run the Initialization Script:**
    ```bash
    python3 ./project_initiator.py json_file_path dest_dir_path
    ```
    - This script will generate all specified directories and scaffold files in your destination path, based on the provided JSON configuration.


---
## 5. ProjectHierarchyGenerator (`project_hierarchy_generator`)
**ProjectHierarchyGenerator** is a simple, customizable folder structure generator designed for **freelancers** and **small studios** to help maintain a clean, consistent, and uniform project hierarchy — all with a single click. It handles all Assets, sequences and shots hierarchy internally.

### 🚀 Features
- ✅ **One-click project hierarchy creation**
- 🔄 **JSON-based structure definition** – Easily update the hierarchy by editing a single JSON file.
- 🧠 **Smart regeneration** – Works on existing projects without overwriting valid existing folders.
- ⏱️ **Time-saving** – Drastically reduces setup time for new projects.
- 🤝 **Team-friendly** – Ensures consistent structure across all artists and teams.

### 🛠 How It Works
- Reads your folder structure from a customizable JSON file.
- Automatically generates the entire folder tree.
- Checks for existing folders and avoids duplication.
- Allows easy updates – just modify the JSON and rerun the tool.

### How to use it
**Steps to create hierarchy**
- Copy `project_hierarchy.bat` to the new shared drive created in your google workspace
- Then double click on that .bat file and it will create all the project folders for you

**Steps to modify hierarchy**
- If you want to change anything in hierarchy just update `project_hierarchy.json` for main folders.
- And for each asset and shot hierarchy we need to modify `assets_hierarchy.json` and `shots_hierarchy.json` respectively.
- Those json files are preety straight forward for root folder just change the root key value, for main folder change name key value and for subfolders change the name inside subfolder list.
- We can also add copy_files keys if we want to copy some basic files by default to any folder created.

**Location to change drive path**
- All `assets_hierarchy.bat, shots_hierarchy.bat, sequence_hierarchy.bat and project_hierarchy.bat` files have 2 location to change.
- First is project root and second is file path either powershell or cs exe.