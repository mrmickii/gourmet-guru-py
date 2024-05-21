from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

data = pd.read_csv("../local-restaurant-data.csv")
data.drop_duplicates(inplace=True)

greetings = ["hello", "hi", "hey", "howdy", "greetings"]
goodbyes = ["bye", "goodbye", "see you", "farewell", "take care"]
recommendation_phrases = ["recommend a local food restaurant", "suggest a local restaurant", "find a local food place", "local food recommendation"]

def get_restaurant_recommendations(location, cuisine, price_level):
    filtered_data = data[data['Location'].str.contains(location, case=False, na=False)]
    if cuisine:
        filtered_data = filtered_data[filtered_data['Type'].str.contains(cuisine, case=False, na=False)]

    price_ranges = {
        1: "$",
        2: "$$",
        3: "$$$",
        4: "$$$$"
    }
    selected_price = price_ranges.get(price_level, "")
    if selected_price:
        filtered_data = filtered_data[filtered_data['Price_Range'].str.contains(selected_price, na=False)]

    return filtered_data.to_dict(orient='records')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message').strip().lower()
    response = {"message": ""}
    if any(greeting in user_input for greeting in greetings):
        response["message"] = "Hello! How can I assist you today?"
    elif any(goodbye in user_input for goodbye in goodbyes):
        response["message"] = "Goodbye! See you later!"
    elif any(phrase in user_input for phrase in recommendation_phrases):
        response["message"] = "Sure! Here are some local food restaurant recommendations:\n"
        recommendations = get_restaurant_recommendations("Cebu City, Philippines", "", 2)
        if recommendations:
            for restaurant in recommendations:
                response["message"] += f"- {restaurant['Name']} - {restaurant['Street Address']} - {restaurant['Location']}\n"
        else:
            response["message"] += "Sorry, I couldn't find any local food restaurant recommendations.\n"
    else:
        recommendations = get_restaurant_recommendations("Cebu City, Philippines", user_input, 2)
        if recommendations:
            response["message"] = f"Here are some {user_input} restaurants in Cebu City, Philippines:\n"
            for restaurant in recommendations:
                response["message"] += f"- {restaurant['Name']} - {restaurant['Street Address']} - {restaurant['Location']}\n"
        else:
            response["message"] = f"Sorry, I couldn't find any {user_input} restaurants in Cebu City, Philippines.\n"
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
