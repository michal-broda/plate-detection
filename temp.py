import logging

from logger import logger

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

logging.info("aaaaa")
