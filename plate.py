# zapis w szarosci
import sqlite3

from sqlalchemy import create_engine, MetaData, select, text
from sqlalchemy.orm import sessionmaker


import easyocr
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import util
from dbi import create_plates


def search_plate(name_file):
    # define constants
    model_cfg_path = os.path.join('.', 'model', 'cfg', 'darknet-yolov3.cfg')
    model_weights_path = os.path.join('.', 'model', 'weights', 'model.weights')
    class_names_path = os.path.join('.', 'model', 'class.names')

    img_path = "model/new_cars/" + name_file

    # load class names
    with open(class_names_path, 'r') as f:
        class_names = [j[:-1] for j in f.readlines() if len(j) > 2]
        f.close()

    # load model
    net = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)

    # load image

    img = cv2.imread(img_path)

    H, W, _ = img.shape

    # convert image
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True)

    # get detections
    net.setInput(blob)

    detections = util.get_outputs(net)

    # bboxes, class_ids, confidences
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

    # apply nms
    bboxes, class_ids, scores = util.NMS(bboxes, class_ids, scores)

    # plot

    reader = easyocr.Reader(['en'])
    plate = False
    for bbox_, bbox in enumerate(bboxes):
        xc, yc, w, h = bbox

        """cv2.putText(img,
                    class_names[class_ids[bbox_]],
                    (int(xc - (w / 2)), int(yc + (h / 2) - 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    7,
                    (0, 255, 0),
                    15)
        """

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
        #plt.imshow(cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB))
        cv2.imwrite("model/only_plate/" + name_file, license_plate)
        print("saved new plate")
        #plt.show()

    else:
        print("nie ma")


def new_plate(name_file):
    sql_url = "sqlite:///data.db"

    temp = (
        "sss",
        "aaaaaa",
        "Wwwww",
        False,
    )


    plate = "model/only_plate/" + name_file
    reader = easyocr.Reader(['en'])
    aaa = reader.readtext(plate)
    print(aaa)
    print(type(aaa))
    print(len(aaa))
    print(len(aaa[0]))

    for put in aaa:
        engine = create_engine(sql_url)
        session = sessionmaker(engine)
        connection = engine.connect()
        metadata = MetaData()
        conn = sqlite3.connect("data.db")

        one, two, tree = put
        #print(one, two, tree)
        #print("ssssss")
        print(two)
        create_plates(conn, temp)
        print("added new plate in db")

