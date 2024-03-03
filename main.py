# Description: This file contains the main function to run the genetic algorithm to solve the 3D truck loading problem
from genetic_algorithm_grouping import *
from visualization import *
from container import *
from package import *
from box3dvisualizer import *

import plotly.graph_objects as go
import os


def main_grouping(json_container, json_delivery):
    data_container = pd.read_json(json_container)
    data_delivery = pd.read_json(json_delivery)
    # excel_file_path = "Sample_data0.xlsx"
    # sheet_container = "Container"
    # sheet_items_d1 = "Ex2-del1"
    # sheet_items_d2 = "Ex2-del2"
    # data_container = read_excel(excel_file_path, sheet_container)
    # data_delivery = read_excel(excel_file_path, sheet_items_d1)
    # Genetic Algorithm Parameters
    POPULATION_SIZE = 100
    NUM_GENERATIONS = 100
    MUTATION_RATE = 0.2

    # draw a ASCII Graphics rectangle as a comment with depth, width, height
    # -------------------------  ---
    # |                       |
    # |                       |  width
    # |                       |
    # -------------------------
    # |<----    depth    ---->|  ---

    # Initialize the container
    container_height = int(data_container["Height"][0])
    container_width = int(data_container["Width"][0])
    container_depth = int(data_container["Length"][0])

    packages, list_of_colors = dataframe_to_package_parser(data_delivery)
    # Run the genetic algorithm
    best_chromosome, best_fitness = genetic_algorithm(
        packages, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE, "3D"
    )
    # Print the best loading order
    print("Best Loading Order:", best_chromosome, "Fitness:", best_fitness)

    # Translate the best chromosome into a list of items to be loaded in the container
    items_to_be_loaded = []
    color_package = []
    for group_id, package_ids in best_chromosome.items():
        for package_idx in package_ids:
            package = packages[package_idx]
            color_package.append(list_of_colors[package_idx])
            items_to_be_loaded.append(
                (
                    package.width,
                    package.height,
                    package.depth,
                )
            )
    # for i, package_idx in enumerate(best_chromosome):
    #    package = packages[package_idx]
    #    color_package.append(list_of_colors[package_idx])
    #    items_to_be_loaded.append((package.width, package.height, package.depth))

    container = PartiallyLoadedContainer(
        2, 2, [0, container_depth], [0, container_width]
    )
    container.height = container_height

    # Load the boxes in the container
    for box in items_to_be_loaded:
        depth, width, height = box
        best_row, best_column, best_score = find_best_position(
            container, depth, width, height
        )
        load_box(container, best_row, best_column, depth, width, height)

    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()

    # Output the lower and upper corners and the index of the boxes loaded in the container
    # print('Boxes loaded in the container:')
    # print('Index, Lower Corner, Upper Corner')
    # for i in range(len(container.boxes)):
    #    print(container.boxes_index[i], container.boxes_lower_corner[i], container.boxes_upper_corner[i])
    #    print(color_package)

    # Make a list of boxes in JSON format
    # Assign same colors to same size boxes
    boxes_json = get_json_for_list_of_boxes(
        container.boxes_index,
        color_package,
        container.boxes,
        container.boxes_lower_corner,
        cdepth=container_depth + 1,
        cwidth=container_width + 1,
        cheight=container_height + 1,
    )
    print(boxes_json)

    # test_draw_box()
    """     
        visualize3Dboxes(
        container.boxes_lower_corner,
        container.boxes,
        container.width,
        container.depth,
        container.height,
        list_of_colors,
    ) """
    return boxes_json


def main():
    # data_container = pd.read_json(json_container)
    # data_delivery = pd.read_json(json_delivery)

    excel_file_path = "Sample_data0.xlsx"
    sheet_container = "Container"
    sheet_items_d1 = "Ex2-del1"
    sheet_items_d2 = "Ex2-del2"
    data_container = read_excel(excel_file_path, sheet_container)
    data_delivery = read_excel(excel_file_path, sheet_items_d1)
    # Genetic Algorithm Parameters
    POPULATION_SIZE = 50
    NUM_GENERATIONS = 100
    MUTATION_RATE = 0.2

    # draw a ASCII Graphics rectangle as a comment with depth, width, height
    # -------------------------  ---
    # |                       |
    # |                       |  width
    # |                       |
    # -------------------------
    # |<----    depth    ---->|  ---

    # Initialize the container
    container_height = int(data_container["Height"][0])
    container_width = int(data_container["Width"][0])
    container_depth = int(data_container["Length"][0])

    packages, list_of_colors = dataframe_to_package_parser(data_delivery)

    # Run the genetic algorithm
    best_chromosome, best_fitness = genetic_algorithm(
        packages, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE, "3D"
    )

    # Print the best loading order
    print("Best Loading Order:", best_chromosome, "Fitness:", best_fitness)

    # Translate the best chromosome into a list of items to be loaded in the container
    items_to_be_loaded = []
    color_package = []
    for i, package_idx in enumerate(best_chromosome):
        package = packages[package_idx]
        color_package.append(list_of_colors[package_idx])
        items_to_be_loaded.append((package.width, package.height, package.depth))

    container = PartiallyLoadedContainer(
        2, 2, [0, container_depth], [0, container_width]
    )
    container.height = container_height

    # Load the boxes in the container
    for box in items_to_be_loaded:
        depth, width, height = box
        best_row, best_column, best_score = find_best_position(
            container, depth, width, height
        )
        load_box(container, best_row, best_column, depth, width, height)

    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()

    # Output the lower and upper corners and the index of the boxes loaded in the container
    # print('Boxes loaded in the container:')
    # print('Index, Lower Corner, Upper Corner')
    # for i in range(len(container.boxes)):
    #    print(container.boxes_index[i], container.boxes_lower_corner[i], container.boxes_upper_corner[i])
    #    print(color_package)

    # Make a list of boxes in JSON format
    # Assign same colors to same size boxes
    boxes_json = get_json_for_list_of_boxes(
        container.boxes_index,
        color_package,
        container.boxes,
        container.boxes_lower_corner,
        cdepth=container_depth + 1,
        cwidth=container_width + 1,
        cheight=container_height + 1,
    )
    # print(boxes_json)

    # test_draw_box()
    """     
        visualize3Dboxes(
        container.boxes_lower_corner,
        container.boxes,
        container.width,
        container.depth,
        container.height,
        list_of_colors,
    ) """
    return boxes_json


def read_excel(excel_file_name, sheet_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the Excel file
    excel_file_path = os.path.join(script_dir, excel_file_name)

    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    return df


def dataframe_to_package_parser(df):
    l0 = df["Length"].to_numpy()
    w0 = df["Width"].to_numpy()
    h0 = df["Height"].to_numpy()
    quantity = df["Quantity"].to_numpy()
    wgt0 = df["Weight"].to_numpy()
    type0 = df["Type"]
    available_colors = [
        "red",
        "green",
        "blue",
        "yellow",
        "purple",
        "white",
        "black",
        "orange",
        "violet",
        "cyan",
        "gray",
        "pink",
        "brown",
        "lime",
        "maroon",
        "olive",
        "navi",
    ]  # up to 17 different colors, more colors can be added

    packages = []
    list_of_colors = []
    item_id = 0

    for i in range(len(l0)):
        # group_packages = []
        # group_colors = []
        for _ in range(quantity[i]):
            packages.append(
                Package(
                    item_id=item_id,
                    width=w0[i],
                    height=l0[i],
                    depth=h0[i],
                    non_stackable=False,
                    group_id=i,
                )
            )
            list_of_colors.append(available_colors[i])
            item_id = item_id + 1
        # packages.append(group_packages)
        # list_of_colors.append(group_colors)

    return packages, list_of_colors


if __name__ == "__main__":
    test_grouping()
