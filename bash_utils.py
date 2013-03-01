import os, sys, subprocess, random, re
    
class BC:
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[30m'
    RED = '\033[31m'
    RED_BOLD = '\033[1;31m'
    GREEN = '\033[32m'
    GREEN_BOLD = '\033[1;32m'
    YELLOW = '\033[33m'
    YELLOW_BOLD = '\033[1;33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    ENDC = '\033[0m'

    def disable(self):
        self.RED = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.BLUE = ''
        self.PURPLE = ''
        self.CYAN = ''
        self.ENDC = ''

def main():
    if len(sys.argv)==1:
        print "Which util? -- [git_branch_status]"
        return 1
    if sys.argv[1] == "git_branch_status":
        return git_branch_status(sys.argv[2:])
    if sys.argv[1] == "git_branch_pull_upstream":
        return git_branch_pull_upstream(sys.argv[2:])
    if sys.argv[1] == "test":
        return test(sys.argv[2:])
    print "Unknown util: "+sys.argv[1]
    return 1

def git_branch_pull_upstream(args):
    dryrun = True if "-n" in args else False
    force = True if "-f" in args else False
    loud = True if "-q" not in args else False
    if len(args) < 1:
        print "usage: git_branch_pull_upstream <localbranch> [-f] [-q] [-n]"
        return
    branch = args[0]
    localbranches = bash_output("git branch --no-color --list '%s'" % branch)
    if localbranches is None:
        # not a git repo; user already warned via stdout
        return
    if localbranches not in ("  "+branch+"\n", "* "+branch+"\n"):
        print localbranches
        print "error: '%s' is not a local branch" % branch
        return
    upstream = bash_output("git for-each-ref --format='%%(upstream:short)' -- 'refs/heads/%s'" % branch).strip()
    if not upstream:
        print "error: '%s' has no upstream" % branch
        return
    branch_sha = git_merge_base(branch)
    upstream_sha = git_merge_base(upstream)
    if branch_sha == upstream_sha:
        print "Already up to date."
        return
    mergebase = git_merge_base(branch_sha, upstream_sha)
    ahead = git_diff_count(mergebase, branch_sha)
    behind = git_diff_count(mergebase, upstream_sha)
    plus = colored("+%d" % ahead, BC.GREEN_BOLD) if ahead else ""
    minus = colored("-%d" % behind, BC.RED_BOLD) if behind else ""
    plusminus = "<%s>" % ("%s %s" % (plus, minus)).strip()
    if ahead and not force:
        print "error: can't pull %s upstream to %s <+%s -%s> (%s..%s) (Forced update required)" % (branch, upstream, ahead, behind, branch_sha[:7], upstream_sha[:7])
        return
    verb = "would pull" if dryrun else "pulling"
    print "%s %s upstream to %s %s (%s..%s)" % colored_l((verb, branch, upstream, plusminus, branch_sha[:7], upstream_sha[:7]), (None, BC.GREEN, BC.CYAN, None, None, None))
    if dryrun:
        return
    gitfolder = get_git_folder()
    reffile = os.path.join(gitfolder, "refs", "heads", branch)
    if not os.path.isfile(reffile):
        print "fatal: reffile not a file: %s" % reffile
    if open(reffile).read() != branch_sha + "\n":
        print "fatal: reffile contents not as expected"
    with open(reffile,'w') as f:
        f.write(upstream_sha+"\n")
    
def git_branch_status(args):
    verbose = True if "-v" in args else False
    output = bash_output('git branch --no-color -v -v')
    if not output:
        return
    lines = output.splitlines()
    rows = []
    lm = re.compile("(?P<current>[*]?)\s*(?P<local>(\S|no branch)+)(?P<localpad>\s+?)(?P<sha>[0-9a-f]+)\s+(\[(?P<remote>[^]]+)\])? ?(?P<message>.*)$")
    rm = re.compile("(?P<branch>\S+)(:|$)\s*(ahead (?P<ahead>\d+))?,?\s*(behind (?P<behind>\d+))?") #origin/foo: ahead 5, behind 5
    for line in lines:
        line = line.strip()
        row = {"padding":"#  "}
        rows.append(row)
        match = lm.match(line)
        remote = match.group("remote") if match.group("remote") else ""
        row["sha"] = BC.LIGHT_GRAY+match.group("sha")+BC.ENDC
        row["message"] = BC.LIGHT_GRAY+match.group("message")+BC.ENDC
        row["current"] = BC.YELLOW+u"\u2713"+BC.ENDC if match.group("current") else ""
        color = BC.GREEN if match.group("current") else ""
        row["branch"] = color+match.group("local")+BC.ENDC+" "
        if remote:
            rmatch = rm.match(remote)
            row["ahead"] = BC.GREEN_BOLD+"+"+rmatch.group("ahead")+BC.ENDC if rmatch.group("ahead") else ""
            row["behind"] = BC.RED_BOLD+"-"+rmatch.group("behind")+BC.ENDC if rmatch.group("behind") else ""
            row["remoteBranch"] = BC.CYAN+rmatch.group("branch")+BC.ENDC
        else:
            row["ahead"] = ""
            row["behind"] = ""
            row["remoteBranch"] = BC.PURPLE+"<local>"+BC.ENDC
    cols = ["padding","branch","current","ahead","behind","remoteBranch","sha"]
    if verbose: cols += ["message"]
    counts={}
    for col in cols: 
        counts[col] = 0
    for row in rows:
        for col in cols: 
            counts[col] = max(counts[col], vislen(row[col]))
    for col, count in counts.items():
        if count == 0:
            cols.remove(col)
    for row in rows:
        for col in cols:
            print visljust(row[col], counts[col]),
        print ""

def get_git_folder():
    path = os.path.abspath(".")
    while path != "/" and ".git" not in os.listdir(path):
        path = os.path.dirname(path)
    path = os.path.join(path, ".git")
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        relpath = re.match(r"gitdir:\s*(?P<path>.*)\s*", open(path).read()).group("path")
        return os.path.normpath(os.path.join(path, "..", relpath))
    else:
        return None        

def colored(value, color):
    if color:
        return color + str(value) + BC.ENDC
    return str(value)
def colored_l(values, colors):
    return tuple(colored(value, color) for value, color in zip(values, colors))

def git_diff_count(fromRef, toRef):
    return int(bash_output("git rev-list %s..%s | wc -l" % (fromRef, toRef)).strip())

def git_merge_base(refname, alt=None):
    if not alt:
        alt = refname
    sha = bash_output("git merge-base '%s' '%s'" % (refname, alt))
    if sha and len(sha.strip()) == 40:
        return sha.strip()

def bash_output(command, raiseError=False):
    try:
        return subprocess.check_output(command, shell=True)
    except:
        if raiseError:
            raise

def visljust(string, width):
    len = vislen(string)
    return string + "".ljust(width-len)

def vislen(string):
    return len(re.sub("\x1b\[(\d+;)?\d+m","",string))

def test(args):
    foo = BC.GREEN+"foo"+BC.ENDC
    foolen=vislen(foo)
    if not foolen==3: raise AssertionError("vislen("+repr(foo)+") should be 3 - was "+str(foolen))
    print "All tests passed"

if __name__ == "__main__":
    sys.exit(main())
