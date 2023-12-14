import random
import time
import json
from pymongo import MongoClient

annotations = 450_000
framerate = 30
cameras = 10

connection = MongoClient("mongodb://root:example@127.0.0.1:27017/")  # password in docker-compose.yml
db = connection["myDb"]

db.drop_collection("myTable")
db.create_collection("myTable")
collection = db["myTable"]


def get_bounding_box(i):
    annotation = {'timestamp': time.time(),
                  'frameId': i,
                  'camera': random.randint(0, 9),
                  'class': random.randint(0, 5),
                  'confidence': random.randint(0, 100),
                  'x1': random.randint(0, 1910),
                  'y1': random.randint(0, 1070),
                  'x2': random.randint(10, 1910),
                  'y2': random.randint(10, 1070)
                  }
    return annotation


def create_objects_frame_by_frame():  # for each frame create a json that contains all bounding boxes of that frame
    annotations_per_frame = int(annotations / (framerate * cameras))

    annotation_json_list = []
    for camera_number in range(cameras):
        for frame_number in range(framerate):
            frame_annotations = []
            for annotation_number in range(annotations_per_frame):
                frame_annotations.append(get_bounding_box(camera_number * frame_number * annotation_number))

            #annotation_json_list.append(json.dumps(frame_annotations))
            annotation_json_list.append(frame_annotations)

    return annotation_json_list


def create_objects_bb_by_bb():  # store each bounding box in a new entry / row
    annotation_list = []
    for i in range(annotations):
        annotation_list.append(get_bounding_box(i))
    return annotation_list


def insert_objects():

    # Does not work
    """
    print("Frame by frame")
    start_time_frame_by_frame = time.time()
    objects_frame_by_frame = create_objects_frame_by_frame()
    end_time_frame_by_frame = time.time()
    print(f"Creation of {annotations} objects took {end_time_frame_by_frame - start_time_frame_by_frame} seconds")

    start_time_insert_frame_by_frame = time.time()
    collection.insert_many(objects_frame_by_frame)
    end_time_insert_frame_by_frame = time.time()
    insert_frame_by_frame_time = end_time_insert_frame_by_frame - start_time_insert_frame_by_frame
    print(f"Insertion of {annotations} objects took {insert_frame_by_frame_time} seconds")
    print(f"{annotations / insert_frame_by_frame_time} objects per second")
    print("---------------------------------------------------------------")
    """
    print("Bounding box by bounding box")
    start_time_bb_by_bb = time.time()
    objects_bb_by_bb = create_objects_bb_by_bb()
    end_time_bb_by_bb = time.time()
    print(f"Creation of {annotations} objects took {end_time_bb_by_bb - start_time_bb_by_bb} seconds")

    start_time_insert_bb_by_bb = time.time()
    collection.insert_many(objects_bb_by_bb)
    end_time_insert_bb_by_bb = time.time()
    insert_bb_by_bb_time = end_time_insert_bb_by_bb - start_time_insert_bb_by_bb
    print(f"Insertion of {annotations} objects took {insert_bb_by_bb_time} seconds")
    print(f"{int(annotations / insert_bb_by_bb_time)} objects per second")
    print("---------------------------------------------------------------")


print("MongoDB")
insert_objects()
