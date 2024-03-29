# Erase duplicates
export HISTCONTROL=erasedups
export FIGNORE=$FIGNORE:.pyc:.DS_Store
export PYTHONDONTWRITEBYTECODE=1

export ANDROID_HOME=~/android-sdk
export ANDROID_BUILD_TOOLS_VERSION=21.1.1
export ANDROID_PATH=$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/$ANDROID_BUILD_TOOLS_VERSION:$ANDROID_HOME/ndk-bundle

export ANDROID_STUDIO_BIN='/Applications/Android Studio.app/Contents/MacOS'

export XCODE_BIN=/Applications/Xcode.app/Contents/Developer/usr/bin

export PATH=~/bin:/usr/local/bin:$ANDROID_PATH:$PATH:$XCODE_BIN:$ANDROID_STUDIO_BIN

# add depot_tools to path
export PATH=~/workspace/depot_tools:$PATH

# add diffmerge to path
export PATH=$PATH:/Applications/DiffMerge.app/Contents/MacOS

alias lsla="ls -la"


export EDITOR='nano'

hammer ()
{
    ATTEMPT=1
    WAIT_TIME=2
    until ($@); do
        echo "hammer: still broken on attempt $ATTEMPT"
        ATTEMPT=$((ATTEMPT+1))
        sleep $(( WAIT_TIME ))
    done
    echo "hammer: it worked on attempt $ATTEMPT"
}


crowbar ()
{
    ATTEMPT=1
    WAIT_TIME=1
    while ($@); do
        echo "crowbar: still working on attempt $ATTEMPT"
        ATTEMPT=$((ATTEMPT+1))
        sleep $(( WAIT_TIME ))
    done
    echo "crowbar: broke it on attempt $ATTEMPT"
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
alias gf="git fetch --prune --all && gb"
alias gc='clear ; echo -e "\033[32m $ git status\033[0m" ; git status ; echo -e "\033[32m $ gb\033[0m"; gb'
alias gu="git submodule sync && git submodule update --init --recursive"
alias deepclean="gfor git clean -xdf"
alias csvtxt="~/personal/envstuff/csvtxt.py"
alias gitrmdeleted='git status --porcelain | grep "^ D " | sed "s/^ D //" | xargs git rm'

alias gitfire="git checkout -b fire/$USER/$RANDOM ; git commit -m'staged' --allow-empty ; git commit -am'working' --allow-empty ; git add . ; git commit -am'untracked' --allow-empty ; git push -u origin `git branch --no-color | grep \* | cut -d ' ' -f2`"

# Show me all my branches, locally and remote
alias whogit="git for-each-ref --format='%(authoremail) %09 %(refname)' --sort=committerdate"
alias mygit="whogit | grep `git config --get user.email`"

# android aliases
alias logcat="adb logcat -v time"
alias greplog="adb logcat -v time | grep --color"
