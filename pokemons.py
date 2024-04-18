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
        nombre_pokemon = data["name"]
        tipo_pokemon = [t["type"]["name"] for t in data["types"]]
        generation_url = data["species"]["url"]
        generation_info = requests.get(generation_url).json()
        generation_name = generation_info["generation"]["name"]
        
        return nombre_pokemon, tipo_pokemon, generation_name
    else:
        print(f"No se pudo obtener la información del Pokémon con ID o nombre {pokemon_id_or_name}.")
        return None, None, None
        
def AlmacenarEnMongo(pokemon_id_or_name):
    nombre_pokemon, tipo_pokemon, generation_name = get_pokemon_info(pokemon_id_or_name)
    
    if nombre_pokemon:
        pokemon_data = {
            "pokemon_id": pokemon_id_or_name,
            "name": nombre_pokemon,
            "types": tipo_pokemon,
            "generation": generation_name
        }

        collection.insert_one(pokemon_data)

def IdUltimoIngresado():
    UltimaIDPokemon = collection.find_one({}, sort=[("pokemon_id", -1)])
    
    if UltimaIDPokemon is None:
        return 1
    
    return UltimaIDPokemon["pokemon_id"] + 1

start_id = IdUltimoIngresado()
print("reanudando desde el ID", start_id)

for pokemon_id in range(start_id, 1001):
    print(f"Obteniendo información del Pokémon con ID {pokemon_id}...")
    nombre_pokemon, tipo_pokemon, generation_name = get_pokemon_info(pokemon_id)
    if nombre_pokemon:
        print(f"Nombre del Pokémon: {nombre_pokemon}")
        print(f"Tipo(s) del Pokémon: {', '.join(tipo_pokemon)}")
        print(f"Generación del Pokémon: {generation_name}")
        print()
        AlmacenarEnMongo(pokemon_id)
        print(f"Datos del Pokémon con ID {pokemon_id} guardados en la base de datos.\n")


