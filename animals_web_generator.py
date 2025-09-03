import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
API_URL = "https://api.api-ninjas.com/v1/animals?"


def load_data_from_api():
    """
    prompt user to enter a name of an animal
    sends a query to animal api get json
    returns list of dicts from api
    """
    animal = input("Enter a name of an animal: ")
    response = requests.get(API_URL, params={"name": animal}, headers={"X-Api-Key": api_key})
    response = response.json()

    if not response:
        return (f"\t<li class=\"cards__item\">\n"
                f"\t\t<p class=\"card__text\"><h2>The animal {animal} doesn't exist.</h2>\n</p>\n"
                f"\t</li>")
    else:
        return response


def load_html(file_path):
    """loads a html file"""
    with open(file_path, "r") as file:
        return file.read()


def get_data():
    """
    loads a list of dicts from api and returns a string with name, diet, type and location of an Animal
    """
    animals_data_dict = {}
    animals_data = load_data_from_api()

    if isinstance(animals_data, str):
        return animals_data

    for animal in animals_data:
        # get data from dictionary
        name = animal.get("name")
        sci_name = animal.get("taxonomy", {}).get("scientific_name") # Bonus Task 1
        diet = animal.get("characteristics", {}).get("diet")
        animal_type = animal.get("characteristics", {}).get("type")
        location = animal.get("locations")[0] #join location list to a string

        animals_data_dict.setdefault(name, {})
        animals_data_dict[name].setdefault("Scientific Name", sci_name) # Bonus Task 1
        animals_data_dict[name].setdefault("Diet", diet)
        animals_data_dict[name].setdefault("Location", location)
        animals_data_dict[name].setdefault("Type", animal_type)
    return animals_data_dict


def serialize_animal(animal_dict):
    """Gets an dictionaries in a dictionary and returns it as html list"""

    if isinstance(animal_dict, str):
        return animal_dict

    output = ""
    for animal, data in animal_dict.items():
        output += "<li class=\"cards__item\">\n"
        output += (f"\t<div class=\"card__title\">{animal}</div>\n"
                   f"\t<p class=\"card__text\">\n"
                   f"\t\t<ul>\n")

        for info, detail in data.items():
            if detail is not None:
                output += f"\t\t\t<li><strong>{info}</strong>: {detail}</li>\n"
        output += ("\t\t</ul>\n"
                   "\t</p>\n"
                   "</li>\n")
    return output


def replace_string(old_string):
    """
    Loads an HTML page, gets data from json, replaces a specific string (old_string)
    with the data from json (new_string) and returns a new HTML.
    :param old_string:
    :return new_html:
    """
    new_string = serialize_animal(get_data())
    html_temp = load_html("animals_template.html")
    new_html = html_temp.replace(old_string, new_string)
    return new_html


def write_html(old_string):
    """
    Gets HTML code and writes it to a html file
    :param old_string:
    """
    new_html = replace_string(old_string)
    with open("animals.html", "w") as file:
        file.write(new_html)
    print("Website was successfully generated to the file animals.html.")

# call function an (over)write html
write_html("__REPLACE_ANIMALS_INFO__")
