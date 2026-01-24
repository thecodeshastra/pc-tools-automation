# ~/.bashrc

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# Add custom bin dirs to PATH if not already included
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    export PATH="$HOME/bin:$PATH"
fi

#-----------------------------------------------------------------
# Alias custom
# generic
alias .='cd ..'
alias dev='cd DEV_ROOT'
alias work='cd DEV_ROOT/workspace'
alias sy='cd SATTVICYANTRA_ROOT'

# office
alias somum='cd DEV_ROOT/softwares/vpn_dneg_config && sudo openvpn mumbai_dneg.ovpn'
alias vpnmum='sudo openvpn mumbai_dneg.ovpn'
alias sochn='cd DEV_ROOT/softwares/vpn_dneg_config && sudo openvpn chennai_dneg.ovpn'
alias vpnmum='sudo openvpn chennai_dneg.ovpn'
alias sosyd='cd DEV_ROOT/softwares/vpn_dneg_config && sudo openvpn sydney_dneg.ovpn'
alias solon='cd DEV_ROOT/softwares/vpn_dneg_config && sudo openvpn london_dneg.ovpn'
alias sovan='cd DEV_ROOT/softwares/vpn_dneg_config && sudo openvpn vancouver_dneg.ovpn'
alias somtl='cd DEV_ROOT/softwares/vpn_dneg_config && sudo openvpn montreal_dneg.ovpn'

# git repos
alias gcpta='git clone git@github.com:thecodeshastra/PortfolioToolsAndAutomation.git'
alias gctcs='git clone git@github.com:thecodeshastra/thecodeshastra.git'
alias gccp='git clone git@github.com:thecodeshastra/coding_practice.git'
alias gcaw='git clone git@github.com:thecodeshastra/AI-workbench.git'
alias gcpta='git clone git@github.com:thecodeshastra/PC_TOOLS_AUTOMATION.git'


# env vars
export DEV_ROOT='$HOME/DEV_ROOT'
export DEV_WORK='$DEV_ROOT/WORKSPACE'
export SY_ROOT='$HOME/SATTVICYANTRA_ROOT'
export SY_TOOLS='$SY_ROOT/platform/tools-automations/tools'
export SY_AUTOMATION='$SY_ROOT/platform/tools-automations/automations'
export PYTHONPATH='$DEV_WORK/PortfolioToolsAndAutomation/src/common':$PYTHONPATH
# # windows env vars
# set DEV_ROOT=C:/DEV_ROOT
# set CFS_ROOT=%DEV_ROOT%/SATTVIC_YANTRA_ROOT
# set PYTHONPATH=%DEV_ROOT%/PortfolioToolsAndAutomation/src/common;%PYTHONPATH%

# apps
alias z='zoom'
alias pc='pcoip-client'
alias tor_browser='$HOME/Downloads/tor-browser/start-tor-browser.desktop'
alias renamer='$DEV_ROOT/softwares/inviska_rename.AppImage'
alias qbittorrent='$DEV_ROOT/softwares/qbittorrent.AppImage'
alias kdenlive='$DEV_ROOT/softwares/kdenlive.AppImage'
alias noisetorch='$HOME/.local/bin/noisetorch'

# tools-automations
alias create-gitkeep="$SY_TOOLS/create-gitkeep/run.sh"
alias dir-to-md="$SY_TOOLS/dir-to-md/run.py"

parse_git_branch() {
  git rev-parse --abbrev-ref HEAD >& /dev/null && echo ":{`git rev-parse --abbrev-ref HEAD`}"
}
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$(parse_git_branch)\$ '

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


# opencode
export PATH=/home/rudra/.opencode/bin:$PATH
alias opencode="/home/rudra/.opencode/bin/opencode"
