import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse
import json
from box3dvisualizer import *
import plotly


# print in the json format (see example above) a list of boxes, index, size of boxes, lower corners in container (with height)
# to json format; assign random colors to the boxes according to colors list (default is 'red')
def print_json_for_list_of_boxes(boxes_indexes, colors, boxes_sizes, boxes_lower_corners,cdepth=8000, cwidth=3400, cheight=2800):
# print in the json format (see example above) a list of boxes, index, size of boxes, lower corners in container (with height)
# to json format; assign random colors to the boxes according to colors list (default is 'red')
# transform cdepth, clength, cwidth to strings

    print('{ "container": {')
    print('"size": {')
    print('"width":' + str(cwidth) + ',')
    print('"height":' + str(cheight) + ',')
    print('"depth":' + str(cdepth))
    print('},')
    print('"items": [')
    for i in range(len(boxes_indexes)):
        print('{', end=" ")
        print('"id": "BOX', boxes_indexes[i], '",',  end=" ")
        print('"type": "box",', end=" ")
        # Make a string from the color assignment to avoid spaces around the color name; no line breaks
        color_print = '"color": "' + colors[i].strip() + '",'
        print(color_print, end=" ")
        print('"size": {', end=" ")
        print('"width": ', boxes_sizes[i][1], ',', end=" ")
        print('"height": ', boxes_sizes[i][2], ',', end=" ")
        print('"depth": ', boxes_sizes[i][0], end=" ")
        print('},', end=" ")
        print('"position": {', end=" ")
        print('"x": ', boxes_lower_corners[i][0], ',', end=" ")
        print('"y": ', boxes_lower_corners[i][2], ',', end=" ")
        print('"z": ', boxes_lower_corners[i][1], end=" ")
        print('}', end=" ")
        if (i < len(boxes_indexes)-1):
            print('},')
        else:
            print('}')
    print(']', end=" ")
    print('}'+ '}')

def visualize3Dboxes(boxes_lower_corners, boxes_sizes,
                     container_width, container_depth, container_height, colors=None):
    # # Define the size of the boxes
    # dx, dy, dz = 1, 1, 1
    #
    # # Define the base colors for the boxes
    blue_color = (0, 0, 255)
    green_color = (0, 255, 0)
    orange_color = (255, 165, 0)
    yellow_color = (255, 255, 0)
    pink_color = (255, 192, 203)

    # make a list of colors from the above
    colors = [blue_color, green_color, orange_color, yellow_color, pink_color]

    # make a function that selects a color from the list of colors based on the index of the box modulo the number of
    # colors
    # draw boxes using the function draw_box from box3dvisualizer in the argument at positions box_lower_corners '
    # and with sizes box_sizes
    # make a list of boxes
    all_boxes = []
    if colors is None:
        for i in range(len(boxes_lower_corners)):
            all_boxes = all_boxes + draw_box(boxes_lower_corners[i][1], boxes_lower_corners[i][0], boxes_lower_corners[i][2],
                                boxes_sizes[i][0], boxes_sizes[i][1], boxes_sizes[i][2], colors[i % len(colors)])
    else:
        for i in range(len(boxes_lower_corners)):
            all_boxes = all_boxes + draw_box(boxes_lower_corners[i][1], boxes_lower_corners[i][0], boxes_lower_corners[i][2],
                                boxes_sizes[i][0], boxes_sizes[i][1], boxes_sizes[i][2], colors[i % len(colors)])

    # Create a figure and add the boxes
    fig = go.Figure(data=all_boxes)

    # Set the layout for the 3D plot
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='width',range=[-1, container_depth]),
            yaxis=dict(title='depth',range=[-1, container_width]),
            zaxis=dict(title='height',range=[-1, container_height]),
        ),
        margin=dict(l=10, r=10, b=10, t=10)
    )
    # Show the plot
    fig.show()


    #
    #
    #
    # blue_box = draw_box(0, 0, 0, dx, dy, dz, blue_color)
    # green_box = draw_box(0.5, 0.5, 0, 0.5, 0.5, 1.5, orange_color)
    # orange_box = draw_box(0.1, 0.2, 0, 0.9, 0.8, 1.25, yellow_color)
    # yellow_box = draw_box(0.0, 0.25, 0, 1, 0.75, 1.35, pink_color)
    # pink_box = draw_box(0.25, 0.1, 0, 0.75, 0.9, 1.25, green_color)
    #
    # # make a python list of all the boxes
    # all_boxes = blue_box + green_box + orange_box + yellow_box + pink_box
    #
    # # Create a figure and add the boxes
    # fig = go.Figure(data=all_boxes)
    #
    # # Set the layout for the 3D plot
    # fig.update_layout(
    #     scene=dict(
    #         xaxis=dict(nticks=4, range=[0, container_width]),
    #         yaxis=dict(nticks=4, range=[0, container_depth]),
    #         zaxis=dict(nticks=4, range=[0, container_height])
    #     ),
    #     margin=dict(r=10, l=10, b=10, t=10)
    # )
    #
    # # Show the plot
    # fig.show()

