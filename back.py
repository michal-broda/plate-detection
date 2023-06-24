from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger import logger
import argparse

from plate import new_plate, search_plate


class FileCreateHandler(FileSystemEventHandler):
    """ watchdog for new car image """
    def on_created(self, event):

        dir = str(event.src_path)

        if '.' in dir:
            name_file = event.src_path[::-1]
            x = len(name_file) - name_file.find("/")
            name_file = event.src_path[x:]
            logger.info(f'NEW IMAGE! {name_file}')

            logger.info("Created in: " + event.src_path)
            search_plate(name_file, dir)

        else:
            logger.error("new file is directory !")


if __name__ == "__main__":

    event_handler = FileCreateHandler()

    """ create an observer. """
    observer = Observer()

    """ attach the observer to the event handler. """
    observer.schedule(event_handler, "model/new_cars", recursive=True)

    """ start the observer """
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
