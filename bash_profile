
# highlight different files
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

parse_git_branch ()
{
    if git rev-parse --git-dir --no-color >/dev/null 2>&1
    then
        gitver="$(git branch --no-color 2>/dev/null| sed -n '/^\*/s/^\* //p')"
    else
        return 0
    fi
    echo -e $gitver
}

arrow_color()
{
    if [ "$?" = "0" ] ; then
        color="${c_green}"
    else
        color="${c_red}"
    fi
    echo -ne "${color}"
}

branch_color ()
{
    if git rev-parse --git-dir >/dev/null 2>&1
    then
        color=""
        if git diff --quiet 2>/dev/null >&2
        then
            color="${c_green}"
        else
            color="${c_red}"
        fi
    else
        return 0
    fi
    echo -ne $color
}

gl () {
    if [ -z "$1" ]
    then
        git log $(git merge-base origin/master HEAD)^.. --oneline
    else
        git log $(git merge-base origin/$1 HEAD)^.. --oneline
    fi
}

ssh_target () {
    if [ -n "$SSH_CLIENT" ]
    then
        echo -ne "${c_purple}@$HOSTNAME "
    fi
}

PS1='\[$(arrow_color)\]→ \[$(ssh_target)\]\[$(branch_color)\]$(parse_git_branch)\[${c_sgr0}\]\[${c_gray}\]$(git log -1 --format=" %h " 2>/dev/null)\[${c_cyan}\]\W\[${c_sgr0}\]$ '

if [ `uname` == Darwin ]; then
  # Add git completion from Homebrew installation of Git on OSX
  source /usr/local/etc/bash_completion.d/git-completion.bash
fi

c_yellow=`tput setaf 3`
c_blue=`tput setaf 4`
c_purple=`tput setaf 5`
c_gray=`tput setaf 8`
c_gray2=`tput setaf 7`
c_cyan=`tput setaf 6`
c_red=`tput setaf 1`
c_green=`tput setaf 2`
c_sgr0=`tput sgr0`

# minimal import of other stuff
export ENVSTUFF=~/personal/envstuff

# pull in base stuff
source $ENVSTUFF/shell/jeff.sh
source $ENVSTUFF/shell/skydio.sh
