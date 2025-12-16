#!/bin/bash

# Define the JSON file path directly in each .sh file
JSON_FILE="LINUXPATH\ProjectHierarchyGenerator\project_hierarchy.json"

# Check if the JSON file exists
if [[ ! -f "$JSON_FILE" ]]; then
    echo "Error: JSON file not found - $JSON_FILE"
    exit 1
fi

# Get project root and its parent directory
PROJECT_ROOT=$(jq -r '.root' "$JSON_FILE")
PROJECT_ROOT_PATH="$(pwd)/$PROJECT_ROOT"
PARENT_ROOT_PATH=$(dirname "$PROJECT_ROOT_PATH")

# Function to create folders and copy files
create_folders() {
    local parent_path="$1"
    local json_data="$2"

    # Extract folder name
    local folder_name
    folder_name=$(echo "$json_data" | jq -r '.root // .name')

    # Create folder
    local folder_path="$parent_path/$folder_name"
    mkdir -p "$folder_path"
    echo "Created: $folder_path"

    # Copy files if specified
    local files
    files=$(echo "$json_data" | jq -r '.copy_files[]?')
    for file in $files; do
        # Replace $PARENT_ROOT$ with actual path
        file_path="${file//PARENT_ROOT/$PARENT_ROOT_PATH}"

        if [[ -f "$file_path" ]]; then
            cp "$file_path" "$folder_path"
            echo "Copied: $file_path to $folder_path"
        else
            echo "File not found: $file_path"
        fi
    done

    # Check if "subfolders" is a string (external JSON reference)
    subfolders=$(echo "$json_data" | jq -r '.subfolders')

    if [[ -n "$subfolders" && "$subfolders" != "null" ]]; then
        if [[ "$subfolders" == *.json ]]; then
            external_json_file="$subfolders"
            external_json_file="${external_json_file//PARENT_ROOT/$PARENT_ROOT_PATH}"
            if [[ -f "$external_json_file" ]]; then
                external_subfolders=$(cat "$external_json_file")
                for subfolder in $(echo "$external_subfolders" | jq -c '.[]'); do
                    create_folders "$folder_path" "$subfolder"
                done
            else
                echo "Warning: External JSON file not found: $external_json_file"
            fi
        else
            for subfolder in $(echo "$json_data" | jq -c '.subfolders[]?'); do
                create_folders "$folder_path" "$subfolder"
            done
        fi
    fi
}

# Start folder creation
json_content=$(cat "$JSON_FILE")
create_folders "$(pwd)" "$json_content"