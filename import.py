import csv
import cs50

# Crear cursor 

db = cs50.SQL("sqlite:///specs.db")

# Abrir y leer archivo "database.csv"

with open('database.csv', "r") as file:
    reader = csv.DictReader(file, delimiter=';')

    # Obtener datos del diccionario (reader)
    
    for row in reader:
        id = row["ID"]
        brand = row["brand"]
        line = row["line"]
        series = row["series"]
        model = row["model"]
        speed = row["speed"]
        capacity = row["capacity"]
        head = row["shutoff head"]
        max_speed = row["max speed"]
        max_power = row["max motor power"]
        dis = row["discharge"]
        suc = row["suction"]
        max_solids = row["max solids"]
        temp = row["temp"]
        weight = row["weight"]

        # Crear por única vez la tabla "specs" dentro del archivo specs.db
        db.execute("""CREATE TABLE IF NOT EXISTS 'specs' ( 'id' INTEGER NOT NULL,
                        'Brand' TEXT NOT NULL,
                        'Line' TEXT NOT NULL,
                        'Series' TEXT NOT NULL,
                        'Model' TEXT NOT NULL,
                        'Speed' INTEGER NOT NULL,
                        'Capacity' REAL NOT NULL,
                        'Shutoff_Head' REAL NOT NULL,
                        'Max_speed' INTEGER NOT NULL,
                        'Max_power' REAL NOT NULL,
                        'Discharge' REAL NOT NULL,
                        'Suction' REAL NOT NULL,
                        'Max_solids' REAL NOT NULL,
                        'Temperature' REAL NOT NULL,
                        'Weight' REAL NOT NULL)""")

        # Insertar la información almacenada hasta ese momento en database.csv
        db.execute("""INSERT INTO specs (id, Brand, Line, Series, Model, Speed, Capacity, Shutoff_Head, Max_speed, Max_power, Discharge, Suction, Max_solids, Temperature, Weight) 
                        VALUES(:id, :brand, :line, :series, :model, :speed, :capacity, :head, :max_speed, :max_power, :dis, :suc, :max_solids, :temp, :weight)""",
                        id=id, brand=brand, line=line, series=series, model=model, speed=speed, capacity=capacity, head=head, max_speed=max_speed,
                        max_power=max_power, dis=dis, suc=suc, max_solids=max_solids, temp=temp, weight=weight)
                        