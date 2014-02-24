#python watch.py ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Helloworld/
#python ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Helloworld/watchdogFunctions/watch.py ~/Desktop/SAMBA/LOCAL/ttg-svnrepo/trunk/
#sshfs -o IdentityFile=~/.ssh/ssanchez root@dev01.server.egtelecom.es:/mnt/proyecto/proyecto_ssanchez/trunk/ ~/Desktop/SAMBA/REMOTO/ttg-svnrepo/trunk/
#enventos disponibles en FileSystemEventHandler event.is_directory, event.src_path, event.dest_path(<== Solo cuando un archivo ha sido renombrado o movido) 

import sys
import time
import logging
import pprint
import os
import re
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class get_all_events(FileSystemEventHandler):
    def __init__(self):
        self.folderBase = "trunk"
        self.localPath = "~/Desktop/SAMBA/LOCAL/ttg-svnrepo/trunk/"
        self.remotePath = "~/Desktop/SAMBA/REMOTO/ttg-svnrepo/trunk/"


    def ejecutar(self, x):
        time.sleep(2)
        proc = subprocess.Popen(x, 
                                shell = True,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE)


    def split_path_local(self, path):
        match = re.search("(?<=\/" + self.folderBase + "\/).*", path)
        return match.group(0) if match else ""


    def on_modified(self, event):
        if event.is_directory == False: 
            print ">>> SE HA MODIFICADO: " + event.src_path


    def on_created(self, event):
        print ">>> SE HA CREADO: " + event.src_path

        sanitize = self.split_path_local(event.src_path)
        sanitizeLocalPath = self.localPath + sanitize
        sanitizeRemotePath = self.remotePath + sanitize
        
        if event.is_directory == True:
            if os.path.isdir(sanitizeRemotePath) == False:
                cmd = "mkdir -p " + sanitizeRemotePath
        
        elif event.is_directory == False:
            if os.path.exists(sanitizeRemotePath) == False:
                goodPath = self.split_path_local(os.path.dirname(event.src_path))
                cmd = "mkdir -p -m a=rwx '" + self.remotePath + goodPath + "' && cp -p '" + event.src_path + "' " + self.remotePath + goodPath
            
            else:
                cmd = "cp -p '" + event.src_path + "' " + self.remotePath + goodPath

        self.ejecutar(cmd)


    def on_deleted(self, event):
        print ">>> SE HA BORRADO: " + event.src_path


    def on_moved(self, event):
        print ">>> SE HA RENOMBRADO - MOVIDO: " + event.src_path
        print self.split_path_local(event.src_path)

gae = get_all_events()



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
