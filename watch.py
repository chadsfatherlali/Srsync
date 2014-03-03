# -*- coding: utf-8 -*-
#python watch.py ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Helloworld/
#python ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Helloworld/watchdogFunctions/watch.py ~/Desktop/SAMBA/LOCAL/ttg-svnrepo/trunk/
#python watch.py 
#enventos disponibles en FileSystemEventHandler event.is_directory, event.src_path, event.dest_path(<== Solo cuando un archivo ha sido renombrado o movido) 
#python /Users/ssanchez/Desktop/srsync/Srsync/watch.py /Users/ssanchez/Desktop/LOCAL/trunk/

import sys
import time
import logging
import pprint
import os
import re
import subprocess
import shutil
import time
import getpass

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class get_all_events(FileSystemEventHandler):
    def __init__(self):
        self.folderBase = "trunk"
        self.localPath = "/Users/ssanchez/Desktop/LOCAL/trunk/"
        self.remotePath = "/Users/ssanchez/Desktop/SAMBA/trunk/"
        self.user = getpass.getuser().upper()

        print "\n\n>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<"
        print ">>> BIENVENIDO " + self.user + " !! XD"
        print ">>> SRSYNC: Telecoming Group 2014."
        print ">>> Dpto. de diseño."
        print ">>> Version: 1.0."
        print ">>> E-mail: graficottg@telecoming.com."        
        print ">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<"
        print ">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<\n\n\n"


    def split_path_local(self, path):
        match = re.search("(?<=\/" + self.folderBase + "\/).*", path)
        return match.group(0) if match else ""


    def on_modified(self, event):
        if event.is_directory == False: 
            print "\n>>> " + self.user + " SE HA MODIFICADO: " + event.src_path
            print ">>> " + time.ctime()


    def on_created(self, event):
        print "\n>>> " + self.user + " SE HA CREADO: " + event.src_path
        print ">>> " + time.ctime()

        sanitize = self.split_path_local(event.src_path)
        sanitizeLocalPath = self.localPath + sanitize
        sanitizeRemotePath = self.remotePath + sanitize
        
        if event.is_directory == True:
            if os.path.isdir(sanitizeRemotePath) == False:
                operacion = os.makedirs(sanitizeRemotePath, 0777)
        
        elif event.is_directory == False:
            if os.path.exists(sanitizeRemotePath) == False:
                goodPath = self.split_path_local(os.path.dirname(event.src_path))
                
                if(os.path.isdir(self.localPath + goodPath) == True) and (os.path.isdir(self.remotePath + goodPath) == False):
                    operacion = os.makedirs(self.remotePath + goodPath, 0777)

                operacion = shutil.copyfile(sanitizeLocalPath, sanitizeRemotePath)


    def on_deleted(self, event):
        print "\n>>> " + self.user + " SE HA BORRADO: " + event.src_path
        print ">>> " + time.ctime()


    def on_moved(self, event):
        print "\n>>> " + self.user + " SE HA RENOMBRADO - MOVIDO: " + event.src_path
        print ">>> " + time.ctime()
        print self.split_path_local(event.src_path)



if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    event_handler = get_all_events()
    observer = Observer()
    observer.schedule(
                    event_handler, 
                    path, 
                    recursive = True)
    
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
