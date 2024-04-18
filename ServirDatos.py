from flask import Flask, render_template, json, jsonify
from pymongo import MongoClient
from collections import defaultdict

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Configura la conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["pokemon_db"]
collection = db["pokemon_collection"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pokemonData')
def pokemon_data():
    # Define las generaciones que quieres incluir
    FiltrarGeneracion = ["generation-i", "generation-ii", "generation-iii", "generation-iv"]

    # Consulta la colección de MongoDB y agrupa por generación y tipo
    TiposPorGeneracion = defaultdict(lambda: defaultdict(int))
    
    for pokemon in collection.find():
        generation = pokemon.get('generation')
        types = pokemon.get('types', [])
        
        # Solo incluye las generaciones especificadas
        if generation in FiltrarGeneracion:
            for pokemon_type in types:
                TiposPorGeneracion[generation][pokemon_type] += 1
    
    # Combina las generaciones en pares
    combined_data = []
    for i in range(0, len(FiltrarGeneracion), 2):
        combined_types_count = defaultdict(int)
        for generation in FiltrarGeneracion[i:i+2]:
            for pokemon_type, count in TiposPorGeneracion[generation].items():
                combined_types_count[pokemon_type] += count
        combined_data.append({
            "generations": FiltrarGeneracion[i:i+2],
            "types": [{"type": pokemon_type, "count": count} for pokemon_type, count in combined_types_count.items()]
        })
    
    # Devuelve los datos como JSON
    return jsonify(combined_data)

# Ejecuta la aplicación en modo de desarrollo
if __name__ == '__main__':
    app.run(debug=True)