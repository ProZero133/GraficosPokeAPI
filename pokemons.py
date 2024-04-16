import requests
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["pokemon_db"]
collection = db["pokemon_collection"]

def get_pokemon_info(pokemon_id_or_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id_or_name}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_name = data["name"]
        pokemon_types = [t["type"]["name"] for t in data["types"]]
        generation_url = data["species"]["url"]
        generation_info = requests.get(generation_url).json()
        generation_name = generation_info["generation"]["name"]
        
        return pokemon_name, pokemon_types, generation_name
    else:
        print(f"No se pudo obtener la información del Pokémon con ID o nombre {pokemon_id_or_name}.")
        return None, None, None
        
def save_pokemon_data(pokemon_id_or_name):
    # Obtén los datos del Pokémon
    pokemon_name, pokemon_types, generation_name = get_pokemon_info(pokemon_id_or_name)
    
    # Crea un documento con los datos obtenidos
    if pokemon_name:
        pokemon_data = {
            "pokemon_id": pokemon_id_or_name,
            "name": pokemon_name,
            "types": pokemon_types,
            "generation": generation_name
        }
        # Inserta el documento en la colección de MongoDB
        collection.insert_one(pokemon_data)

def get_last_stored_pokemon_id():
    # Encuentra el Pokémon con el ID más alto en la base de datos
    last_pokemon = collection.find_one({}, sort=[("pokemon_id", -1)])
    
    # Si no hay ningún documento, comienza desde el ID 1
    if last_pokemon is None:
        return 1
    
    # Si hay un documento, devuelve el ID del último Pokémon almacenado + 1
    return last_pokemon["pokemon_id"] + 1

# Obtener el ID desde el que comenzar a realizar solicitudes
start_id = get_last_stored_pokemon_id()
print("reanudando desde el ID", start_id)

# Llamamos a la función para obtener la información de los Pokémon con ID del 1 al 200
for pokemon_id in range(start_id, 201):
    print(f"Obteniendo información del Pokémon con ID {pokemon_id}...")
    pokemon_name, pokemon_types, generation_name = get_pokemon_info(pokemon_id)
    if pokemon_name:
        print(f"Nombre del Pokémon: {pokemon_name}")
        print(f"Tipo(s) del Pokémon: {', '.join(pokemon_types)}")
        print(f"Generación del Pokémon: {generation_name}")
        print()
        save_pokemon_data(pokemon_id)
        print(f"Datos del Pokémon con ID {pokemon_id} guardados en la base de datos.\n")


