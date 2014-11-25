
local ret_status="%(?:%{$fg_bold[green]%}➜ :%{$fg_bold[red]%}➜ %s)%{$reset_color%}"

PROMPT='${ret_status}%{$fg[green]%}%p%{$fg[blue]%}$(git_prompt_info)%{$fg[blue]%} % %{$fg[cyan]%}%1~%{$reset_color%} $ '

ZSH_THEME_GIT_PROMPT_PREFIX=""
ZSH_THEME_GIT_PROMPT_SUFFIX=""
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%}"

function git_hash() {
    hash=$(git --no-pager log -1 --format=':%h' 2>/dev/null)
    echo "%{$fg[yellow]%}${hash}%{$reset_color%}"
}
function git_prompt_info() {
    ref=$(git branch 2>/dev/null) || return
    echo " $(parse_git_dirty)$ZSH_THEME_GIT_PROMPT_PREFIX$(current_branch)$ZSH_THEME_GIT_PROMPT_SUFFIX%{$reset_color%}$(git_hash)"
}
