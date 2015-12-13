# Erase duplicates
export HISTCONTROL=erasedups
export FIGNORE=$FIGNORE:.pyc:.DS_Store
export PYTHONDONTWRITEBYTECODE=1

export ANDROID_HOME=~/android-sdk
export ANDROID_BUILD_TOOLS_VERSION=21.1.1
export ANDROID_PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/$ANDROID_BUILD_TOOLS_VERSION:$ANDROID_HOME/ndk-bundle

export ANDROID_STUDIO_BIN='/Applications/Android Studio.app/Contents/MacOS'

export XCODE_BIN=/Applications/Xcode.app/Contents/Developer/usr/bin

export PATH=~/bin:/usr/local/bin:$PATH:$ANDROID_PATH:$XCODE_BIN:$ANDROID_STUDIO_BIN

# add depot_tools to path
export PATH=~/workspace/depot_tools:$PATH

# add diffmerge to path
export PATH=$PATH:/Applications/DiffMerge.app/Contents/MacOS

alias lsla="ls -la"


export EDITOR='nano'

hammer ()
{
    WAIT_TIME=2
    until ($@); do
           sleep $(( WAIT_TIME ))
    done
}

crowbar ()
{
    WAIT_TIME=1
    while ($@); do
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
