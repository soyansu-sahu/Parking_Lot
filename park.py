import random
import json
import boto3

class ParkingLot:
    def __init__(self, square_footage, spot_length=8, spot_width=12):
        self.spot_length = spot_length
        self.spot_width = spot_width
        self.parking_lot_size = square_footage // (spot_length * spot_width)
        self.parking_lot = [None] * self.parking_lot_size
        self.available_spots = list(range(self.parking_lot_size))
        self.parking_map = {}

    def park_vehicle(self, car):
        if not self.available_spots:
            return "No available spots. Parking lot is full."

        spot_number = random.choice(self.available_spots)
        self.parking_lot[spot_number] = car.license_plate
        self.available_spots.remove(spot_number)
        self.parking_map[car.license_plate] = spot_number
        return f"Car with license plate {car.license_plate} parked successfully in spot {spot_number}"

    def map_vehicles_to_spots(self):
        return {plate: index for index, plate in enumerate(self.parking_lot) if plate is not None}

    def get_size(self):
        return self.parking_lot_size

    def get_parking_lot_map(self):
        return self.parking_lot

class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    def __str__(self):
        return f"Car with license plate {self.license_plate}"

    def park(self, parking_lot):
        return parking_lot.park_vehicle(self)

def main():
    parking_lot = ParkingLot(square_footage=2000)
    # Create cars
    cars = [Car(str(i).zfill(7)) for i in range(20)]

    # Park cars in the parking lot
    print("\nParking cars...")
    for car in cars:
        result = car.park(parking_lot)
        print(result)

    # Print parking lot map
    print("\nParking Lot Map:", parking_lot.get_parking_lot_map())

    # Save parking lot map to a JSON file
    parking_lot_json = parking_lot.map_vehicles_to_spots()
    with open('parking_lot_map.json', 'w') as json_file:
        json.dump(parking_lot_json, json_file)
        print("\nParking Lot Map saved to parking_lot_map.json")

    # Upload to S3
    try:
        s3 = boto3.client('s3')
        bucket_name = 'your-s3-bucket-name'
        s3.upload_file('parking_lot_map.json', bucket_name, 'parking_lot_map.json')
        print(f"\nUploaded parking_lot_map.json to S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
    main()
