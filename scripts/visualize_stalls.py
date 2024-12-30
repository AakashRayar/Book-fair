import os
import sys
import django
import cv2
import matplotlib.pyplot as plt

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstall.settings')
django.setup()

# Import models
from book.models import Click

def visualize_stalls():
    # Load image
    image_path = os.path.join(os.path.dirname(__file__), '../book/static/book/images/cbf-layout1.jpg')
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found at", image_path)
        return
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get stalls from the database
    stalls = Click.objects.all()

    # Draw rectangles for each stall
    for stall in stalls:
        x, y, width, height = int(stall.x_coordinate), int(stall.y_coordinate), int(stall.width), int(stall.height)
        print(f"Stall {stall.stall_number} at coordinates: (x = {x}, y = {y})")  # Print stall number and coordinates
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.putText(image, f"Stall {stall.stall_number}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


    # Display the image with stall locations
    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.title("Stall Locations")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    visualize_stalls()
