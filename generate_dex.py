import os
import json


def get_occuring_pokemon(spawn_pool_world_location) -> list:
    # get the names of all pokemon that spawn in the wild
    spawn_filenames = os.listdir(spawn_pool_world_location)
    poke_filenames = [spawn_file.split("_")[1].replace(".json", "") for spawn_file in spawn_filenames]
    return poke_filenames

def fix_names(poke_names) -> list:
    # generate docstring by typing """
    rename_dict = {
        "nidoranf" : "nidoran-f", 
        "nidoranm" : "nidoran-m", 
        "mrmime" : "mr-mime", 
        "mimejr" : "mime-jr", 
        "porygonz" : "porygon-z",
        "jangmoo" : "jangmo-o", 
        "hakamoo" : "hakamo-o",
        "kommoo" : "kommo-o"
    }
    return [rename_dict.get(poke_name, poke_name) for poke_name in poke_names]

def get_evolution_ids(poke_name, species_json) -> list:
    # generate docstring by typing """
    if not("evolution_ids" in species_json[poke_name]):
        return []
    return species_json[poke_name]["evolution_ids"]
    
def generate_dex(poke_names, poke_filepath) -> dict:
    # generate docstring by typing """
    
    # get species json
    # Read the JS file and remove the `export default` part
    with open(os.path.join(poke_filepath, "pokemon.js"), "r") as file:
        js_content = file.read().replace("export default ", "").replace(";", "")
        species_json = json.loads(js_content)
        
    # find each pokemon name in the filepaths & include 1 entry per form.
    poke_names = list(reversed(poke_names))
    species_keys = species_json.keys()
    
    # initialize dex
    dex_order = {}
    
    # iterate over all pokemon and add them to the dex
    while len(poke_names) > 0:
        poke_name = poke_names.pop()
        # check if poke name is in species if not raise error
        if not(poke_name in species_keys):
            raise ValueError(poke_name + " needs to be edited")
        forms_keys = list(reversed([poke_name] + [form for form in species_keys if poke_name + "-" in form]))
        print(forms_keys)
        
        # per form, add the form and its evolutions to the dex. exception for gmax forms.
        while len(forms_keys) > 0:
            key = forms_keys.pop()
            if "-gmax" in key: 
                continue
            # check if form is already in it. if not, add to dex
            if not([[species_json[key]["base_id"],species_json[key]["form_id"] ]] in dex_order.values()):
                dex_order[str(len(dex_order) + 1)] = [[species_json[key]["base_id"],species_json[key]["form_id"] ]]
            for evo_id in get_evolution_ids(key, species_json):
                dex_order[str(len(dex_order) + 1)] = [evo_id]
            
    dex = {
        "cobblemon" : 
            {
                "name": "Cobblemon", 
                "order": dex_order
            }
    }
    
    return dex



## executing code

def main():
    poke_names = get_occuring_pokemon(os.path.join("cobblemon", "spawn_pool_world"))
    poke_names = fix_names(poke_names)
    dex = generate_dex(poke_names, os.path.join("static", "js"))

    # Save the result to a file
    with open('cobblemon_dict.json', 'w', encoding='utf-8') as f:
        json.dump(dex, f, ensure_ascii=False, indent=4)
    
    
if __name__ == "__main__":
    main()