from flask import Flask

# Créer une application Flask
app = Flask(__name__)

# Définir un itinéraire pour la page d'accueil
@app.route('/')
def hello_world():
    return "Ce robot est fabriqué par Maniafatic et actuellement il est hébergé et en direct pour tout Manifatic."

# Exécutez l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
