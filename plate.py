import logging
import sqlite3
import datetime
from logger import logger

from sqlalchemy import create_engine, MetaData, select, text
from sqlalchemy.orm import sessionmaker

import easyocr
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import util
from dbi import create_plates


def search_plate(name_file, dir):

    """ search only plate in new car image """
    model_cfg_path = os.path.join('.', 'model', 'cfg', 'darknet-yolov3.cfg')
    model_weights_path = os.path.join('.', 'model', 'weights', 'model.weights')
    class_names_path = os.path.join('.', 'model', 'class.names')

    img_path = dir

    """ load class names """
    with open(class_names_path, 'r') as f:
        class_names = [j[:-1] for j in f.readlines() if len(j) > 2]
        f.close()

    """ load model """
    net = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)

    """ load image """
    croop_image = cv2.imread(img_path)
    img = croop_image[600:1000, 800:1600]

    #cv2.imwrite("model/gfg.jpg", img)

    H, W, _ = img.shape

    """ convert image """
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True)

    """ get detections """
    net.setInput(blob)

    detections = util.get_outputs(net)

    """ bboxes, class_ids, confidences """
    bboxes = []
    class_ids = []
    scores = []

    for detection in detections:
        # [x1, x2, x3, x4, x5, x6, ..., x85]
        bbox = detection[:4]

        xc, yc, w, h = bbox
        bbox = [int(xc * W), int(yc * H), int(w * W), int(h * H)]

        bbox_confidence = detection[4]

        class_id = np.argmax(detection[5:])
        score = np.amax(detection[5:])

        bboxes.append(bbox)
        class_ids.append(class_id)
        scores.append(score)

    """ apply nms """
    bboxes, class_ids, scores = util.NMS(bboxes, class_ids, scores)

    """ plot """

    reader = easyocr.Reader(['en'])
    plate = False
    for bbox_, bbox in enumerate(bboxes):
        xc, yc, w, h = bbox

        plate = True
        license_plate = img[int(yc - (h / 2)):int(yc + (h / 2)), int(xc - (w / 2)):int(xc + (w / 2)), :].copy()

        img = cv2.rectangle(img,
                            (int(xc - (w / 2)), int(yc - (h / 2))),
                            (int(xc + (w / 2)), int(yc + (h / 2))),
                            (0, 255, 0),
                            10)

        # output = reader.readtext(license_plate)
        # print(output)

    #plt.figure()
    #plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    #plt.figure()

    if plate == True:

        license_plate = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
        license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)

        cv2.imwrite("model/only_plate/" + name_file, license_plate)
        cv2.imwrite("static/" + name_file, license_plate)
        logger.info("saved new plate")

        #plt.show()

        new_plate(name_file)

    else:
        logger.error("It's not car or something wrong...")
        logger.info("I'm waiting for next image...")


def new_plate(name_file):

    """ saved text plate in db """
    sql_url = "sqlite:///data.db"

    temp = [
        datetime.datetime.now().strftime("%Y-%m-%d"),
        datetime.datetime.now().strftime("%H:%M:%S"),
        "KR1234",
        '<img src="static/'+name_file+'"',
    ]

    plate = "model/only_plate/" + name_file
    reader = easyocr.Reader(['en'])
    aaa = reader.readtext(plate)

    logger.info("Quantity text = ", len(aaa))

    for put in aaa:
        engine = create_engine(sql_url)
        session = sessionmaker(engine)
        connection = engine.connect()
        metadata = MetaData()
        conn = sqlite3.connect("data.db")

        one, two, tree = put

        logger.info("Name plate is: ", two)

        temp[2] = two

        create_plates(conn, temp)