# TODO: requirements.txt
# TODO: influx in compose
import random
import time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS, WriteOptions

print("InfluxDB")
annotations = 450_000

url = "http://127.0.0.1:8086"
org = "PSE"
token = "5s0f7oPs0F_1AlOMqBn5--SPjSI_qfD9jjPwAP4sXV3oZdTIUgM9a7DNr2uN98Mrgvb_w-LYQC1S5NrHRxqn6A==" # TODO: Change
bucket = "annotations"
client = InfluxDBClient(url=url, token=token, org=org)

write_api = client.write_api(SYNCHRONOUS)

points = []
timestamp = int(time.time()*1000.0) * 2

for frame in range(annotations):
    timestamp += 33
    point = (
        Point("annotations")
        .tag("cameraID", random.randint(0, 9))
        .tag("frameSpecificBoundingBoxID", random.randint(0, 1500))
        .field("iterationHash", "29c4d3b40280ae810fb4a81681e4417b")
        .field("frameID", frame)
        .field("x_1", random.randint(0, 1910))
        .field("y_1", random.randint(0, 1070))
        .field("x_2", random.randint(10, 1910))
        .field("y_2", random.randint(10, 1070))
    )
    points.append(point)

start_time = time.time()
try:
    write_api.write(bucket=bucket, org=org, record=points)
except Exception as e:
    print(e)

end_time = time.time()
insert_time = end_time - start_time

print(f"Insertion of {annotations} objects took {insert_time} seconds")
print(f"{int(annotations / insert_time)} objects per second")
print("---------------------------------------------------------------")
