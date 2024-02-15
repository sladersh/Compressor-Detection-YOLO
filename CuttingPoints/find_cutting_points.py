import cv2

class_mapping = {"0": "compressor", "1": "base_plate", "2": "metal_wire"}


def generate_yolo_bbox(file_name):
    yolo_bbox_value = []

    with open(file_name, "r") as file:
        lines = file.readlines()

    for line in lines:
        values = line.strip().split(" ")
        class_label = class_mapping.get(values[0], "unknown")
        bbox = [float(value) for value in values[1:]]
        yolo_bbox_value.append({"class": class_label, "bbox": bbox})

    return yolo_bbox_value


def generate_opencv_bbox(yolo_bbox_value, img_width, img_height):
    opencv_bbox_value = []

    for bbox_value in yolo_bbox_value:
        x, y, w, h = bbox_value["bbox"]

        x_min = int((x - w / 2) * img_width)
        y_min = int((y - h / 2) * img_height)
        x_max = int((x + w / 2) * img_width)
        y_max = int((y + h / 2) * img_height)

        opencv_bbox_value.append(
            {"class": bbox_value["class"], "bbox": [x_min, y_min, x_max, y_max]}
        )

    return opencv_bbox_value


def draw_bbox(img, bbox_value):
    index = 0
    for bbox_val in bbox_value:
        if bbox_val["class"] == "compressor":
            box_colour = (255, 0, 255)
        elif bbox_val["class"] == "base_plate":
            box_colour = (0, 255, 0)
        else:
            box_colour = (255, 0, 0)

        x_min = bbox_val["bbox"][0]
        y_min = bbox_val["bbox"][1]
        x_max = bbox_val["bbox"][2]
        y_max = bbox_val["bbox"][3]

        cv2.rectangle(
            img,
            (x_min, y_min),
            (x_max, y_max),
            box_colour,
            5,
        )

        if bbox_val["class"] == "metal_wire":
            start_point_wire = (x_min, int((y_min + y_max) / 2))
            end_point_wire = (x_max, int((y_min + y_max) / 2))
            cv2.line(img, start_point_wire, end_point_wire, (0, 0, 255), 20)
            index = index + 1
            print(f"Start point of METAL WIRE {index} - {start_point_wire}")
            print(f"End point of METAL WIRE {index} - {end_point_wire}")
            print()
        elif bbox_val["class"] == "base_plate":
            start_point1_plate = (x_min, int(y_min + 200))
            end_point1_plate = (x_max, int(y_min + 200))
            cv2.line(img, start_point1_plate, end_point1_plate, (0, 0, 255), 20)
            print(f"Start point of BASE PLATE TOP - {start_point1_plate}")
            print(f"End point of BASE PLATE TOP - {end_point1_plate}")
            print()
            start_point2_plate = (x_min, int(y_max - 200))
            end_point2_plate = (x_max, int(y_max - 200))
            cv2.line(img, start_point2_plate, end_point2_plate, (0, 0, 255), 20)
            print(f"Start point of BASE PLATE BOTTOM - {start_point2_plate}")
            print(f"End point of BASE PLATE BOTTOM - {end_point2_plate}")
            print()


image = cv2.imread("assets/draw1.jpg")

yolo_bbox = generate_yolo_bbox("assets/bbox1.txt")

opencv_bbox = generate_opencv_bbox(yolo_bbox, image.shape[1], image.shape[0])

print()
draw_bbox(image, opencv_bbox)

cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
cv2.imshow("Output", image)

image_scale_down = 4
h = int((image.shape[0] / image_scale_down))
w = int((image.shape[1] / image_scale_down))

cv2.resizeWindow("Output", w, h)

cv2.waitKey(0)
cv2.destroyAllWindows()
