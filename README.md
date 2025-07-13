✈️ Airline Market Demand Dashboard
A data-driven web app that visualizes U.S. airline route demand using a clean and interactive dashboard built with Flask, Chart.js, and Bootstrap.

📊 Features
🔍 Search & Filter: Real-time search and city dropdown to filter by route origin.

✈️ Top 5 Popular Routes: Table view of routes with the most bookings.

💸 Average Fare Chart: Horizontal bar chart for the top 20 most expensive routes.

📈 Monthly Booking Demand: Line chart showing trends over time.

📥 CSV Downloads: Export datasets for custom analysis.

🌙 (Optional) Dark Mode Toggle

📊 Gemini summary integration (currently commented out due to API plan limitations)

🧠 Project Approach
Preprocessed and cleaned a public dataset of airline fares and routes.

Implemented dynamic visualizations using Chart.js and Flask templating (Jinja2).

Optimized data handling for Render’s 512MB RAM free-tier limit by reducing the dataset size while keeping the integrity of analytics intact.

Gemini Pro integration was included but commented due to API restrictions.

🚀 Live Demo
📦 GitHub: https://github.com/SohamGhorpade326/Airline

🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML, Bootstrap, JavaScript, Chart.js

Data: Cleaned .csv file (U.S. airline fare dataset)

Optional API: Gemini (Google Generative AI)

📁 Folder Structure
plaintext
Copy
Edit
Airline/
├── static/
│   └── data/
│       └── us_airline_fares.csv
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
└── README.md
📦 Installation & Running Locally
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/SohamGhorpade326/Airline
cd Airline

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
Then go to http://127.0.0.1:5000 in your browser.

🔐 Environment Variables (Optional for Gemini)
Create a .env file:

env
Copy
Edit
GEMINI_API_KEY=your_google_generative_ai_key
🧪 Example Data Source
The project uses a cleaned version of publicly available airline fare data (manually preprocessed to reduce size for deployment). It can be updated with real API-based integrations in future versions.

❓Questions / Future Improvements
Should we integrate a login system for personalized summaries or saving filters?

Can we expand to include international routes or airport-level stats?

Is real-time API-based data preferred over static datasets?
