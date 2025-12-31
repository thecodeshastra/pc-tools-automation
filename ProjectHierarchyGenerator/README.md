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