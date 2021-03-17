import cs50
import pandas as pd
import sys
import csv

# Cursor a la base de datos 
db = cs50.SQL("sqlite:///specs.db")

brands_dict = {
    0 : 'SlurryPro',
    1 : 'Toro',
    2 : 'Techniflo',
    3 : 'Audex'
}

print("Bienvenido a la base de datos de Información Técnica\n")
print("Actualizando base de datos...")

# Definición de las funciones principales

# Función principal - Se encarga de preguntar al usuario y consultar la base de datos en "specs.db"
def main():

    print("Por favor, elija una marca para comenzar la selección y luego presione 'Enter'")
    print("[0] SlurryPro\n[1] Toro\n[2] Techniflo\n[3] Audex\n")

    # 'br' short for 'brand'
    br = cs50.get_int('Escriba el número correspondiente acá abajo\n') 
    # Chequear
    if br > 3:
        sys.exit("Error al escribir el número")

    # Relacionar input con una marca
    brand_chosen = brands_dict[br]
        
    # Buscar cuántas líneas hay
    lines = db.execute("SELECT Line from specs WHERE Brand = ? GROUP BY Line", brand_chosen)

    # Preguntar al usuario
    i = 0
    print("\nPor favor, seleccione una línea\n")
    
    lines_dict = {}

    for line in lines:
        print(f"[{i}] {line['Line']}")
        lines_dict[f'{i}'] = line['Line']
        i += 1 


    # "ln" short for "line"
    ln = cs50.get_int('\nEscriba el número correspondiente acá abajo\n')
    # Chequear
    if ln >= i:
        sys.exit("Error al escribir el número")

    # Relacionar input con una línea
    line_chosen = lines_dict[str(ln)]

    # Buscar cuántas series hay
    series = db.execute("SELECT Series FROM specs WHERE Brand = ? AND Line = ? GROUP BY Series", brand_chosen, line_chosen)

    # Preguntar al usuario
    j = 0
    print("\nPor favor, seleccione una serie\n")

    series_dict = {}

    for series_singular in series:
        print(f"[{j}] {series_singular['Series']}")
        series_dict[f'{j}'] = series_singular['Series']
        j += 1

    # "sr" short for "series"
    sr = cs50.get_int('\nEscriba el número correspondiente acá abajo\n') 
    # Chequear
    if sr >= j:
        sys.exit("Error al escribir el número")

    # Relacionar input con una serie        
    series_chosen = series_dict[str(sr)]

    # Buscar todos los modelos
    models = db.execute("SELECT Model FROM specs WHERE Brand = ? AND Line = ? AND Series = ? GROUP BY Model", brand_chosen, line_chosen, series_chosen)

    # Preguntar al usuario
    k = 1
    print("\nPor favor, seleccione un modelo\n")
    print("[0] Ver todas")

    models_dict ={}

    for model in models:
        print(f"[{k}] {model['Model']}")
        models_dict[f'{k}'] = model['Model']
        k += 1

    # "md" short for "model"
    md = cs50.get_int('\nEscriba el número correspondiente acá abajo\n')
    # Chequear
    if md >= k:
        sys.exit("Error al escribir el número\n")

    # Si se quiere visualizar todas las bombas de la misma línea
    if md == 0:
        all_models = db.execute("SELECT * FROM specs WHERE Brand = ? AND Line = ? AND Series = ?", 
                        brand_chosen, line_chosen, series_chosen,)
        
        df_all = pd.DataFrame(all_models)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)

        units2= []
        units2.insert(0, {
            'id': '',
            'Brand': '',
            'Line': '',
            'Series': '',
            'Model': '',
            'Speed':'RPM',
            'Capacity':'m3/hr',
            'Shutoff_Head':'m',
            'Max_speed':'RPM',
            'Max_power':'kW',
            'Discharge':'in',
            'Suction':'in',
            'Max_solids':'mm',
            'Temperature':'°C',
            'Weight':'kg',
        })

        df_final2 = pd.concat([pd.DataFrame(units2), df_all], ignore_index=True)

        print(df_final2)
        input("Presiona 'Enter'para una nueva búsqueda")
        print("")
        main()
    


    #else
    # Relacionar input con un modelo
    model_chosen = models_dict[str(md)]

    # Crear DataFrame para mostrar las especificaciones

    model = db.execute("SELECT * FROM specs WHERE Brand = ? AND Line = ? AND Series = ? AND Model = ?", 
                        brand_chosen, line_chosen, series_chosen, model_chosen)

    df = pd.DataFrame(model)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    units= []
    units.insert(0, {
        'id': '',
        'Brand': '',
        'Line': '',
        'Series': '',
        'Model': '',
        'Speed':'RPM',
        'Capacity':'m3/hr',
        'Shutoff_Head':'m',
        'Max_speed':'RPM',
        'Max_power':'kW',
        'Discharge':'in',
        'Suction':'in',
        'Max_solids':'mm',
        'Temperature':'°C',
        'Weight':'kg',
    })

    df_final = pd.concat([pd.DataFrame(units), df], ignore_index=True)
    
    print(df_final)
        
    input("\nPresiona 'Enter'para una nueva búsqueda\n")
    
    main()

# Detecta nuevas entradas en "database.csv" y las inserta en "specs.db"
def update():
    # Se decidió que la manera más simple y eficiente es eliminar todos los datos de la tabla
    # y luego cargar nuevamente todo

    db.execute("DELETE FROM specs")

    # Abrir base de datos editable:
    with open('database.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')

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

            # Insertar la información almacenada 
            db.execute("""INSERT INTO specs (id, Brand, Line, Series, Model, Speed, Capacity, Shutoff_Head, Max_speed, Max_power, Discharge, Suction, Max_solids, Temperature, Weight) 
                        VALUES(:id, :brand, :line, :series, :model, :speed, :capacity, :head, :max_speed, :max_power, :dis, :suc, :max_solids, :temp, :weight)""",
                        id=id, brand=brand, line=line, series=series, model=model, speed=speed, capacity=capacity, head=head, max_speed=max_speed,
                        max_power=max_power, dis=dis, suc=suc, max_solids=max_solids, temp=temp, weight=weight)



update()
print("Listo!\n")
main() 


