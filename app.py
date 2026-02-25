from flask import Flask
from routes.cars_bp import cars_bp

#Skapar Flask-applikationen
app = Flask(__name__)
#Registrerar Blueprint som innehåller alla bil-relaterade routes
app.register_blueprint(cars_bp)

#Startar applikationen i debug-läge vid lokal körning
if __name__ == "__main__":
    app.run(debug=True)