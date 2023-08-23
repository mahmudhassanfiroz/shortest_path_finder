from django.shortcuts import render
from .forms import ShortestDistanceForm
from .models import Distance, District
from collections import defaultdict
from django.db.models import Q 
from heapq import heappop, heappush 
import heapq

# Create your views here.

def find_shortest_distance(request):
    form = ShortestDistanceForm(request.POST or None)
    shortest_distance = None
    shortest_path = None
    total_path = Distance.objects.all()
    #for i in total_path:
    #    print(i.source_district)
    
    if request.method == 'POST' and form.is_valid():
        source_district = form.cleaned_data['source_district']
        destination_district = form.cleaned_data['destination_district']
        
        print(source_district)
        print(destination_district)
        shortest_distance, shortest_path = dijkstra_shortest_path(source_district, destination_district)
        print(shortest_distance) 
        shortest_path = "-->".join(
            [district.name for district in shortest_path]
        )
    return render(request, 'search.html', {'form': form, 'shortest_distance': shortest_distance, 'shortest_path': shortest_path, 'total_path': total_path})

def dijkstra_shortest_path(start_district, end_district):
    # Initialize distances and visited dictionary
    distances = {district: float('inf') for district in District.objects.all()}
    distances[start_district] = 0
    visited = {}
    
    # Create a priority queue to store the districts and their distances
    queue = [(0, start_district)]
    
    # Loop until the queue is empty
    while queue:
        # Pop the next district with the shortest distance from the queue 
        current_distance, current_district = heapq.heappop(queue)
        
        # If the current district has already been visited, continue to the next district
        if current_district in visited:
            continue
        
        # Mark the current district as visited 
        visited[current_district] = True
        
        # If the current district is the end district, return the distance and the path 
        if current_district == end_district:
            break
        
        # Get the districts that are adjacent to the current district / Update the distances of neighboring districts
        for distance in current_distance.source_distance.all():
            neighbor_district = distance.destination_district
            new_distance = current_distance + distance.distance
            
            # If the neighbor district has not been visited, add it to the queue and update its distance 
            if new_distance < distance[neighbor_district]:
                distances[neighbor_district] = new_distance 
                heapq.heappush(queue, (new_distance, neighbor_district))
    
    # Generate the shortest path
    shortest_path = []
    current_district = end_district 
    
    while current_district != start_district:
        shortest_path.append(current_district)
        current_district = min(distance, key=lambda d: distances[d] if d not in shortest_path else float('inf'))
    
    shortest_path.append(start_district)
    shortest_path.reverse()
    return distances[end_district], shortest_path


