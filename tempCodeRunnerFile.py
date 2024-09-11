import os
import json

# get the names of all pokemon that spawn in the wild
spawn_filenames = os.listdir(os.path.join("cobblemon", "spawn_pool_world"))
json_names = [spawn_file.split("_")[1] for spawn_file in spawn_filenames]
print(json_names)

# find each pokemon in the species folder & include 1 entry per form.

for json_name in json_names:
    1
    
with open("cobblemon/species/generation1/meowth.json") as j:
    meowth = json.load(j)

with open("cobblemon/species/generation1/aerodactyl.json") as j:
    aerodactyl = json.load(j)
    
def get_nr_of_forms(pokeJson) -> int:
    # generate docstring by typing """
    if "forms" in pokeJson:
        return len(pokeJson["forms"]) + 1
    return 1

print(get_nr_of_forms(meowth))
print(get_nr_of_forms(aerodactyl))