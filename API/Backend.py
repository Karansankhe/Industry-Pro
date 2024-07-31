import os
import requests
import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini model with API key directly
genai.configure(api_key=os.getenv('GENAI_API_KEY'))
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Set the Alpha Vantage API key in the configuration
app.config['ALPHA_VANTAGE_API_KEY'] = os.getenv('ALPHA_VANTAGE_API_KEY')

# Function to fetch stock data from Alpha Vantage API
def fetch_alpha_vantage_stock_data(symbol):
    api_key = app.config['ALPHA_VANTAGE_API_KEY']
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Function to fetch stock data from Yahoo Finance using yfinance
def fetch_yfinance_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        # Convert the DataFrame to a dictionary and ensure all keys are strings
        data_dict = data.to_dict()
        data_dict_str_keys = {str(k): {str(inner_k): inner_v for inner_k, inner_v in v.items()} for k, v in data_dict.items()}
        return data_dict_str_keys
    except Exception as e:
        print(f"Error fetching data for {symbol} from Yahoo Finance: {str(e)}")
        return None

# Function to analyze stock data (placeholder)
def analyze_stock_data(data):
    # Replace with your specific analysis logic
    analysis = "Placeholder analysis"
    return analysis

# Function to interact with Gemini AI for stock-related queries
def get_gemini_response(symbol):
    prompt_template = (
        "You are an intelligent assistant with expertise in stock market analysis. "
        "Provide detailed insights or analysis on the following stock:\n\n"
        "Stock: {}\n"
        "Analysis:"
    )

    response = model.generate_content(prompt_template.format(symbol), stream=True)
    full_text = ""
    for chunk in response:
        full_text += chunk.text
    return full_text

@app.route('/fetch_stock_data', methods=['GET'])
def fetch_stock_data():
    symbol = request.args.get('symbol')
    source = request.args.get('source')

    if not symbol or not source:
        return jsonify({"error": "Please provide both symbol and source"}), 400

    if source == "alpha_vantage":
        data = fetch_alpha_vantage_stock_data(symbol)
    elif source == "yahoo_finance":
        data = fetch_yfinance_stock_data(symbol)
    else:
        return jsonify({"error": "Invalid source provided"}), 400

    if data:
        analysis = analyze_stock_data(data)
        gemini_response = get_gemini_response(symbol)
        return jsonify({
            "stock_data": data,
            "analysis": analysis,
            "gemini_response": gemini_response
        })
    else:
        return jsonify({"error": f"Failed to fetch data for {symbol}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
