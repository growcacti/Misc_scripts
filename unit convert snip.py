def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32
volume_conversions = {
    "liters_to_gallons": 0.264172,
    "gallons_to_liters": 1 / 0.264172,
    "milliliters_to_ounces": 0.033814,
    "ounces_to_milliliters": 1 / 0.033814,
    "cubic_meters_to_cubic_feet": 35.3147,
    "cubic_feet_to_cubic_meters": 1 / 35.3147,
}
mass_conversions = {
    "kilograms_to_pounds": 2.20462,
    "pounds_to_kilograms": 1 / 2.20462,
    "grams_to_ounces": 0.035274,
    "ounces_to_grams": 1 / 0.035274,
    "tons_to_kilograms": 907.185,
    "kilograms_to_tons": 1 / 907.185,
}

length_conversions = {
    "meters_to_feet": 3.28084,
    "feet_to_meters": 1 / 3.28084,
    "meters_to_inches": 39.3701,
    "inches_to_meters": 1 / 39.3701,
    "kilometers_to_miles": 0.621371,
    "miles_to_kilometers": 1 / 0.621371,
    "centimeters_to_inches": 0.393701,
    "inches_to_centimeters": 1 / 0.393701,
}

