import os
import pandas as pd
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

# Load .env variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def load_process(filter_city=None):
    df = pd.read_csv('static/data/us_airline_fares.csv')
    df = df[['city1', 'city2', 'fare', 'Year', 'quarter']].dropna()
    df['fare'] = pd.to_numeric(df['fare'], errors='coerce')
    df = df.dropna(subset=['fare'])
    df['route'] = df['city1'] + ' → ' + df['city2']
    df['month'] = df['Year'].astype(str) + '-Q' + df['quarter'].astype(str)

    if filter_city:
        df = df[df['city1'] == filter_city]

    popular_routes = df['route'].value_counts().head(5).reset_index()
    popular_routes.columns = ['route', 'count']

    avg_price = df.groupby('route')['fare'].mean().reset_index()
    avg_price.columns = ['route', 'average_fare']
    avg_price = avg_price.sort_values(by='average_fare', ascending=False).head(20)

    demand = df['month'].value_counts().sort_index().reset_index()
    demand.columns = ['month', 'bookings']

    cities = sorted(df['city1'].unique().tolist())
    return popular_routes, avg_price, demand, cities

def generate_summary(popular_routes, avg_price, demand):
    try:
        model = genai.GenerativeModel("gemini-pro")

        top_route = popular_routes.iloc[0]['route']
        top_count = int(popular_routes.iloc[0]['count'])
        max_demand_month = demand.iloc[demand['bookings'].idxmax()]['month']
        price_min = int(avg_price['average_fare'].min())
        price_max = int(avg_price['average_fare'].max())

        prompt = (
            f"Summarize this airline booking demand data:\n"
            f"- Most popular route: {top_route} with {top_count} bookings\n"
            f"- Month with highest demand: {max_demand_month}\n"
            f"- Average fares range: ${price_min} to ${price_max}\n"
            f"Generate a short 2-line market insight summary."
        )

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Gemini error: {e}"



@app.route('/')
def index():
    filter_city = request.args.get('filter_city')
    popular_routes, avg_price, demand, cities = load_process(filter_city)
    summary = generate_summary(popular_routes, avg_price, demand)

    return render_template(
        'index.html',
        routes=popular_routes.to_dict(orient='records'),
        price_trend=avg_price.to_dict(orient='records'),
        demand=demand.to_dict(orient='records'),
        cities=cities,
        selected_city=filter_city,
        summary=summary
    )

@app.route('/download/<datatype>')
def download_csv(datatype):
    filter_city = request.args.get('filter_city')
    popular_routes, avg_price, demand, _ = load_process(filter_city)

    data_map = {
        'popular_routes': popular_routes,
        'average_fare': avg_price,
        'demand': demand
    }

    if datatype not in data_map:
        return "Invalid data type", 400

    csv = data_map[datatype].to_csv(index=False)
    return Response(
        csv,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={datatype}.csv'}
    )

if __name__ == '__main__':
    app.run(debug=True)
