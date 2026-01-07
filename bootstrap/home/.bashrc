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
alias work='cd DEV_ROOT/WORKSPACE'
alias sy='cd SATTVIC_YANTRA_ROOT'
alias sywork='cd SATTVIC_YANTRA_ROOT/WORKSPACE'

# office
alias somum='cd DEV_ROOT/SOFTWARES/vpn_dneg_config && sudo openvpn mumbai_dneg.ovpn'
alias vpnmum='sudo openvpn mumbai_dneg.ovpn'
alias sochn='cd DEV_ROOT/SOFTWARES/vpn_dneg_config && sudo openvpn chennai_dneg.ovpn'
alias vpnmum='sudo openvpn chennai_dneg.ovpn'
alias sosyd='cd DEV_ROOT/SOFTWARES/vpn_dneg_config && sudo openvpn sydney_dneg.ovpn'
alias solon='cd DEV_ROOT/SOFTWARES/vpn_dneg_config && sudo openvpn london_dneg.ovpn'
alias sovan='cd DEV_ROOT/SOFTWARES/vpn_dneg_config && sudo openvpn vancouver_dneg.ovpn'
alias somtl='cd DEV_ROOT/SOFTWARES/vpn_dneg_config && sudo openvpn montreal_dneg.ovpn'

# git repos
alias gcpta='git clone git@github.com:thecodeshastra/PortfolioToolsAndAutomation.git'
alias gctcs='git clone git@github.com:thecodeshastra/thecodeshastra.git'
alias gccp='git clone git@github.com:thecodeshastra/coding_practice.git'
alias gcaw='git clone git@github.com:thecodeshastra/AI-workbench.git'
alias gcpta='git clone git@github.com:thecodeshastra/PC_TOOLS_AUTOMATION.git'

# env vars
export DEV_ROOT='/home/rudra/DEV_ROOT'
export DEV_WORK='$DEV_ROOT/WORKSPACE'
export SY_ROOT='/home/rudra/SATTVIC_YANTRA_ROOT'
export SY_WORK='$SY_ROOT/WORKSPACE'
export PYTHONPATH='$DEV_WORK/PortfolioToolsAndAutomation/src/common':$PYTHONPATH

# apps
alias z='zoom'
alias pc='pcoip-client'
alias tor_browser='/home/rudra/Downloads/tor-browser/start-tor-browser.desktop'
alias renamer='$DEV_ROOT/SOFTWARES/inviska_rename.AppImage'
alias qbittorrent='$DEV_ROOT/SOFTWARES/qbittorrent.AppImage'
alias kdenlive='$DEV_ROOT/SOFTWARES/kdenlive.AppImage'

# Git branch in prompt
parse_git_branch() {
  git rev-parse --abbrev-ref HEAD >& /dev/null && echo ":{`git rev-parse --abbrev-ref HEAD`}"
}
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$(parse_git_branch)\$ '
