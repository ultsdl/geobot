
from typing import Any, Text, Dict, List, Union
from rasa_sdk.forms import FormAction
from rasa_sdk.events import EventType, AllSlotsReset
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from create_query import ward_tax_fetch,building_details,prop_id_fetch

class ResetFormSlots(Action):
    def name(self) -> Text:
        return "action_reset_form_slots"
        
    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


#################################### ward based ###################################################

class ActionWardForm(FormAction):
    def name(self) -> Text:
        return  "action_ward_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["ward_no"]  #order of slots

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return{
                "ward_no":[self.from_text()],
              }

    def submit(self, dispatcher: CollectingDispatcher, 
              tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
            
        try:
            ward_no = tracker.get_slot('ward_no')
            df = ward_tax_fetch(ward_no,sub_type='total_tax')
            total_properties = str(df.shape[0])
            total_tax = str(sum([val for val in df["tax_amnt"] if val!=-1 and val!=-2]))
            ward_name = df['ward_nm'][0]
            message1 = 'We have total of {0} properties in this ward({1}) and the total tax paid is {2}' \
            .format(total_properties,ward_name,total_tax)
            message2 = 'Do you like to know more information?'
            buttons = [
                {"title":"Yes","payload":"/ward_yes_b"},{"title":"No","payload":"/ward_no_b"}
                ]
            message = '{0}\n{1}'.format(message1,message2)
            dispatcher.utter_button_message(message, buttons)
        
        except:
            message = 'Please enter ward number correctly eg: 23'
            dispatcher.utter_message(text=message)

        return []

class ActionWardOwnerProcess(Action):
    def name(self) -> Text:
        return "action_wardowner_details"
    
    def run(self,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ward_no = str(tracker.get_slot('ward_no'))
        try:
            df = ward_tax_fetch(ward_no,sub_type="owner")
            message = "In ward no {0} highest tax is paid by: \n Name: {1}\n House name: {2}\n Location: {3}\n Phone no: {4}\n Building Type: {5}\n Tax: {6}\n" \
            .format(ward_no,df['ownr_nm'][0],df['ownr_house'][0],df['ward_nm'][0], \
             df['ownr_mob'][0],df['bldg_typ'][0],df['tax_amnt'][0])
        
        except:
            message = "Difficult to fetch data. Please try again later"
        
        dispatcher.utter_message(text=message)
        return []

class ActionWardBuildingForm(FormAction):
    def name(self) -> Text:
        return  "action_wardbtype_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["ward_building_type"]  #order of slots

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return{
                "ward_building_type":[self.from_text()],
            
              }

    def submit(self, dispatcher: CollectingDispatcher, 
              tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
            
        ward_no = str(tracker.get_slot('ward_no'))
        prop_type = str(tracker.get_slot('ward_building_type')).upper()
    
        print(prop_type,ward_no)
        try: 
            df = building_details(prop_type,ward_no=ward_no)
            print(df)
            amt = [val for val in df["tax_amnt"] if val!=-1 and val!=-2]
            if len(amt) > 0: 
                tax = sum(amt)
            else:
                tax = 0
            message = "Total tax amount paid by {} category in ward {} is {} RS".format(prop_type.lower(),ward_no, tax)
        except:
            features = "Residential, Commercial, Public, Semi public, educational, religious"
            message = "Please type any of the following available building types: {}".format(features)
        dispatcher.utter_message(text=message)
        return []


################################################prop_id########################################

class ActionPropidForm(FormAction):
    def name(self) -> Text:
        return  "action_propid_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["propid"]  #order of slots

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return{
                "propid":[self.from_text()],
              }

    def submit(self, dispatcher: CollectingDispatcher, 
              tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
            
        try:
            prop_id = tracker.get_slot('propid')
            df = prop_id_fetch(prop_id)
            print(df)
            message = "Property {0} belongs to: \n Name: {1}\n House name: {2}\n Location: {3}\n Phone no: {4}\n Building Type: {5}\n Tax: {6}\n" \
            .format(prop_id,df['ownr_nm'][0],df['ownr_house'][0],df['ward_nm'][0], \
             df['ownr_mob'][0],df['bldg_typ'][0],df['tax_amnt'][0])
            
            dispatcher.utter_message(text=message)
        
        except:
            message = 'Please enter property id correctly'
            dispatcher.utter_message(text=message)

        return []

################################################################################################