# monitoring/utils.py

appliance_wattage_dict = {
    "air conditioner": 2000,
    "refrigerator": 150,
    "washing machine": 500,
    "microwave": 1200,
    "television": 100,
    # Add more appliances as needed
}

def get_appliance_wattage(appliance_name):
    return appliance_wattage_dict.get(appliance_name.lower(), None)

