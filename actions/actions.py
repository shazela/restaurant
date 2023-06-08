from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict



ALLOWED_starter_typeS = ["mozzarella sticks", "paneer tikka", "veggie mix", "chicken tikka", "crispy chicken"]
VEG_STARTER_ORDER = ["mozzarella sticks", "paneer tikka", "veggie mix"]
MEAT_STARTER_ORDER = ["chicken tikka", "crispy chicken"]

ALLOWED_main_typeS = ["pasta", "paneer 65", "rajma chawal", "butter chicken", "chicken curry"]
VEG_MAIN_ORDER = ["pasta", "paneer 65", "rajma chawal"]
MEAT_MAIN_ORDER = ["butter chicken", "chicken curry"]

ALLOWED_dessert_typeS = ["ice-cream", "rasgulla", "rasmalai", "cheesecake", "eclair"]
VEG_DESSERT_ORDER = ["ice-cream", "rasgulla", "rasmalai"]
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
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in VEG_STARTER_ORDER],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_starter_typeS],
            )
        return []

class AskForMainTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_main_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in VEG_MAIN_ORDER],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_main_typeS],
            )
        return []
    
class AskForDessertTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_dessert_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in VEG_DESSERT_ORDER],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of dish do you want?",
                buttons=[{"title": p, "payload": p} for p in ALLOWED_dessert_typeS],
            )
        return []

class ValidateFancyPizzaForm(FormValidationAction):
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
        
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                    text=f"We serve {'/'.join(VEG_STARTER_ORDER)}. What would you like?"
                )
        else:
            dispatcher.utter_message(
                    text=f"We serve {'/'.join(MEAT_STARTER_ORDER)} non veg starters and {'/'.join(VEG_STARTER_ORDER)} veg starters. What would you like?"
                )
            
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
    
    def validate_main_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `main_type` value."""
        print("$$$inside validate main type, slot value is: " , slot_value)
        
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                    text=f"We serve {'/'.join(VEG_MAIN_ORDER)}. What would you like?"
                )
        else:
            dispatcher.utter_message(
                    text=f"We serve {'/'.join(MEAT_MAIN_ORDER)} non veg starters and {'/'.join(VEG_MAIN_ORDER)} veg starters. What would you like?"
                )

        if slot_value not in ALLOWED_main_typeS:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_main_typeS)}."
            )
            return {"main_type": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"I don't recognize that dish. We serve {'/'.join(ALLOWED_main_typeS)}."
            )
            return {"main_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value}.")
        return {"main_type": slot_value}
    
    def validate_dessert_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `dessert_type` value."""
        
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                    text=f"We serve {'/'.join(VEG_DESSERT_ORDER)}. What would you like?"
                )
        else:
            dispatcher.utter_message(
                    text=f"We serve {'/'.join(MEAT_DESSERT_ORDER)} non veg starters and {'/'.join(VEG_DESSERT_ORDER)} veg starters. What would you like?"
                )

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
