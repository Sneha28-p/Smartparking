import heapq
from collections import defaultdict
from datetime import datetime

class ParkingLot:
    def __init__(self, lot_id, available):
        self.lot_id = lot_id
        self.available = available

class Graph:
    def __init__(self):  
        self.nodes = {}
        self.edges = defaultdict(list)
        self.weights = {}
        self.vehicle_map = {}  

    def add_parking_lot(self, lot_id, available):
        self.nodes[lot_id] = ParkingLot(lot_id, available)

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            current_distance, current_node = heapq.heappop(queue)
            for neighbor in self.edges[current_node]:
                distance = current_distance + self.weights[(current_node, neighbor)]
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
        return distances

    def allocate_parking(self, vehicle_id, vehicle_location):
        if vehicle_id in self.vehicle_map:
            return f"Vehicle '{vehicle_id}' is already parked at lot '{self.vehicle_map[vehicle_id]}'."

        if vehicle_location not in self.nodes:
            return "Invalid vehicle location."

        distances = self.dijkstra(vehicle_location)
        min_heap = []

        for lot_id, lot in self.nodes.items():
            if lot.available > 0:
                heapq.heappush(min_heap, (distances[lot_id], lot_id))

        if not min_heap:
            return "No parking available"

        _, nearest_lot_id = heapq.heappop(min_heap)
        self.nodes[nearest_lot_id].available -= 1
        self.vehicle_map[vehicle_id] = nearest_lot_id

        log_entry = (
            f"{datetime.now()} - Vehicle '{vehicle_id}' at {vehicle_location} "
            f"allocated to Lot '{nearest_lot_id}'"
        )
        self.log_action(log_entry)
        return f"Vehicle '{vehicle_id}' allocated parking at lot '{nearest_lot_id}'"

    def release_parking(self, vehicle_id):
        if vehicle_id not in self.vehicle_map:
            return f"Vehicle '{vehicle_id}' is not currently parked."

        lot_id = self.vehicle_map.pop(vehicle_id)
        self.nodes[lot_id].available += 1

        log_entry = (
            f"{datetime.now()} - Vehicle '{vehicle_id}' exited from Lot '{lot_id}'"
        )
        self.log_action(log_entry)
        return f"Vehicle '{vehicle_id}' released parking from lot '{lot_id}'"

    def log_action(self, log_entry):
        print(log_entry)
        with open("allocations_log.txt", "a") as file:
            file.write(log_entry + "\n")


graph = Graph()
n = int(input("Enter number of parking lots: "))
for _ in range(n):
    lot_id = input("Enter parking lot ID: ")
    available = int(input(f"Enter available slots in lot {lot_id}: "))
    graph.add_parking_lot(lot_id, available)

e = int(input("Enter number of roads (edges): "))
for _ in range(e):
    from_node = input("From lot: ")
    to_node = input("To lot: ")
    weight = int(input(f"Distance between {from_node} and {to_node}: "))
    graph.add_edge(from_node, to_node, weight)


while True:
    print("\n--- Parking System ---")
    print("1. Allocate Parking (Vehicle Entry)")
    print("2. Release Parking (Vehicle Exit)")
    print("3. Exit System")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        vehicle_id = input("Enter vehicle ID: ")
        location = input("Enter current location of vehicle: ")
        print(graph.allocate_parking(vehicle_id, location))

    elif choice == '2':
        vehicle_id = input("Enter vehicle ID to exit:")
        print(graph.release_parking(vehicle_id))
    elif choice=='3':
        print("System exited.Logs saved to 'allocations_log.txt'.")
        break
    else:
        print("Invalid choise.Please enter 1,2 or 3")