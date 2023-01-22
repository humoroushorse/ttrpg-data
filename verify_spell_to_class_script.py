import json
from pydoc import classname

book = 'tashas'

spell_to_class_json = f'data_final/spell_to_class_{book}.json'
class_json = 'data_final/class.json'

classes = []
classes_names = []
spells_to_classes = []

errors = []

def load_spells(spell_file_name): 
  with open(spell_file_name, "r") as input:
    spell_list = json.load(input)
    assert len(spell_list) > 0, "expected spells"
    first_spell_name = spell_list[0].get('name')
    return spell_list, first_spell_name

spells_tashas, first_spell_name_tashas = load_spells("data_final/spells_tashas.json")
spells_xanathar, first_spell_name_xanathar = load_spells("data_final/spells_xanathars.json")
spells_phb, first_spell_name_phb = load_spells("data_final/spells_phb.json")

with open(class_json, "r") as input:
  classes = json.load(input)
  classes_names = [c.get('name') for c in classes]
  assert len(classes) > 0, "expected classes"

with open(spell_to_class_json, "r") as input:
  spells_to_classes = json.load(input)
  assert len(spells_to_classes) > 0, "expected spell_to_class"

def verify_spell_list(source_id: int):
  spell_list = []
  first_spell = ""
  if source_id == 0:
    spell_list = [*spells_phb]
    first_spell = first_spell_name_phb
  if source_id == 1:
    spell_list = [*spells_xanathar]
    first_spell = first_spell_name_xanathar
  if source_id == 2:
    spell_list = [*spells_tashas]
    first_spell = first_spell_name_tashas
  for s2c_spell in s2c_spells:
    expected_spell = next((index for (index, s) in enumerate(spell_list) if s.get('name') == s2c_spell), None)
    # TODO: figure out the acid splash issue (because it's the first spell?)
    if not expected_spell and s2c_spell != first_spell:
      errors.append(f"Spell: '{s2c_spell}' does not appear to exist! source_id='{source_id}', class='{s2c_class_name}', level='{s2c_spell_level}'")

for s2c in spells_to_classes:
  s2c_spell_dict = s2c.get('spells')
  s2c_class_name = s2c.get('class_name')
  st2_source_id = s2c.get('source_id')
  if s2c_class_name not in classes_names:
    errors.append(f"Class '{s2c_class_name}' does not appear to exist.")
  else:
    for c in classes:
      if c.get('name') == s2c_class_name:
        if c.get('id') != s2c.get('class_id'):
          errors.append(f"Class id '{s2c.get('class_id')}' does not match expected id of '{c.get('id')}' for class {s2c_class_name} ")
  for s2c_spell_level, s2c_spells in s2c_spell_dict.items():
    verify_spell_list(st2_source_id)



if not len(errors):
  print("No errors found!")
else:
  print("Errors found!")
  print(f"Class file: {class_json}")
  print(f"Spell to class file: {spell_to_class_json}")
  for e in errors:
    print(f"\t{e}")
