from typing import Text, List, Any, Dict
import requests
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, AllSlotsReset, Restarted


ALLOWED_starter_typeS = ["mozzarella sticks", "paneer tikka", "veggie mix", "chicken tikka", "crispy chicken"]
VEG_STARTER_ORDER = ["mozzarella sticks", "paneer tikka", "veggie mix"]
MEAT_STARTER_ORDER = ["chicken tikka", "crispy chicken"]

ALLOWED_food_typeS = ["pasta", "aloo gobhi", "rajma chawal", "butter chicken", "chicken curry"]
VEG_FOOD_ORDER = ["pasta", "aloo gobhi", "rajma chawal"]
MEAT_FOOD_ORDER = ["butter chicken", "chicken curry"]

ALLOWED_dessert_typeS = ["ice cream", "rasgulla", "rasmalai", "cheesecake", "eclair"]
VEG_DESSERT_ORDER = ["ice cream", "rasgulla", "rasmalai"]
MEAT_DESSERT_ORDER = ["cheesecake", "eclair"]


class AskForVegetarianAction(Action):
    def name(self) -> Text:
        return "action_ask_vegetarian"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="Would you like to order a vegetarian meal?",
            buttons=[
                {"title": "yes", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        
        return []



class AskForStarterTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_starter_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of starter do you want?",
                buttons=[{"title": p, "payload": p} for p in VEG_STARTER_ORDER],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_starter_typeS],
            )
        return []

class AskForFoodTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_food_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of main course do you want?",
                buttons=[{"title": p, "payload": p} for p in VEG_FOOD_ORDER],
                
            )
        
        else:
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_food_typeS],
            )
        SlotSet("food_type", "payload")
        return []
        
    
class AskForDessertTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_dessert_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of dessert do you want?",
                buttons=[{"title": p, "payload": p} for p in VEG_DESSERT_ORDER],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_dessert_typeS],
            )
        return []

class ValidateMenuForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_menu_form"

    def validate_vegetarian(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `vegetarian` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            dispatcher.utter_message(
                text=f"I'll remember you prefer vegetarian."
            )
            return {"vegetarian": True}
        if tracker.get_intent_of_latest_message() == "deny":
            dispatcher.utter_message(
                text=f"I'll remember that you don't want only vegetarian."
            )
            return {"vegetarian": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"vegetarian": None}

    

    def validate_starter_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `starter_type` value."""
        
        # if tracker.get_slot("vegetarian"):
        #     dispatcher.utter_message(
        #             text=f"We serve {'/'.join(VEG_STARTER_ORDER)}. What would you like?"
        #         )
        # else:
        #     dispatcher.utter_message(
        #             text=f"We serve {'/'.join(MEAT_STARTER_ORDER)} non veg starters and {'/'.join(VEG_STARTER_ORDER)} veg starters. What would you like?"
        #         )
            
        if slot_value not in ALLOWED_starter_typeS:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_starter_typeS)}."
            )
            return {"starter_type": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_starter_typeS)}."
            )
            return {"starter_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value}.")
        return {"starter_type": slot_value}
    
    def validate_food_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `food_type` value."""
        
        #print("!!!!this is the slot value", slot_value)  
        if slot_value not in ALLOWED_food_typeS:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_food_typeS)}."
            )
            return {"food_type": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_food_typeS)}."
            )
            return {"food_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value}.")
        return {"food_type": slot_value}
    
    
    
    def validate_dessert_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `dessert_type` value."""
        
        # if tracker.get_slot("vegetarian"):
        #     dispatcher.utter_message(
        #             text=f"We serve {'/'.join(VEG_DESSERT_ORDER)}. What would you like?"
        #         )
        # else:
        #     dispatcher.utter_message(
        #             text=f"We serve {'/'.join(MEAT_DESSERT_ORDER)} non veg starters and {'/'.join(VEG_DESSERT_ORDER)} veg starters. What would you like?"
        #         )

        if slot_value not in ALLOWED_dessert_typeS:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_dessert_typeS)}."
            )
            return {"dessert_type": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_dessert_typeS)}."
            )
            return {"dessert_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value}.")
        return {"dessert_type": slot_value}


class fetch_API(object):

    def __init__(self):
        self.url = "http://localhost:105/hello/"
        self.headers={
            "Content-Type": "application/json"
        }
        
    def ask(self, starter, main, dessert):
        #content  = self.prompt + "\n\n" + restaurants + "\n\n" + question
        body = {
            "starter_type": starter, 
            "food_type": main,
            "dessert_type": dessert,
            #"messages":[{"role": "user", "content": question}] ##
        }
        #print("###headers are", self.headers)
        #print("$$$ this is the url:", self.url)
        result = requests.post(
            url= "http://localhost:105/hello/",
            headers={
            "Content-Type": "application/json"
        },
            json=body
        )
        
        print("$$this is the result:", result.json())
        return result.json()["message"]
    
fetchapi=fetch_API()

class API(Action):
    def name(self) -> Text:
        return "action_API"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #previous_results = tracker.get_slot("results")
        try:
            starter = tracker.get_slot("starter_type")
            main = tracker.get_slot("food_type")
            dessert = tracker.get_slot("dessert_type")
            answer = fetch_API.ask(self, starter, main, dessert)
            dispatcher.utter_message(text = answer)
            return [AllSlotsReset(), Restarted()]
        except Exception as e:
            return [AllSlotsReset(), Restarted()]

class OrderSlots(Action):
    def name(self):
        return 'action_order_slots'
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if 'starter_type' in ALLOWED_starter_typeS and 'food_type' in ALLOWED_food_typeS and 'dessert_type' in ALLOWED_dessert_typeS:
            dispatcher.utter_message(text="I will order now")
        else:
            dispatcher.utter_message(text="error")

        
        return []