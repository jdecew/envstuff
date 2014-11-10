
# highlight different files
export CLICOLOR=1
export LSCOLORS=ExFxCxDxBxegedabagacad

# Erase duplicates
export HISTCONTROL=erasedups
#export PS1="\[\033[0;31m\]\W\[\033[0m\]$ "
export FIGNORE=$FIGNORE:.pyc:.DS_Store

export ENVSTUFF=~/personal/envstuff

export ANDROID_HOME=~/android-sdk
export ANDROID_BUILD_TOOLS_VERSION=android-4.4W
export ANDROID_PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/$ANDROID_BUILD_TOOLS_VERSION

export XCODE_BIN=/Applications/Xcode.app/Contents/Developer/usr/bin

export PATH=~/bin:/usr/local/bin:$PATH:$ANDROID_PATH:$XCODE_BIN

source /usr/local/etc/bash_completion.d/git-completion.bash

c_yellow=`tput setaf 3`
c_blue=`tput setaf 4`
c_purple=`tput setaf 5`
c_gray=`tput setaf 8`
c_gray2=`tput setaf 7`
c_cyan=`tput setaf 6`
c_red=`tput setaf 1`
c_green=`tput setaf 2`
c_sgr0=`tput sgr0`

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

#PS1='\[${c_cyan}\]\W\[${c_sgr0}\] (\[$(branch_color)\]$(parse_git_branch)\[${c_sgr0}\])$ '
#PS1='\[$(branch_color)\]$(parse_git_branch)\[${c_sgr0}\]:\[${c_cyan}\]\W\[${c_sgr0}\]$ '
PS1='\[$(branch_color)\]$(parse_git_branch)\[${c_sgr0}\]\[${c_gray}\]$(git log -1 --format=" %h " 2>/dev/null)\[${c_cyan}\]\W\[${c_sgr0}\]$ '

# bash aliases
alias bash_update="source ~/.bash_profile"
alias la="ls -a"
alias lsla="ls -la"

hammer ()
{
    WAIT_TIME=2
    until ($@); do
           sleep $(( WAIT_TIME ))
    done
}

OK () {
  CODE=$?
  if [ "$CODE" == 0 ]
  then
    printf "\a" ; say OK
  else
    printf "\a\a" ; say ERROR. $CODE
  fi
}

alias internet='hammer curl http://www.google.com > /dev/null ; say "The Internet is BACK"'

# git alias
function gfor() { $*; git submodule foreach --recursive $*;}
alias gs="git status"
alias gd="git diff"
alias gb="python ~/personal/envstuff/bash_utils.py git_branch_status"
alias gbpu="python ~/personal/envstuff/bash_utils.py git_branch_pull_upstream"
alias gf="git fetch --all && gb"
alias gc='clear ; echo -e "\033[32m $ git status\033[0m" ; git status ; echo -e "\033[32m $ gb\033[0m"; gb'
alias gu="git submodule sync && git submodule update --init --recursive"
alias deepclean="gfor git clean -xdf"
alias csvtxt="~/personal/envstuff/csvtxt.py"
alias gitrmdeleted='git status --porcelain | grep "^ D " | sed "s/^ D //" | xargs git rm'

# android aliases
alias logcat="adb logcat -v time"
alias greplog="adb logcat -v time | grep --color"
