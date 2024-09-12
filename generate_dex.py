import os
import json


def get_occuring_pokemon(spawn_pool_world_location) -> list:
    # get the names of all pokemon that spawn in the wild
    spawn_filenames = sorted(os.listdir(spawn_pool_world_location))
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

def insert_missing(forms_keys) -> list:
    # generate docstring by typing """
    return forms_keys

def is_exception(poke_name) -> bool:
    # generate docstring by typing """
    if "-gmax" in poke_name:
        return True
    
    exceptions = [
        "sandshrew-alola", 
        "sandslash-alola", 
        "growlithe-hisui",
        "arcanine-hisui", 
        "geodude-alola", 
        "graveler-alola", 
        "golem-alola", 
        "slowpoke-galar", 
        "slowbro-galar", 
        "slowking-galar", 
        "grimer-alola", 
        "muk-alola", 
        "weezing-galar", 
        "mr-mime-galar",
        "mr-rime", 
        "tauros-paldea-combat",
        "tauros-paldea-blaze",
        "tauros-paldea-aqua",
        "darumaka-galar", 
        "darmanitan-galar", 
        "yamask-galar", 
        "runerigus", 
        "avalugg-hisui", 
        "heracross-mega", 
        "sceptile-mega", 
        "blaziken-mega", 
        "swampert-mega", 
        "aggron-mega", 
        "camerupt-mega", 
        "metagross-mega", 
        "lopunny-mega", 
        "lucario-mega"
    ]
    
    if poke_name in exceptions:
        return True
    return False

def poke_name_by_id(base_id, form_id, species_json) -> str:
    # generate docstring by typing """
    for name, ids in species_json.items():
        if ids["base_id"] == base_id and ids["form_id"] == form_id:
            return name
    return None  # if no match is found

def get_evolution_names(poke_name, species_json) -> list:
    # generate docstring by typing """
    if not("evolution_ids" in species_json[poke_name]):
        return []
    return [poke_name_by_id(evo_id, evo_form_id, species_json) for evo_id, evo_form_id in species_json[poke_name]["evolution_ids"]]
    
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
        forms_keys = insert_missing(forms_keys)
        
        #print(forms_keys)
        
        # per form, add the form and its evolutions to the dex. exception for gmax forms.
        while len(forms_keys) > 0:
            key = forms_keys.pop()
            # check if form is already in it. if not, add to dex
            if not([[species_json[key]["base_id"],species_json[key]["form_id"] ]] in dex_order.values()): # do not include if pokemon is already in dex
                if not(is_exception(key)):
                    dex_order[str(len(dex_order) + 1)] = [[species_json[key]["base_id"],species_json[key]["form_id"] ]]
            # add evolutions to front of dex so they are done immediately
            evo_names = list(reversed(get_evolution_names(key, species_json)))
            for evo_name in evo_names:
                forms_keys.append(evo_name)
            
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
        json.dump(dex, f)
    
    
if __name__ == "__main__":
    main()