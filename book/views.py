from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Click
from django.views.decorators.csrf import csrf_exempt
import networkx as nx
from PIL import Image
from django.views.decorators.cache import cache_control
from datetime import datetime
import os
import cv2
from scripts.shortest_path import(find_nearest_node,load_data,build_graph,plot_path,draw_stalls_on_image)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated


def stall_details(request):
    """
    Display the main image and clickable areas.
    """
    stalls = Click.objects.all()  # Retrieve all stalls from the Click model
    return render(request, 'book/stall_details.html', {
        'stalls': stalls,
        'image_path': '/static/book/images/cbf-layout1.jpg'  # Ensure this path is correct
    })

def get_stall_details(request, stall_id):
    """
    Fetch specific stall details along with events.
    """
    stall = get_object_or_404(Click, id=stall_id)  # Fetch stall by ID or return 404 if not found

    events = stall.events if stall.events else "No events available"  # Default message if no events

    # Log for debugging
    print(f"Events for stall {stall_id}: {events}")

    return JsonResponse({
        "stall_number": stall.stall_number,
        "description": stall.description,
        "coordinates": {
            "x": stall.x_coordinate,
            "y": stall.y_coordinate,
            "width": stall.width,
            "height": stall.height,
        },
        "events": events  # Return the events or a default message
    })

def index(request):
    cities = [
        {"name": "Mumbai", "image": "mumbai.png"},
        {"name": "Delhi", "image": "ncr.png"},
        {"name": "Bangalore", "image": "bang.png"},
        {"name": "Hyderabad", "image": "hyd.png"},
        {"name": "Chandigarh", "image": "chd.png"},
        {"name": "Ahmedabad", "image": "ahd.png"},
        {"name": "Pune", "image": "pune.png"},
        {"name": "Kolkata", "image": "kolk.png"},
        {"name": "Kochi", "image": "koch.png"},
        {"name": "Chennai", "image": "chen.png"},
    ]
    return render(request, 'book/index.html', {'cities': cities})



@cache_control(no_cache=True, must_revalidate=True)
def shortest_path_view(request):
    if request.method == "POST":
        start_stall = request.POST.get("start_stall").strip()
        end_stall = request.POST.get("end_stall").strip()

        # File paths for data and layout image
        stalls_path = r'D:\Book-fair\bookstall\book\box_information_with_ocr.xlsx'
        blank_spaces_path = r"D:\Book-fair\bookstall\book\box_5_information.xlsx"
        layout_image_path = r"D:\Book-fair\bookstall\book\static\book\images\cbf2024.jpg"
        output_image_path = r"D:\Book-fair\bookstall\book\static\book\images\shortest_path_result1.jpg"

        # Load data
        stalls, blank_spaces = load_data(stalls_path, blank_spaces_path)
        stalls['center_x'] = (stalls['x_min'] + stalls['x_max']) / 2
        stalls['center_y'] = (stalls['y_min'] + stalls['y_max']) / 2
        stalls['Name (stall_number)'] = stalls['Name (stall_number)'].astype(str).str.strip()

        # Build graph
        graph = build_graph(blank_spaces)

        # Validate input
        start_row = stalls.loc[stalls['Name (stall_number)'] == start_stall]
        end_row = stalls.loc[stalls['Name (stall_number)'] == end_stall]
        if start_row.empty or end_row.empty:
            return JsonResponse({"error": "Invalid start or end stall number"}, status=400)

        # Compute shortest path
        start_node = find_nearest_node(graph, start_row['center_x'].values[0], start_row['center_y'].values[0])
        end_node = find_nearest_node(graph, end_row['center_x'].values[0], end_row['center_y'].values[0])

        try:
            path = nx.shortest_path(graph, source=start_node, target=end_node, weight="weight")
        except nx.NetworkXNoPath:
            return JsonResponse({"error": "No path found between the selected stalls"}, status=400)

        # Always regenerate the image
        plot_path(graph, stalls, blank_spaces, start_stall, end_stall, path, layout_image_path, output_image_path)

        return JsonResponse({"image_path": "/static/book/images/shortest_path_result1.jpg"})
    return render(request, "book/shortest_path.html")


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Override default permissions

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        # Your login logic
        return Response({"key": "generated-auth-token"}, status=status.HTTP_200_OK)
    
class RegistrationView(APIView):
    def post(self, request):
        # Your registration logic
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    
class ProtectedView(APIView):
    def get(self, request):
        return Response({'message': 'You have accessed a protected endpoint.'})


