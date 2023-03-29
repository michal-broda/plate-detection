#


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse

from plate import new_plate, search_plate



class FileCreateHandler(FileSystemEventHandler):
    def on_created(self, event):
        name_file = event.src_path[::-1]
        #print(name_file.find("\\"))
        x = len(name_file) - name_file.find("/")
        name_file = event.src_path[x:]
        print(name_file)

        print("Created: " + event.src_path)
        search_plate(name_file)
        new_plate(name_file)


if __name__ == "__main__":

    event_handler = FileCreateHandler()

    # Create an observer.
    observer = Observer()

    # Attach the observer to the event handler.
    observer.schedule(event_handler, "model/new_cars", recursive=True)

    # Start the observer.
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
