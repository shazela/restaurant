
from flask import Flask, request, jsonify
from rasa_sdk import Tracker, FormValidationAction, Action
import requests
import json





app = Flask(__name__)

@app.route('/hello/', methods=['POST'])


# link: POST : http://localhost:105/hello/
# Postman body: json, raw
# { 
# "starter_type" : "paneer tikka",
# "food_type" : "pasta",
# "dessert_type" : "eclair"
# }

def order():
    ALLOWED_starter_typeS = ["mozzarella sticks", "paneer tikka", "veggie mix", "chicken tikka", "crispy chicken"]
    ALLOWED_food_typeS = ["pasta", "aloo gobhi", "rajma chawal", "butter chicken", "chicken curry"]
    ALLOWED_dessert_typeS = ["ice cream", "rasgulla", "rasmalai", "cheesecake", "eclair"]
    data = json.loads(request.data)
    print("### data is --->", data)
    starter = request.json['starter_type']
    main = request.json['food_type']
    dessert = request.json['dessert_type']
    print("### starter is --->", starter)
    print("### main course is --->", main)
    print("### dessert is --->", dessert)
    if starter in ALLOWED_starter_typeS and main in ALLOWED_food_typeS and dessert in ALLOWED_dessert_typeS:
        response_message = 'Order Successful'
        # all slots reset to be added
    else:
        response_message = "Order unsuccessful!"
    
    response_code = 200

    response = {
        'code': response_code,
        'message': response_message
    }

    return jsonify(response)


    # errorMessage = " "
    # if starter in ALLOWED_starter_typeS:
    #     isOrderSuccessful = True
    # else:
    #     errorMessage = "kindly select the correct starter"
    #     isOrderSuccessful = False
    # if main in ALLOWED_food_typeS:
    #     isOrderSuccessful = True
    # else:
    #     errorMessage = "kindly select the correct main course"
    #     isOrderSuccessful = False
    # if dessert in ALLOWED_dessert_typeS:
    #     isOrderSuccessful = True
    # else:
    #     errorMessage = "kindly select the correct dessert"
    #     isOrderSuccessful = False
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)