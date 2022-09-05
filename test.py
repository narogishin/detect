import cv2
import numpy as np

# salihi.lyazid@gmail.com
# nadiaoukrich@gmail.com

def detection(a, b, i):
    yolo = cv2.dnn.readNet(a, b)

    with open('detect/coco.names', 'r') as f:
        classes = f.read().splitlines()

    image = cv2.imread(i)
    blob = cv2.dnn.blobFromImage(image, 1/255, (320, 320), (0,0,0), swapRB = True, crop = False)
    i = blob[0].reshape(320,320,3)
    width = 320
    height = 320
    yolo.setInput(blob)
    output_layer_name = yolo.getUnconnectedOutLayersNames()
    layeroutput = yolo.forward(output_layer_name)
    boxes = []
    confidences = []
    class_ids = []
    for output in layeroutput:
        for detection in output:
            score = detection[5:]
            class_id = np.argmax(score)
            confidence = score[class_id]
            if confidence > 0.7:
                center_x = int(detection[0]*width)
                center_y = int(detection[0]*height)
                w = int(detection[0]*width)
                h = int(detection[0]*height)

                x = int(center_x -w/2)
                y = int(center_y -h/2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    alpha = []
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    if indexes == ():
        return []
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size = (len(boxes), 3))

    for i in indexes.flatten():
        x,y,w,h = boxes[i]
        label = str(classes[class_ids[i]])
        confi = str(round(confidences[i], 2))
        color = colors[i]

        cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)
        cv2.putText(image, label + " " +confi, (x, y+20), font, 2, (255, 255, 255), 2)
        alpha.append(label)
    return alpha
