from fetch_data import fetch_data_from_api


def get_animal_name():
    """prompts user to enter a animal name"""
    animal_name = input("Enter a name of an animal: ")
    return animal_name


def load_html(file_path):
    """loads a html file"""
    with open(file_path, "r") as file:
        return file.read()


def create_error_message(animal_name):
    """takes in an animal name and creates an error message"""
    error_message = (f"\t<li class=\"cards__item\">\n"
                     f"\t\t<p class=\"card__text\"><h3>The animal {animal_name} doesn't exist.</h3>\n</p>\n"
                     f"\t</li>")
    return error_message


def extract_animal_data(animals_data):
    """
    loads a list of dicts from api and returns a string with name, diet, type and location of an Animal
    """
    animals_data_dict = {}

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
    """Gets dictionaries in a dictionary and returns it as html list (str)"""

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


def replace_string(old_string, new_string):
    """
    Loads an HTML page, replaces a specific string (old_string)
    with new_string and returns a new HTML.
    """
    html_temp = load_html("animals_template.html")
    new_html = html_temp.replace(old_string, new_string)
    return new_html


def write_html(old_string, new_string):
    """
    Gets HTML code and writes it to a html file
    """
    new_html = replace_string(old_string, new_string)
    with open("animals.html", "w") as file:
        file.write(new_html)
    print("Website was successfully generated to the file animals.html.")


def main():
    new_string = ""

    # get animal name
    animal_name = get_animal_name()

    # get data from api(fetch animal data from api)
    animals_data = fetch_data_from_api(animal_name)

    #check if list is empty to create
    if not animals_data:
        new_string = create_error_message(animal_name)
    else:
        animals_data_dict = extract_animal_data(animals_data)
        new_string = serialize_animal(animals_data_dict)

    #create/overwrite html
    write_html("__REPLACE_ANIMALS_INFO__", new_string)


if __name__ == "__main__":
    main()
