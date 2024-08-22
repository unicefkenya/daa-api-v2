#!python
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the command you want to execute
command = "python3 manage.py process_tasks"

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'Change detected in {event.src_path}. Reloading...')
        subprocess.run(command, shell=True)

def main(): 
    path = "."  # Replace with the path to your project directory
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()

