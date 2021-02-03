import pandas as pd 
from connect import execute_querry


def prop_id_fetch(prop_id):
    q = f"select ownr_nm,ward_nm,bldg_typ,ownr_mob,ownr_house,tax_amnt from knr_full_assets where prop_id = '{prop_id}'"
    q = execute_querry(q)
    return q


def ward_tax_fetch(ward_no,sub_type='total_tax'):
    if sub_type == 'owner':
        q = f"select ownr_nm,ward_nm,bldg_typ,ownr_mob,ownr_house,tax_amnt from knr_full_assets where ward_no = '{ward_no}' order by tax_amnt DESC limit 1"
    elif sub_type == 'total_tax':
        q = f"select ward_no,ward_nm,tax_amnt from knr_full_assets where ward_no = '{ward_no}'"
    q = execute_querry(q)
    return q

def building_details(building_type, ward_no=None):
    if ward_no is None:
        q =  "SELECT tax_amnt from knr_full_assets WHERE bldg_typ ='{}'".format(building_type)
    else:
        q = "SELECT tax_amnt from knr_full_assets WHERE (bldg_typ ='{}' AND ward_no = '{}')".format(building_type, ward_no)
    q = execute_querry(q)
    return q




