from flask import Blueprint, request, jsonify
import json
import os

#Skapar en Blueprint för bil-relaterade routes
cars_bp = Blueprint("cars_bp", __name__)

#skapar korrekt sökväg till cars.json i projektets rotmapp
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(os.path.dirname(BASE_DIR), "cars.json")

#Läser in alla bilar från JSON-filen
def load_cars():
    if not os.path.exists(FILE_NAME):
        return {}

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}

#Spara bilar till JSON_filen
def save_cars(cars: dict):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4, ensure_ascii=False)

#startsida
@cars_bp.get("/")
def home():
    return {"message": "Ruffel & Båg Car API is running"}

#GET/cars- Hämta alla bilar
@cars_bp.get("/cars")
def get_cars():
    cars = load_cars()
    return jsonify(cars), 200

#POST/cars- Skapa ny bil
@cars_bp.post("/cars")
def create_car():
    cars = load_cars()
    data = request.get_json(silent=True)

    if not data:
        return {"error": "Body måste vara JSON"}, 400

    regnr = data.get("regnr")
    if not regnr:
        return {"error": "regnr är obligatoriskt"}, 400

    if regnr in cars:
        return {"error": "Bil med detta regnr finns redan"}, 409

    car_data = {k: v for k, v in data.items() if k != "regnr"}
    cars[regnr] = car_data
    save_cars(cars)

    return {"message": "Bil skapad", "regnr": regnr, "car": cars[regnr]}, 201

#GET/cars<regnr>- Hämta specifik bil
@cars_bp.get("/cars/<regnr>")
def get_car(regnr):
    cars = load_cars()

    if regnr not in cars:
        return {"error": "Hittade ingen bil med detta regnr"}, 404

    return {"regnr": regnr, **cars[regnr]}, 200

#PUT/cars<regnr>- Uppdatera bil
@cars_bp.put("/cars/<regnr>")
def update_car(regnr):
    cars = load_cars()

    if regnr not in cars:
        return {"error": "Hittade ingen bil att uppdatera"}, 404

    data = request.get_json(silent=True)
    if not data:
        return {"error": "Body måste vara JSON"}, 400
#Uppdaterar endast skcikade fält
    for key, value in data.items():
        if key != "regnr":
            cars[regnr][key] = value

    save_cars(cars)
    return {"message": "Bil uppdaterad", "regnr": regnr, "car": cars[regnr]}, 200

#DELETE/cars<regnr>- Radera bil
@cars_bp.delete("/cars/<regnr>")
def delete_car(regnr):
    cars = load_cars()

    if regnr not in cars:
        return {"error": "Hittade ingen bil att radera"}, 404

    deleted_car = cars.pop(regnr)
    save_cars(cars)

    return {"message": "Bil raderad", "regnr": regnr, "deleted": deleted_car}, 200
