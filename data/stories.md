## happy path
* greet
  - utter_intro_buttons
* basic_tax_info_b
  - utter_taxation_details_buttons
* wardtax_based_b
  - action_reset_form_slots
  - action_ward_form
  - form{"name": "action_ward_form"}
  - form{"name": null} 
* ward_yes_b
  - utter_ward_expand_buttons
* ward_building_type_b
  - action_wardbtype_form
  - form{"name": "action_wardbtype_form"}
  - form{"name": null}

# path2
* ward_owner_b
  - action_wardowner_details

# path3
* propidtax_based_b
  - action_propid_form
  - form{"name": "action_propid_form"}
  - form{"name": null}
  
