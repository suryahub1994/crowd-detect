import cv2
import math
import random
from b_box import Box
from ultralytics import YOLO
from algo_factory import *

model = YOLO("yolov8m.pt")

VIDEO_PATH = "data/PeopleBusy.mp4"
OUTPUT_PATH = "output/crowd_result.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("❌ Error: Cannot open video file.")
    exit()
else:
    print("✅ Video opened successfully!")


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
out = cv2.VideoWriter(
    OUTPUT_PATH,
    cv2.VideoWriter_fourcc(*'mp4v'),
    fps if fps > 0 else 25.0,
    (frame_width, frame_height)
)
print(f"🎥 Output video will be saved to: {OUTPUT_PATH}")
count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame, conf=0.10)
    heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)
    if count == 0:
        heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)
    else:
        heatmap *= 0.9
    list_of_boxes = []
    for x1, y1, x2, y2 in results[0].boxes.xyxy:
        centroid_x = int((x1 + x2) / 2)
        centroid_y = int((y1 + y2) / 2)
        bbox = Box(int(x1), int(y1), int(x2), int(y2), centroid_x, centroid_y, 0)
        list_of_boxes.append(bbox)
    centroid_algorithm = getcentroidalgorithm()
    centroid_and_boxes_list = centroid_algorithm.getcentroids(list_of_boxes)
    centroid_aggregator = {}
    for i in range(NO_OF_CLUSTERS):
        centroid_aggregator[i] = {"min_x": 5000, "min_y": 5000, "max_x": -5000, "max_y": -5000 , "centroid_x": -1, "centroid_y":-1, "count": 0, "label":i}
    for bbox in centroid_and_boxes_list:
        centroid_aggregator[bbox.centroid_class]["count"]+=1
        centroid_aggregator[bbox.centroid_class]["min_x"] =  min(centroid_aggregator[bbox.centroid_class]["min_x"], bbox.x_left_top)
        centroid_aggregator[bbox.centroid_class]["min_y"] =  min(centroid_aggregator[bbox.centroid_class]["min_y"], bbox.y_left_top)
        centroid_aggregator[bbox.centroid_class]["max_x"] = max(centroid_aggregator[bbox.centroid_class]["max_x"], bbox.x_right_bottom)
        centroid_aggregator[bbox.centroid_class]["max_y"] = max(centroid_aggregator[bbox.centroid_class]["max_y"], bbox.y_right_bottom)
        centroid_aggregator[bbox.centroid_class]["centroid_x"] = bbox.x_centroid
        centroid_aggregator[bbox.centroid_class]["centroid_y"] = bbox.y_centroid
    for label, values in centroid_aggregator.items():
        xlefttop = int(values["min_x"])
        ylefttop = int(values["min_y"])
        xrightbottom = int(values["max_x"])
        yrightbottom = int(values["max_y"])
        print(f'{xlefttop}, {ylefttop} ,{xrightbottom}, {yrightbottom}')
        x_centroid = int(values["centroid_x"])
        y_centroid = int(values["centroid_y"])
        radius_x = max(x_centroid - xlefttop, xrightbottom -x_centroid)
        radius_y = max(y_centroid - ylefttop, yrightbottom -y_centroid)
        radius = max(radius_x, radius_y)
        radius = int(radius)
        intensity = min(1.0, values["count"] / 10.0)
        cv2.circle(heatmap, (x_centroid, y_centroid), radius, intensity, -1)
    heatmap = cv2.GaussianBlur(heatmap, (91, 91), 0)
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    colored = cv2.applyColorMap((heatmap).astype(np.uint8), cv2.COLORMAP_TURBO)
    overlay = cv2.addWeighted(frame, 0.5, colored, 0.5, 0)
    #cv2.imwrite(f"dump/{count}.jpg", overlay)
    out.write(overlay)
    count += 1

cap.release()
out.release()
cv2.destroyAllWindows()

print(f" Processing complete. Saved {count} frames to video: {OUTPUT_PATH}")
