import pandas as pd
import numpy as np
import json
import os

# print in the json format (see example above) a list of boxes, index, size of boxes, lower corners in container (with height)
# to json format; assign random colors to the boxes according to colors list (default is 'red')
def print_json_for_list_of_boxes(
    boxes_indexes,
    colors,
    boxes_sizes,
    boxes_lower_corners,
    cdepth=8000,
    cwidth=3400,
    cheight=2800,
):
    # print in the json format (see example above) a list of boxes, index, size of boxes, lower corners in container (with height)
    # to json format; assign random colors to the boxes according to colors list (default is 'red')
    # transform cdepth, clength, cwidth to strings

    print('{ "container": {')
    print('"size": {')
    print('"width":' + str(cwidth) + ",")
    print('"height":' + str(cheight) + ",")
    print('"depth":' + str(cdepth))
    print("},")
    print('"items": [')
    for i in range(len(boxes_indexes)):
        print("{", end=" ")
        print('"id": "BOX', boxes_indexes[i], '",', end=" ")
        print('"type": "box",', end=" ")
        # Make a string from the color assignment to avoid spaces around the color name; no line breaks
        color_print = '"color": "' + colors[i].strip() + '",'
        print(color_print, end=" ")
        print('"size": {', end=" ")
        print('"width": ', boxes_sizes[i][1], ",", end=" ")
        print('"height": ', boxes_sizes[i][2], ",", end=" ")
        print('"depth": ', boxes_sizes[i][0], end=" ")
        print("},", end=" ")
        print('"position": {', end=" ")
        print('"x": ', boxes_lower_corners[i][0], ",", end=" ")
        print('"y": ', boxes_lower_corners[i][2], ",", end=" ")
        print('"z": ', boxes_lower_corners[i][1], end=" ")
        print("}", end=" ")
        if i < len(boxes_indexes) - 1:
            print("},")
        else:
            print("}")
    print("]", end=" ")
    print("}" + "}")


def get_json_for_list_of_boxes(
    boxes_indexes,
    colors,
    boxes_sizes,
    boxes_lower_corners,
    cdepth=8000,
    cwidth=3400,
    cheight=2800,
):
    result_json = {
        "container": {
            "size": {
                "width": int(cwidth),
                "height": int(cheight),
                "depth": int(cdepth),
            },
            "items": [],
        }
    }

    for i in range(len(boxes_indexes)):
        item = {
            "id": "BOX" + str(int(boxes_indexes[i])),
            "type": "box",
            "color": colors[i].strip(),
            "size": {
                "width": int(boxes_sizes[i][1]),
                "height": int(boxes_sizes[i][2]),
                "depth": int(boxes_sizes[i][0]),
            },
            "position": {
                "x": int(boxes_lower_corners[i][0]),
                "y": int(boxes_lower_corners[i][2]),
                "z": int(boxes_lower_corners[i][1]),
            },
        }
        result_json["container"]["items"].append(item)

    return json.dumps(result_json, separators=(',', ':'))


def read_excel(excel_file_name, sheet_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the Excel file
    excel_file_path = os.path.join(script_dir, excel_file_name)

    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    return df