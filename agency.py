import redis
import json


class AgencyManager:
    r = redis.Redis(db=7)
    passenger_id = 0
    trip_id = 0
    tour_id = 0

    def add_passenger(self):
        self.passenger_id += 1
        name = input("Please enter name: ")
        age = input("Please enter age: ")
        phone_number = input("Please enter phone_number: ")
        self.r.hset(f"{self.passenger_id}", mapping={"name": name, "age": age, "phone_number": phone_number})

    def show_passenger(self, name: str):
        return self.r.hgetall(name)

    def add_trip(self):
        self.trip_id += 1
        departure = input("Please enter departure: ")
        destination = input("Please enter destination: ")
        duration = input("Please enter duration: ")
        vehicle = input("Please enter vehicle: ")
        passenger_ids = input("Please enter passenger ids:(1 4 5 ...) ").split(' ')
        passengers = {}
        for i in passenger_ids:
            passenger = self.r.hgetall(i)
            for k in passenger:
                passenger[k.decode('utf-8')] = passenger.pop(k).decode('utf-8')
            passengers[i] = passenger

        trip = {
            "departure": departure,
            "destination": destination,
            "duration": duration,
            "vehicle": vehicle,
            "passengers": json.dumps(passengers)
        }

        self.r.hset(f"{self.trip_id}", mapping=trip)

    def show_trip(self, trip_id):
        return self.r.hgetall(trip_id)

    def add_tour(self):
        self.tour_id += 1
        leader = input("Please enter leader name: ")
        departure = input("Please enter departure: ")
        destination = input("Please enter destination: ")
        price = input("Please enter price: ")
        duration = input("Please enter duration: ")
        description = input("Please enter description: ")
        passenger_ids = input("Please enter passenger ids:(1 4 5 ...) ").split(' ')
        passengers = {}

        for i in passenger_ids:
            passenger = self.r.hgetall(i)
            for k in passenger:
                passenger[k.decode('utf-8')] = passenger.pop(k).decode('utf-8')
            passengers[i] = passenger

        tour = {
            "leader": leader,
            "departure": departure,
            "destination": destination,
            "duration": duration,
            "price": price,
            "description": description,
            "passengers": json.dumps(passengers),
        }

        self.r.hset(f"{self.trip_id}", mapping=tour)

    def show_tour(self, tour_id):
        return self.r.hgetall(tour_id)


if __name__ == '__main__':
    am = AgencyManager()
    am.r.flushdb()

    for i in range(2):
        am.add_passenger()

    am.add_trip()

    am.add_tour()

    print(am.show_trip('1'))
    print(am.show_tour('1'))
