import json
import os
import random


def add_priority_to_orders(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(input_folder, filename)

            # Load the JSON data
            with open(file_path, "r") as file:
                data = json.load(file)

            # Add priority to each order
            for order in data["orders"]:
                order["priority"] = random.randint(1, 3)

            # Save the updated JSON data to the output folder
            output_path = os.path.join(output_folder, filename)
            with open(output_path, "w") as file:
                json.dump(data, file, indent=4)


# Specify the input and output folders
input_folder = "./json_files"
output_folder = "./priority_jsons"

# Run the function
add_priority_to_orders(input_folder, output_folder)
