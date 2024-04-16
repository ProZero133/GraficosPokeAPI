import requests

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

# Llamamos a la función para obtener la información de los Pokémon con ID del 1 al 200
for pokemon_id in range(15, 201):
    print(f"Obteniendo información del Pokémon con ID {pokemon_id}...")
    pokemon_name, pokemon_types, generation_name = get_pokemon_info(pokemon_id)
    if pokemon_name:
        print(f"Nombre del Pokémon: {pokemon_name}")
        print(f"Tipo(s) del Pokémon: {', '.join(pokemon_types)}")
        print(f"Generación del Pokémon: {generation_name}")
        print()
