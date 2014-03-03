# -*- coding: utf-8 -*-
#python watch.py ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Helloworld/
#python ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Helloworld/watchdogFunctions/watch.py ~/Desktop/SAMBA/LOCAL/ttg-svnrepo/trunk/
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

        print "\n\n>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<"
        print ">>> SRSYNC: Telecoming Group 2014."
        print ">>> Dpto. de diseño."
        print ">>> Version: 1.0."
        print ">>> E-mail: graficottg@telecoming.com."
        print ">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<"
        print ">>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<\n\n\n"


    def ejecutar(self, x):
        proc = subprocess.Popen(x, 
                                shell = True,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE)


    def split_path_local(self, path):
        match = re.search("(?<=\/" + self.folderBase + "\/).*", path)
        return match.group(0) if match else ""


    def replace_ws(self, string):
        result = string.replace(" ", "\ ")
        return result 


    def on_modified(self, event):
        if event.is_directory == False: 
            print ">>> SE HA MODIFICADO: " + event.src_path


    def on_created(self, event):
        print ">>> SE HA CREADO: " + event.src_path

        cmd = ""

        sanitize = self.split_path_local(event.src_path)
        sanitizeLocalPath = self.localPath + sanitize
        sanitizeRemotePath = self.remotePath + sanitize
        
        if event.is_directory == True:
            #if os.path.isdir(sanitizeRemotePath) == False:
            cmd = "mkdir -p -m 777 " + self.replace_ws(sanitizeRemotePath)
        
        elif event.is_directory == False:
            # if os.path.exists(self.replace_ws(sanitizeRemotePath)) == False:
            #     goodPath = self.split_path_local(os.path.dirname(event.src_path))
            #     cmd = "mkdir -p -m 777 " + self.replace_ws(self.remotePath + goodPath) + " && cp -p " + self.replace_ws(event.src_path) + " " + self.replace_ws(self.remotePath + goodPath)
            
            # else:
            goodPath = self.split_path_local(os.path.dirname(event.src_path))
            cmd = "cp -prf " + self.replace_ws(event.src_path) + " " + self.replace_ws(self.remotePath + goodPath)

        self.ejecutar(cmd)


    def on_deleted(self, event):
        print ">>> SE HA BORRADO: " + event.src_path


    def on_moved(self, event):
        print ">>> SE HA RENOMBRADO - MOVIDO: " + event.src_path
        print ">>> DESTINO " + event.dest_path
        
        cmd = ""

        sanitizeRemove = self.split_path_local(event.src_path)
        sanitizeLocalPathRemove = self.localPath + sanitizeRemove
        sanitizeRemotePathRemove = self.remotePath + sanitizeRemove

        sanitizeNew = self.split_path_local(event.dest_path)
        sanitizeLocalPathNew = self.localPath + sanitizeNew
        sanitizeRemotePathNew = self.remotePath + sanitizeNew

        if event.is_directory == True:
            print 1
            # print sanitizeRemotePathRemove
            # print sanitizeRemotePathNew
            if os.path.isdir(self.replace_ws(sanitizeRemotePathRemove)) == True:
                cmd = "rm -fdr" + self.replace_ws(sanitizeRemotePathRemove) + " && mkdir -p -m 777 " + self.replace_ws(sanitizeRemotePathNew)

        elif event.is_directory == False:
            print 2
            print sanitizeRemotePathRemove
            print event.dest_path
            print sanitizeRemotePathNew
            print os.path.exists(sanitizeRemotePathRemove)
            if os.path.exists(self.replace_ws(sanitizeRemotePathRemove)) == True:
                print 3
                goodPath = self.split_path_local(os.path.dirname(event.dest_path))
                cmd = "rm " + self.replace_ws(sanitizeRemotePathRemove) + " && cp -p " + self.replace_ws(event.dest_path) + " " + self.replace_ws(sanitizeRemotePathNew)
        
        print cmd

#gae = get_all_events()



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
