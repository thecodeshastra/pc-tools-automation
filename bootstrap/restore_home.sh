#!/usr/bin/env bash

SOURCE_HOME_FOLDER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/home"

# restore home folder
restore_home_folder() {
    log "Restoring home folder"
    if [[ -d "$SOURCE_HOME_FOLDER" ]]; then
    log "Restoring home files"
    rsync -aAXHv --numeric-ids \
        --exclude=".cache" \
        --exclude=".local/share/Trash" \
        "$SOURCE_HOME_FOLDER/" "$HOME/"
    else
    warn "Home backup not found"
    fi
}

restore_home_folder