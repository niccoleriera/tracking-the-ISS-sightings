from flask  import Flask
import xmltodict 
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

iss_epoch_data = {}
iss_sighting_data = {}

@app.route('/', methods= ['GET'])
def app_information():
    """
    ### ISS Tracker ###
    
    Informational and management routes: 

    /                                                    (GET) print this information
    /reset                                               (POST) reset data, load from file

    Routes for querying positional and velocity data:

    /epochs                                              (GET) list all epochs
    /epochs/<epoch>                                      (GET) info on a specific epoch


    Routes for querying sighting data:
    
    /countries                                           (GET) List of all countries
    /countries/<country>                                 (GET) All data associated with <country>
    /countries/<country>/regions                         (GET) List of all regions ina given country
    /countries/<country>/regions/<region>                (GET) All data associated with <region>
    /countries/<country>/regions/<region>/cities         (GET) List of all cities in a given region
    /countries/<country>/regions/<region>/cities/<city>  (GET) All data associated with <city>
    """
    logging.info("Printing information on how to use this application.")
    return(app_information.__doc__)

@app.route('/reset', methods= ['POST'])
def reset_data():
    """
    This function reads ISS data from XML to a dictionary and stores it as a variable for each data set.

    Returns:
        A string that states that the Data has been read from the file.
    """
    logging.info("Reading the data.")
    global iss_epoch_data
    global iss_sighting_data

    with open('ISS.OEM_J2K_EPH.xml', 'r') as f:
        iss_epoch_data = xmltodict.parse(f.read())
    
    with open('XMLsightingData_citiesUSA01.xml', 'r') as f:
        iss_sighting_data = xmltodict.parse(f.read())

    return f'Data has been read from file\n'

@app.route('/epochs', methods= ['GET'])
def all_epochs() -> str:
    """
    This function loops through every dictionary in the epoch data list, finds the value for 'EPOCH', and adds the value to a list.

    Returns:
        A string with all of the epochs found in the epochs data set.
    """
    logging.info("Printing all epochs in the data.")
    epoch_data_list = iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector']
    epochs_final_list = []
    for i in range(len(epoch_data_list)):
        epochs_final_list.append(epoch_data_list[i]['EPOCH'])
    return('\n'.join(epochs_final_list) + '\n')

@app.route('/epochs/<epoch>', methods= ['GET'])
def specific_epoch_info(epoch: str) -> dict:
    """
    This function loops through every dictionary in the epoch data list and looks for when the value for 'EPOCH' is the same as the epoch given in the argument.

    Args:
        epoch (str): An epoch string
    
    Returns:
        epoch_data_list[i] (dict): The dictionary with information on the epoch specified. 
    """
    logging.info("Printing data on the epoch specified.")
    epoch_data_list = iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector']
    for i in range(len(epoch_data_list)):
        if (epoch_data_list[i]['EPOCH'] == epoch):
            return(epoch_data_list[i])

@app.route('/countries', methods= ['GET'])
def all_countries() -> str:
    """
    This function loops through every dictionary in the sighting data list, finds the value for 'country', and adds the value to a list.

    Returns:
        A string with all the countries where there were ISS sightings.
    """
    logging.info("Printing all countries in the data.")
    sighting_data_list = iss_sighting_data['visible_passes']['visible_pass']
    sightings_final_list = []
    for i in range(len(sighting_data_list)):
        sightings_final_list.append(sighting_data_list[i]['country'])
    sightings_final_list = list(set(sightings_final_list))
    return('\n'.join(sightings_final_list) + '\n')

@app.route('/countries/<country>', methods=['GET'])
def specific_country_info(country: str) -> dict:
    """
    This function loops through every dictionary in the sighting data list and looks for when the value for 'country' is the same as the country given in the argument.

    Args:
        country (str): A country string

    Returns:
        country_dict (dict): A dictionary that contains a list of all the dictionaries that reference a specific country.
    """
    logging.info("Printing all data on the country specified.")
    sighting_data_list = iss_sighting_data['visible_passes']['visible_pass']
    country_dict = {}
    country_dict[country] = []
    for i in range(len(sighting_data_list)):
        if (sighting_data_list[i]['country'] == country):
            country_dict[country].append(sighting_data_list[i])
    return country_dict

@app.route('/countries/<country>/regions', methods=['GET'])
def all_regions_in_country(country: str) -> str:
    """
    This function loops through every dictionary in the sighting data list, looks for when the value for 'country' is the same as the country given in the argument, finds the value for 'region', and adds it to a list.

    Args:
        country (str): A country string

    Returns:
        A string with all of the regions in a specified country.
    """
    logging.info("Printing all regions in a country specified.")
    sighting_data_list = iss_sighting_data['visible_passes']['visible_pass']
    regions_list = []
    for i in range(len(sighting_data_list)):
        if (sighting_data_list[i]['country'] == country):
            regions_list.append(sighting_data_list[i]['region'])
    regions_list = list(set(regions_list))
    return ('\n'.join(regions_list) + '\n')
                    
@app.route('/countries/<country>/regions/<region>', methods=['GET'])
def specific_region_info(country: str, region: str) -> dict:
    """
    This function loops through every dictionary in the sighting data list, looks for when the value for 'country' and 'region' is the same as the country and region given in the argument, and adds all the dictionaries that mention that region to a list of dictionaries.

    Args:
        country (str): A country string
        region (str): A region string

    Returns:
        region_dict (dict): A list of dictionaries mentioning a specific region
    """
    logging.info("Printing all  data on the region specified.")
    sighting_data_list = iss_sighting_data['visible_passes']['visible_pass']
    region_dict = {}
    region_dict[region] = []
    for i in range(len(sighting_data_list)):
        if ( (sighting_data_list[i]['country'] == country) and (sighting_data_list[i]['region'] == region)):
            region_dict[region].append(sighting_data_list[i])
    return region_dict

@app.route('/countries/<country>/regions/<region>/cities', methods=['GET'])
def all_cities_in_region(country: str, region: str) -> str:
    """
    This function loops through every dictionary in the sighting data list, looks for when the value for 'country' and 'region' is the same as the country and region given in the argument, and adds the value for 'city' to a list.

    Args:
        country (str): A country string
        region (str): A region string
    
    Returns:
        A string with all the cities in a specified region and country.
    """
    logging.info("Printing all cities in a specific region and country.")
    sighting_data_list = iss_sighting_data['visible_passes']['visible_pass']
    cities_list = []
    for i in range(len(sighting_data_list)):
        if ( (sighting_data_list[i]['country'] == country) and (sighting_data_list[i]['region'] == region)):
            cities_list.append(sighting_data_list[i]['city'])
    cities_list = list(set(cities_list))
    return ('\n'.join(cities_list) + '\n')

@app.route('/countries/<country>/regions/<region>/cities/<city>', methods=['GET'])
def specific_city_info(country: str, region: str, city: str) -> dict:
    """
    This function loops through every dictionary in the sighting data list, looks for when the value for 'country','region', and 'city' is the same as the country, region, and city given in the argument, and adds all the dictionaries that mention that city to a list of dictionaries.

    Args:
        country (str): A country string
        region (str): A region string
        city (str): A city string

    Returns:
        city_dict (dict): A dictionary with a list of dictionaries that mention a specific city in a region and country.
    """
    logging.info("Printing all data on a specific city.")
    sighting_data_list = iss_sighting_data['visible_passes']['visible_pass']
    city_dict = {}
    city_dict[city] = []
    for i in range(len(sighting_data_list)):
        if ( (sighting_data_list[i]['country'] == country) and (sighting_data_list[i]['region'] == region) and (sighting_data_list[i]['city'] == city) ):
            city_dict[city].append(sighting_data_list[i])
    return city_dict


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

