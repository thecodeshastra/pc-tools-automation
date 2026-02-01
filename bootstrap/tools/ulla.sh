install_ulla(){
    echo "Starting installation of ulla-browser"

    # run the official installation wget command
    wget -O install-ulaa-browser.sh https://ulaa.com/release/linux/stable/install-ulaa-browser.sh?isDownload=true 
    # run the installtion
    /bin/bash install-ulaa-browser.sh
}

install_ulla
