#! /usr/bin/env python

import os, argparse

def main():
    credSets = {"debug":("android","androiddebugkey","android"), "pg":("password","alias_name","password")}

    parser = argparse.ArgumentParser(description='Re-sign an APK with a new key')
    parser.add_argument('apkFile', metavar='apk', help='the APK to sign or re-sign')
    parser.add_argument('-out', metavar='outfile', help='location of signed APK (default overwrite apkFile)')
    parser.add_argument('keystore', metavar='keystore', help='keystore to use')
    parser.add_argument('-tmp', metavar='tempfile', default=".resign.apk", help='temporary file to use while resigning')
    parser.add_argument('-c', choices=credSets.keys(), metavar='creds', default="pg", help='keystore credentials set to use')
    parser.add_argument('-ksp', metavar='keystorepass', help='(overrides -c value) keystore password')
    parser.add_argument('-ka', metavar='keyalias', help='(overrides -c value) key alias')
    parser.add_argument('-kp', metavar='keypass', help='(overrides -c value) key password')
    args = parser.parse_args()
    
    #print args

    cKeyStorePass, cKeyAlias, cKeyPass = list(credSets[args.c])
    if args.ksp: cKeyStorePass = args.ksp
    if args.ka: cKeyAlias = args.ka
    if args.kp: cKeyPass = args.kp

    #print cKeyStorePass, cKeyAlias, cKeyPass
    
    error = False
    # check apkfile
    if not os.path.exists(args.apkFile):
        print "Can't find APK: "+ args.apkFile +" ("+ os.path.abspath(args.apkFile) +")"
        error = True
    apkFile = os.path.abspath(args.apkFile)
    if '"' in apkFile:
        print "APK path contains quote (\"): "+ apkFile
        error = True
    # check keystore
    if not os.path.exists(args.keystore):
        print "Can't find Keystore: "+ args.keystore +" ("+ os.path.abspath(args.keystore) +")"
        error = True
    keystore = os.path.abspath(args.keystore)
    if '"' in keystore:
        print "Keystore path contains quote (\"): "+ keystore
        error = True
    # check outfile
    if args.out and not os.path.isdir(os.path.dirname(os.path.abspath(args.out))):
        print "Outfile is not in an existing directory: "+ os.path.dirname(os.path.abspath(args.out))
        error = True
    outFile = os.path.abspath(args.out) if args.out else apkFile
    if '"' in outFile:
        print "Output path contains quote (\"): "+ outFile
        error = True
    # check tmpfile
    if args.tmp and not os.path.isdir(os.path.dirname(os.path.abspath(args.tmp))):
        print "Tempfile is not in an existing directory: "+ os.path.dirname(os.path.abspath(args.tmp))
        error = True
    tmpFile = os.path.abspath(args.tmp)
    if '"' in tmpFile:
        print "Tempfile path contains quote (\"): "+ tmpFile
        error = True
    if error: return

    tmpFile2 = tmpFile+".tmp2"
    tmpFile = tmpFile+".tmp1"
    
    # verify keystore and credentials
    if system('keytool -list -keystore "%s" -alias "%s" -storepass "%s"' % (keystore, cKeyAlias, cKeyStorePass), False):
        print "Keystore + KeystorePass + KeyAlias do not match"
        return
    
    system('cp "%s" "%s"' % (apkFile, tmpFile), desc="Step 1: Copy APK to tempFile")
    system('zip -d "%s" META-INF/*' % (tmpFile), desc="Step 2: Delete existing signature and manifest from the tmpFile APK")
    system('jarsigner -keystore "%s" -storepass "%s" -keypass "%s" "%s" "%s"' % (keystore, cKeyStorePass, cKeyPass, tmpFile, cKeyAlias), desc="Step 3: Re-sign the tmpFile APK")
    system('jarsigner -verify "%s"' % (tmpFile), desc="Step 4: Verify the signature of the tmpFile APK")
    system('zipalign -f 4 "%s" "%s"' % (tmpFile, tmpFile2), desc="Step 5: ZipAlign the tmpFile APK into tmpFile2")
    system('zipalign -c 4 "%s"' % (tmpFile2), desc="Step 6: Check the zip alignment of the tmpFile2 APK")
    system('mv "%s" "%s"' % (tmpFile2, tmpFile), desc="Step 7: Overwrite tmpFile with tmpFile2 APK")
    system('mv "%s" "%s"' % (tmpFile, outFile), desc="Step 8: Overwrite outFile with tmpFile APK")
    
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