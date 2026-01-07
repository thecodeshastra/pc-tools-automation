#!/usr/bin/env bash

TARGET_HOME_FOLDER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/home"

# List of paths to backup (relative to $HOME)
PATHS_TO_BACKUP=(
    ".bashrc"
    ".gitconfig"
    ".local/share/fonts"
    ".ssh"
)

# backup home folder
backup_home_folder() {
    echo "Backing up home folder"
    if [[ -d "$HOME" ]]; then
        for path in "${PATHS_TO_BACKUP[@]}"; do
            source_path="$HOME/$path"
            target_path="$TARGET_HOME_FOLDER/$path"
            
            if [[ -e "$source_path" ]]; then
                echo "Copying $path"
                mkdir -p "$(dirname "$target_path")"
                
                # For directories, add trailing slash to copy contents, not the folder itself
                if [[ -d "$source_path" ]]; then
                    rsync -aAXHv --numeric-ids \
                        --exclude=".cache" \
                        --exclude=".local/share/Trash" \
                        "$source_path/" "$target_path/"
                else
                    rsync -aAXHv --numeric-ids \
                        --exclude=".cache" \
                        --exclude=".local/share/Trash" \
                        "$source_path" "$target_path"
                fi
            else
                warn "Path not found: $path"
            fi
        done
    else
        warn "Home backup not found"
    fi
}

backup_home_folder