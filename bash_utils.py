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
    if sys.argv[1] == "test":
        return test(sys.argv[2:])
    print "Unknown util: "+sys.argv[1]
    return 1

def git_branch_status(args):
    verbose = True if "-v" in args else False
    filename = "/tmp/git_branch_status_"+str(random.randint(1000,9999))+".txt"
    try:
        writefile = open(filename,"w")
        errorcode = subprocess.call(["git","branch","--no-color","-v","-v"], stdout=writefile)
        writefile.close()
        if not errorcode:
            readfile = open(filename)
            lines = readfile.readlines()
            readfile.close()
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
    finally:
        try: os.remove(filename)
        except: pass
   
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