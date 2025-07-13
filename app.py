import os
import pandas as pd
from flask import Flask, render_template, request, Response
from dotenv import load_dotenv

app = Flask(__name__)

# Load .env variables
load_dotenv()

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

# Dummy placeholder since summary field is used in HTML
def generate_summary(popular_routes, avg_price, demand):
    return "📊 AI summary is currently disabled."

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
