from flask import Flask, render_template_string, request
from database import init_db, insert_city, insert_forecast, get_forecast_city
from api import get_city_info, get_forecast

app = Flask(__name__)
init_db()

HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Météo Dashboard</title>
    <style>
        * {box-sizing: border-box; margin: 0; padding: 0;}

        body {
            font-family: "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            min-height: 100vh;
            color: white;
            padding: 40px 20px;
        }

        body.bg {
            background-image: 
                linear-gradient(rgba(10,10,30,0.35), rgba(10,10,30,0.55)),
                url("/static/sunshine.webp");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }

        h1 {
            text-align: center;
            font-size: 3rem;
            margin-bottom: 30px;
            letter-spacing: 2px;
        }


        .search-bar {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 40px;
        }

        .search-bar input {
            padding: 12px 20px;
            border-radius: 30px;
            border: none;
            font-size: 1rem;
            width: 300px;
            background: rgba(255,255,255,0.1);
            color: white;
            outline: none;
        }

        .search-bar input::placeholder { color: rgba(255,255,255,0.5); }

        .search-bar button[type="submit"] {
            padding: 12px 25px;
            border-radius: 30px;
            border: none;
            background: #e94560;
            color: white;
            font-size: 1rem;
            cursor: pointer;
        }

        .search-bar button[type="submit"]:hover { background: #c73652; }

        .btn-change {
            padding: 10px 20px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.1);
            color: white;
            cursor: pointer;
            font-size: 0.9rem;
            backdrop-filter: blur(5px);
            transition: background 0.2s;
        }

        .btn-change:hover { background: rgba(255,255,255,0.2); }

        .city-title {
            text-align: center;
            font-size: 1.7rem;
            margin-bottom: 25px;
            opacity: 0.9;
        }

        .cards {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            max-width: 1100px;
            margin: 0 auto;
        }

        .card {
            background: rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 20px;
            width: 140px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s;
        }

        .card:hover { transform: translateY(-5px); }

        .card .date     { font-size: 0.9rem; opacity: 0.7; margin-bottom: 8px; }
        .card .icon     { font-size: 2rem; margin: 8px 0; }
        .card .desc     { font-size: 0.75rem; opacity: 0.8; margin-bottom: 10px; }
        .card .temps    { font-size: 1rem; font-weight: bold; }
        .card .temps span { opacity: 0.6; font-size: 0.85rem; }
        .card .details  { font-size: 0.75rem; opacity: 0.6; margin-top: 8px; }

        .error {
            text-align: center;
            color: #e94560;
            font-size: 1.1rem;
        }
    </style>
</head>
<body>
    <h1>Météo</h1>

    <div class="search-bar">
        <form method="GET" action="/" style="display:flex; gap:10px;">
            <input type="text" name="city" placeholder="Entrez une ville" value="{{ city_query }}" autofocus>
            <button type="submit">Rechercher</button>
            <button type="button" class="btn-change" onclick="changeBg()" id="bg-change">🐬</button>
        </form>
    </div>

    {% if error %}
        <p class="error">{{ error }}</p>

    {% elif forecasts %}
        <p class="city-title">📍 {{ forecasts[0].city_name }} - {{ forecasts[0].country }}</p>
        <div class="cards">
            {% for f in forecasts %}
            <div class="card">
                <div class="date">{{ f.date }}</div>
                <div class="icon">{{ f.icon }}</div>
                <div class="desc">{{ f.description }}</div>
                <div class="temps">
                    {{ f.temp_max }}° <span>/ {{ f.temp_min }}°</span>
                </div>
                <div class="details">
                    💧 {{ f.humidity }}%<br>
                    🌀 {{ f.wind }} km/h
                </div>
            </div>
            {% endfor %}
        </div>
    {% endif %}

    <script>
        function changeBg() {
            const btn = document.getElementById("bg-change");
            if (document.body.classList.contains("bg")) {
                document.body.classList.remove("bg");
            } else {
                document.body.classList.add("bg");
            }
        }
    </script>

</body>
</html>
"""

@app.route("/")
def index():
    city_query = request.args.get("city", "").strip()
    forecasts = []
    error = None

    if city_query:
        try:
            #Appel API
            city_info = get_city_info(city_query)
            forecast_data = get_forecast(city_info["latitude"], city_info["longitude"])

            #Stockage en base (INSERT SQL)
            city_id = insert_city(city_info)
            insert_forecast(city_id, forecast_data)

            #Lecture depuis la base (SELECT + JOIN SQL)
            forecasts = get_forecast_city(city_info["name"])

        except ValueError as e:
            error = f"Ville introuvable : {city_query}"

    return render_template_string(HTML, forecasts=forecasts, error=error, city_query=city_query)


if __name__ == "__main__":
    app.run(debug=True)