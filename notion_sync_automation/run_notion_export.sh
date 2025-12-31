#!/bin/bash

# Environment variable: path to notion_sync_automation folder
NOTION_SYNC_SOURCE="/home/rudra/DEV_ROOT/PC-Tools-Automation/notion_sync_automation"

# Get the directory where this script is running
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUN_DIR="$(pwd)"

# Use NOTION_SYNC_SOURCE if provided, otherwise use the script's directory
SOURCE_PATH="${NOTION_SYNC_SOURCE}"
if [[ ! -d "$SOURCE_PATH" ]]; then
    echo "Error: Source path '$SOURCE_PATH' does not exist"
    exit 1
fi

# Files to copy
FILES_TO_COPY=(
    "sync_notion_export.py"
    "converter.py"
    "constants.py"
    "__init__.py"
    "requirements.txt"
)

# Track copied files for cleanup
COPIED_FILES=()

# Use current working directory as destination
WORK_DIR="$RUN_DIR/notion_sync_automation"
[ -d "$WORK_DIR" ] || mkdir "$WORK_DIR"
echo "Working directory: $WORK_DIR"

# Copy files from source to current directory
echo "Copying files from $SOURCE_PATH to $WORK_DIR..."
for file in "${FILES_TO_COPY[@]}"; do
    if [[ -f "$SOURCE_PATH/$file" ]]; then
        cp "$SOURCE_PATH/$file" "$WORK_DIR/"
        COPIED_FILES+=("$WORK_DIR/$file")
        echo "  ✓ Copied: $file"
    else
        echo "  ✗ Warning: File not found: $file"
    fi
done

# Install requirements if exists
if [[ -f "$WORK_DIR/requirements.txt" ]]; then
    echo ""
    echo "Installing requirements..."
    if pip install -q -r "$WORK_DIR/requirements.txt"; then
        echo "  ✓ Requirements installed successfully"
    else
        echo "  ✗ Failed to install requirements"
        rm -rf "$WORK_DIR"
        exit 1
    fi
fi

# Run the sync script
echo ""
echo "Running sync_notion_export.py..."

if python3 "$WORK_DIR/sync_notion_export.py"; then
    echo ""
    echo "✓ Script executed successfully"
    
    # Cleanup copied files
    echo "Cleaning up copied files..."
    for file in "${COPIED_FILES[@]}"; do
        rm -f "$file"
        echo "  ✓ Deleted: $(basename $file)"
    done
    echo "Cleaning up working directory..."
    rm -rf "$WORK_DIR"
    echo "✓ Cleanup completed"
    exit 0
else
    echo ""
    echo "✗ Script failed to execute"
    
    # Keep files for debugging if execution fails
    echo "Copied files kept at: $WORK_DIR (for debugging)"
    exit 1
fi
