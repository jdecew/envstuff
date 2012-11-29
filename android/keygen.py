#! /usr/bin/env python

import os, re, argparse

def main():

    parser = argparse.ArgumentParser(description='Create a PG Publishing signing key')
    parser.add_argument('developer', metavar='developer', help='The developer (company name) to embed in the signature')
    parser.add_argument('-storepass', metavar='password', help='The password to use for the keystore')
    parser.add_argument('-keypass', metavar='password', help='The password to use for the key')
    parser.add_argument('-alias', metavar='alias', help='The alias to use')
    #parser.add_argument('-add', action='store_true', default=False, help='Add to an existing keystore.')
    parser.add_argument('-f', action='store_true', default=False, help='Force.  Overwrite an existing file.')
    args = parser.parse_args()

    filename = re.sub("[^a-z0-9]+", "", args.developer.lower()) + ".keystore"
    
    error = False
    if ('"' or ',') in args.developer:
        print "Developer name contains invalid chars: "+ args.developer
        error = True
    if args.storepass and len(args.storepass) < 6:
        print "Keytore password must be at least 6 characters"
        error = True
    if args.keypass and len(args.keypass) < 6:
        print "Key password must be at least 6 characters"
        error = True
    if args.alias and not re.match("[a-z0-9]+", args.alias):
        print "Alias must contain only lowercase, alphanumeric characters: "+ args.alias
        error = True
    if not args.f and os.path.exists(filename):
        print "File already exists (use -f to overwrite): "+ filename
        error = True
    if error: return

    ou = args.developer
    alias = args.alias if args.alias else re.sub("[^a-z0-9]+", "", args.developer.lower())
    dname = 'CN=Pocket Gems Publishing, OU=%s, O=Pocket Gems Inc, L=San Francisco, S=California, C=US' % ou

    if args.f and os.path.exists(filename):
        system('rm %s' % filename)
    
    storecreds = ' -storepass "%s"' % (args.storepass) if args.storepass else ''
    allcreds = ' -keypass "%s"%s' % (args.keypass, storecreds) if args.keypass else storecreds
    
    # verify keystore and credentials
    system('keytool -genkey -v -alias %s -keyalg RSA -keystore %s -keysize 2048 -validity 10000 -dname "%s"%s' % (alias, filename, dname, allcreds))
    system('keytool -list -v -keystore %s -alias %s%s' % (filename, alias, storecreds))
    
    print "Success!"

def system(command, raiseOnError=True, desc=None):
    if desc:
        print desc
    retval = os.system(command)
    if retval:
        print "***FAILED***"
        if raiseOnError:
            raise RuntimeError("The command '%s' failed with code %d" % (command, retval))
    return retval


if __name__=="__main__":
    main()