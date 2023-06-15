import json


file = 'spells_tashas'
source_short = 'tashas'
source = "tasha's cauldron of everything"
source_id = 2

# file = 'spells_xanathar'
# source_short = 'xanathar'
# source = "xanathar's guide to everything"
# source_id = 1

# file = 'spells_phb'
# source_short = 'phb'
# source = "player's handbook"
# source_id = 0

with open(f"data_manual/{file}.json", "r") as input:
  as_json = json.load(input)
  for spell in as_json:
    del spell['version']
    del spell['path']
    spell['source_name'] = source
    spell['source_id'] = source_id

    spell_id = spell.get('name')
    spell_id = spell_id.replace("'", "")
    spell_id = spell_id.replace(" ", "_")
    spell['id'] = f"{source_short}_{spell_id}"

    description = spell['description']
    description = f"<p>{description}</p>"
    description = description.replace("\n\n", "</p><p>")
    description = description.replace("At Higher Levels.", "<strong>At Higher Levels.</strong>")
    description = description.replace("At Higher Levels:", "<strong>At Higher Levels.</strong>")
    spell['description'] = description
  
    
  with open(f"data_manual/{file}_scripted.json", "w") as output:
    output.write(json.dumps(as_json))
