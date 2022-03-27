from app import *
import pytest

reset_data()

def test_all_epochs():
    assert isinstance(all_epochs(), str) == True

def test_specific_epoch_info():
    assert isinstance(specific_epoch_info('2022-057T12:00:00.000Z'), dict) == True

def test_all_countries():
    assert isinstance(all_countries(), str) == True

def test_specific_country_info():
    assert isinstance(specific_country_info('United_States'), dict) == True

def test_all_regions_in_country():
    assert isinstance(all_regions_in_country('United_States'), str) == True

def test_specific_region_info():
    assert isinstance(specific_region_info('United_States', 'California'), dict) == True

def test_all_cities_in_region():
    assert isinstance(all_cities_in_region('United_States', 'California'), str) == True

def test_specific_city_info():
    assert isinstance(specific_city_info('United_States', 'California', 'Brentwood'), dict) == True
