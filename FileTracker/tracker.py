import os
from os import stat
import time
from spinner import Spinner
import sys
import signal
import win32api as win

class UserFile(object):
    """Class to model file data like last modified date and size"""

    def __init__(self, name, size, lmd):
        self.size = size
        self.name = name
        self.lmd = lmd
        self.exists = True

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return "Name: "+self.name+" Size: "+str(self.size) + " LMD: "+str(self.lmd)+" Exists: " + str(self.exists)+"\n"

    def isModified(self, other):
        return self.lmd != other.lmd or self.size != other.size

if(__name__ == "__main__"):
    print("-"*100)
    UserFiles = []
    filelist = os.listdir()
    for file in filelist:
        name = file
        size = stat(file).st_size
        lmd = stat(file).st_mtime
        print("Name: "+file+" Size: "+str(size) +
              " Last Modified Date: "+str(lmd))
        UserFiles.append(UserFile(name, size, lmd))
    spinner = Spinner()
    
    def signal_handler(signal,frame):
        spinner.stop()
        print("\rExiting...    ")
        sys.exit(0)
    
    spinner.start()
    source=['tracker.py','spinner.py','a.txt']
    sourceMod = False
    signal.signal(signal.SIGINT, signal_handler)
    while (1):
        for u in UserFiles:
            if(not u.exists):
                print("\r"+u.name+" was removed.")
                UserFiles.remove(u)
            else:
                # print(str(u))
                u.exists = False
        # print("-"*100)

        time.sleep(1)
        filelist = os.listdir()
        for file in filelist:
            name = file
            size = stat(file).st_size
            lmd = stat(file).st_mtime
            f = UserFile(name, size, lmd)
            if(UserFiles.count(f) == 0):
                print("\rNew File Added")
                print("File: "+f.name)
                UserFiles.append(f)
            else:
                f2 = UserFiles[UserFiles.index(f)]
                if(f2.isModified(f)):
                    print("\rFile: "+f.name+" is modified.")
                    if win.MessageBox(None,"File: "+f.name+" is modified. Backup?","File Change Alert",1) == 1:
                        print("Backing Up File.")
                    UserFiles.remove(f2)
                    UserFiles.append(f)
                    sourceMod=f.name in source
                else:
                    f2.exists = True
        if sourceMod:
            print("\rSource file modified restart tracker...")
            win.MessageBox(0,"Source File Modified","Terminated",0x00001000)
            spinner.stop()
            break
    spinner.stop()
