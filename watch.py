#python watch.py ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/Helloworld/

import sys
import time
import logging
import pprint

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class get_all_events(FileSystemEventHandler):

    def on_modified(self, event):
        print "\n\nSE HA MODIFICADO"
        print event.is_directory
        print event.src_path
        return "MODIFICADO"

    def on_created(self, event):
        print "\n\nSE HA CREADO"
        print event.is_directory
        print event.src_path

    def on_deleted(self, event):
        print "\n\nSE HA BORRADO"
        print event.is_directory
        print event.src_path

    def on_moved(self, event):
        print "\n\nSE HA RENOMBRADO"
        print event.is_directory
        print event.src_path


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
