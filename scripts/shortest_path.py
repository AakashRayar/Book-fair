import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import cv2
import sys
import os
import django
import numpy as np
from PIL import Image
import io
import matplotlib
matplotlib.use('Agg')


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstall.settings')
django.setup()
from book.models import Click

def load_data(stalls_path, blank_spaces_path):
    stalls = pd.read_excel(stalls_path, sheet_name="Box Information")
    blank_spaces = pd.read_excel(blank_spaces_path, sheet_name="New Rectangles")

    # Ensure required columns exist
    required_columns = ['X', 'Y', 'Width', 'Height']
    for col in required_columns:
        if col not in stalls.columns or col not in blank_spaces.columns:
            raise KeyError(f"Missing required column: {col}")

    # Compute stall rectangles
    for df in [stalls, blank_spaces]:
        df['x_min'] = df['X']
        df['y_min'] = df['Y']
        df['x_max'] = df['X'] + df['Width']
        df['y_max'] = df['Y'] + df['Height']

        # Compute center coordinates
        df['center_x'] = (df['x_min'] + df['x_max']) / 2
        df['center_y'] = (df['y_min'] + df['y_max']) / 2

    return stalls, blank_spaces



def build_graph(blank_spaces):
    G = nx.Graph()

    # Use the center points of blank spaces as nodes
    for _, row in blank_spaces.iterrows():
        center_x = (row['x_min'] + row['x_max']) / 2
        center_y = (row['y_min'] + row['y_max']) / 2
        G.add_node((center_x, center_y))

    # Add edges between neighboring blank spaces
    threshold = 80  # Max distance to connect nodes
    nodes = list(G.nodes)
    for i, node1 in enumerate(nodes):
        for node2 in nodes[i + 1:]:
            dist = ((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2) ** 0.5
            if dist <= threshold:
                G.add_edge(node1, node2, weight=dist)

    return G

def find_nearest_node(graph, x, y):
    # Find the nearest graph node to the given coordinates
    nearest_node = None
    min_dist = float('inf')
    for node in graph.nodes:
        dist = ((node[0] - x) ** 2 + (node[1] - y) ** 2) ** 0.5
        if dist < min_dist:
            nearest_node = node
            min_dist = dist
    return nearest_node

def draw_stalls_on_image(layout_image_path, stalls_queryset):
    # Load the layout image
    image = cv2.imread(layout_image_path)

    # Check if the image is loaded properly
    if image is None:
        raise FileNotFoundError(f"Image not found at {layout_image_path}")

    # Iterate through stalls QuerySet (labels can be added later if needed)
    for stall in stalls_queryset:
        # Ensure all necessary attributes are present
        required_attributes = ['x_coordinate', 'y_coordinate', 'width', 'height', 'stall_number']
        if not all(hasattr(stall, attr) for attr in required_attributes):
            raise ValueError(f"Stall object is missing one or more required attributes: {required_attributes}")

        # Compute rectangle coordinates
        x_min = int(stall.x_coordinate)
        y_min = int(stall.y_coordinate)
        x_max = int(stall.x_coordinate + stall.width)
        y_max = int(stall.y_coordinate + stall.height)
        stall_number = stall.stall_number

        # Remove the black border by not drawing rectangles
        # Optionally, you can still label the stalls if required:
        # cv2.putText(
        #     image,
        #     f"Stall {stall_number}",
        #     (x_min, y_min - 10),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.5,
        #     (255, 0, 0),
        #     2
        # )

    # Convert the image from BGR to RGB for matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image_rgb







def plot_path(graph, stalls, blank_spaces, start_stall, end_stall, path, layout_image_path, output_image_path):
    import matplotlib.pyplot as plt
    import io
    from PIL import Image

    stalls_queryset = Click.objects.all()
    img = draw_stalls_on_image(layout_image_path, stalls_queryset)
    plt.figure(figsize=(16, 12), dpi=150)
    plt.imshow(img)

    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_x, path_y, color="blue", linewidth=3)

        # Get coordinates of the start and end stalls
        start_row = stalls.loc[stalls['Name (stall_number)'] == start_stall]
        end_row = stalls.loc[stalls['Name (stall_number)'] == end_stall]
        start_x, start_y = start_row['center_x'].values[0], start_row['center_y'].values[0]
        end_x, end_y = end_row['center_x'].values[0], end_row['center_y'].values[0]

        # Calculate adjusted positions for arrows to touch the blue line and stall box
        arrow_offset = 5  # Offset from the stall box to avoid overlapping numbers
        start_arrow_x = path_x[0] + (start_x - path_x[0]) * 0.8
        start_arrow_y = path_y[0] + (start_y - path_y[0]) * 0.8
        end_arrow_x = path_x[-1] + (end_x - path_x[-1]) * 0.8
        end_arrow_y = path_y[-1] + (end_y - path_y[-1]) * 0.8

        # Draw arrows
        plt.annotate(
            "",
            xy=(start_arrow_x, start_arrow_y),  # Arrowhead near the stall box
            xytext=(path_x[0], path_y[0]),  # Arrow tail on the blue line
            arrowprops=dict(arrowstyle="->", color="blue", lw=2),
        )
        plt.annotate(
            "",
            xy=(end_arrow_x, end_arrow_y),  # Arrowhead near the stall box
            xytext=(path_x[-1], path_y[-1]),  # Arrow tail on the blue line
            arrowprops=dict(arrowstyle="->", color="blue", lw=2),
        )

    plt.axis("off")

    # Save figure to an in-memory buffer as PNG
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    plt.close()

    # Convert PNG buffer to JPEG with PIL for optimization
    buf.seek(0)
    image = Image.open(buf)
    image = image.convert("RGB")  # Ensure it's in RGB mode for JPEG
    image.save(output_image_path, format="JPEG", quality=70)  # Save optimized JPEG
    buf.close()









# # Main function
# def main():
#     stalls_path = r'D:\Project-3\bookstall\book\Books_stall.xlsx'
#     blank_spaces_path = r"D:\Project-3\bookstall\book\new_Books_stall.xlsx"
#     layout_image_path = r"D:\Project-3\bookstall\book\static\book\images\CBF2024-layout1.jpg"  # Path to the layout image

#     stalls, blank_spaces = load_data(stalls_path, blank_spaces_path)

#     # Compute the center coordinates for stalls
#     stalls['center_x'] = (stalls['x_min'] + stalls['x_max']) / 2
#     stalls['center_y'] = (stalls['y_min'] + stalls['y_max']) / 2

#     print("Stalls DataFrame:\n", stalls.head())

#     # Normalize stall names
#     stalls['Name (stall_number)'] = stalls['Name (stall_number)'].astype(str).str.strip()

#     # print("Available stalls:", stalls['Name (stall_number)'].unique())  # Debugging: Show all stall names

#     graph = build_graph(blank_spaces)

#     # Let the user select start and end stalls
#     start_stall = input("Enter the start stall number: ").strip()  # Keep as string
#     end_stall = input("Enter the end stall number: ").strip()  # Keep as string

#     # Get the nearest nodes in the graph for the selected stalls
#     start_row = stalls.loc[stalls['Name (stall_number)'] == start_stall]
#     end_row = stalls.loc[stalls['Name (stall_number)'] == end_stall]

#     if start_row.empty or end_row.empty:
#         if start_row.empty:
#             print(f"Error: Start stall '{start_stall}' not found.")
#         if end_row.empty:
#             print(f"Error: End stall '{end_stall}' not found.")
#         return

#     start_node = find_nearest_node(graph, start_row['center_x'].values[0], start_row['center_y'].values[0])
#     end_node = find_nearest_node(graph, end_row['center_x'].values[0], end_row['center_y'].values[0])

#     # Find the shortest path
#     try:
#         path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')
#     except nx.NetworkXNoPath:
#         print("Error: No path found between the selected stalls.")
#         return

#     # Plot the result on the layout image
#     plot_path(graph, stalls, blank_spaces, start_stall, end_stall, path, layout_image_path)

# # Run the main function
# if __name__ == "__main__":
#     main()
