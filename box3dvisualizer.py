import plotly.graph_objects as go
# Define a function to draw a 3D box with shaded faces
def draw_box(x, y, z, dx, dy, dz, base_color):
    """Draw a 3D box with each face having a different shade of the base color."""
    # Define the coordinates for each vertex of the box
    v0, v1, v2, v3, v4, v5, v6, v7 = [
        [x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z],
        [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]
    ]

    # Define the vertices for each face
    faces = [
        [v0, v1, v5, v4],  # Front face
        [v1, v2, v6, v5],  # Right face
        [v2, v3, v7, v6],  # Back face
        [v3, v0, v4, v7],  # Left face
        [v0, v3, v2, v1],  # Bottom face
        [v4, v5, v6, v7]   # Top face
    ]

    # Create a list of Plotly Mesh3d objects, one for each face
    box_faces = []
    for i, face in enumerate(faces):
        # Adjust the shade of the base color for each face
        shade = 0.6 + 0.1 * i
        face_color = f'rgba({int(base_color[0] * shade)}, {int(base_color[1] * shade)}, {int(base_color[2] * shade)}, 1)'
        x_coords, y_coords, z_coords = zip(*face)
        box_faces.append(go.Mesh3d(
            x=x_coords, y=y_coords, z=z_coords,
            i=[0, 1, 2, 3], j=[1, 2, 3, 0], k=[2, 3, 0, 1],
            color=face_color,
            opacity=1  # Opaque faces
        ))

    return box_faces

# Define a function to plot a 3-D box with shaded faces given upper and lower bounds
def draw_interval_box(lbx,lby,lbz,ubx,uby,ubz,base_color):
    """Draw a 3D box with each face having a different shade of the base color."""
    # Use function draw_box to draw the box
    # Define dx, dy, dz
    dx = ubx - lbx
    dy = uby - lby
    dz = ubz - lbz
    # assert that dx, dy, dz are positive
    assert dx >= 0 and dy >= 0 and dz >= 0

    # Call draw_box
    return draw_box(lbx, lby, lbz, dx, dy, dz, base_color)

# draw a small ball (point) at the a coordinate
def draw_point(x, y, z, color):
    """Draw a small ball (point) at the a coordinate."""
    return go.Scatter3d(
        x=[x], y=[y], z=[z],
        mode='markers',
        marker=dict(color=color, size=5)
    )

def draw_anchored_boxes(upper_corners, anchor, base_color,point_color):
    """Draw a list of boxes anchored at a point."""
    # Create a list of boxes anchored at the origin
    anchored_boxes = []
    # Create a box anchored at the origin for each box in upper_corners list
    boxes = []
    for corner in upper_corners:
        boxes.append([anchor[0], anchor[1], anchor[2], corner[0], corner[1], corner[2]])


    # Create a box for each set of upper bounds
    for box in boxes:
        anchored_boxes += draw_interval_box(box[0], box[1], box[2], box[3], box[4], box[5], base_color)

    # Draw a point at the anchor
    anchored_boxes.append(draw_point(anchor[0], anchor[1], anchor[2], point_color))

    # append a point at each upper corner
    for corner in upper_corners:
        anchored_boxes.append(draw_point(corner[0], corner[1], corner[2], point_color))

    return anchored_boxes

def test_draw_anchored_boxes():
    # anchor point
    anchor = [0, 0, 0]
    # upper bounds list
    upper_bounds = [[3, 2, 4], [1, 6, 3], [5, 5, 1], [4, 3, 2]]
    # base color orange
    base_color = (255, 165, 0)
    # point color blue
    point_color = ( 0, 0, 255)
    # draw anchored boxes
    anchored_boxes = draw_anchored_boxes(upper_bounds, anchor, base_color, point_color)

    # Create a figure and add the boxes
    fig = go.Figure(data=anchored_boxes)
    # Set the layout for the 3D plot, add labels f1 f2 f3
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-1, 6], title='f1'),
            yaxis=dict(nticks=4, range=[-1, 6], title='f2'),
            zaxis=dict(nticks=4, range=[-1, 6], title='f3')
        ),
        margin=dict(r=10, l=10, b=10, t=10)
    )
    # Show the plot
    fig.show()


    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-1, 6]),
            yaxis=dict(nticks=4, range=[-1, 6]),
            zaxis=dict(nticks=4, range=[-1, 6])
        ),
        margin=dict(r=10, l=10, b=10, t=10)
    )
    # Show the plot
    fig.show()





# test draw_box
def test_draw_box():
    # Define the size of the boxes
    dx, dy, dz = 1, 1, 1

    # Define the base colors for the boxes
    blue_color = (0, 0, 255)
    green_color = (0, 255, 0)
    orange_color = (255, 165, 0)
    yellow_color = (255, 255, 0)
    pink_color = (255, 192, 203)

    # Create boxes in all colors with shaded faces
    blue_box  = draw_box(0, 0, 0, dx, dy, dz, blue_color)
    green_box = draw_box(0.5, 0.5, 0,dx, dy, dz, green_color)
    orange_box = draw_box(0.1, 0.2, 0, dx, dy, dz, orange_color)
    yellow_box = draw_box(0.0, 0.25, 0,dx,dy, dz, yellow_color)
    pink_box = draw_box(0.0, 0.1, 0, dx, dy, dz, pink_color)


    # make a python list of all the boxes
    all_boxes = blue_box + green_box + orange_box + yellow_box + pink_box


    # Create a figure and add the boxes
    fig = go.Figure(data=all_boxes)
    #

    # Set the layout for the 3D plot
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-1, 10]),
            yaxis=dict(nticks=4, range=[-1, 10]),
            zaxis=dict(nticks=4, range=[-1, 10])
        ),
        margin=dict(r=220, l=220, b=220, t=10)
    )

    # Show the plot
    fig.show()
