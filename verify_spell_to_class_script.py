import json
from pydoc import classname

book = 'tashas'

spell_to_class_json = f'data_final/spell_to_class_{book}.json'
class_json = 'data_final/class.json'
spell_json = f"data_final/spells_{book}.json"

spells = []
classes = []
classes_names = []
spells_to_classes = []

first_spell_name = '' # off by one troubleshooting or something

errors = []

with open(spell_json, "r") as input:
  spells = json.load(input)
  assert len(spells) > 0, "expected spells"
  first_spell_name = spells[0].get('name')

with open(class_json, "r") as input:
  classes = json.load(input)
  classes_names = [c.get('name') for c in classes]
  assert len(classes) > 0, "expected classes"


with open(spell_to_class_json, "r") as input:
  spells_to_classes = json.load(input)
  assert len(spells_to_classes) > 0, "expected spell_to_class"


for s2c in spells_to_classes:
  s2c_spell_dict = s2c.get('spells')
  s2c_class_name = s2c.get('class_name')
  if s2c_class_name not in classes_names:
    errors.append(f"Class '{s2c_class_name}' does not appear to exist.")
  else:
    for c in classes:
      if c.get('name') == s2c_class_name:
        if c.get('id') != s2c.get('class_id'):
          errors.append(f"Class id '{s2c.get('class_id')}' does not match expected id of '{c.get('id')}' for class {s2c_class_name} ")
  for s2c_spell_level, s2c_spells in s2c_spell_dict.items():
    for s2c_spell in s2c_spells:
      expected_spell = next((index for (index, s) in enumerate(spells) if s.get('name') == s2c_spell), None)
      # TODO: figure out the acid splash issue (because it's the first spell?)
      if not expected_spell and s2c_spell != first_spell_name:
        errors.append(f"Spell: '{s2c_spell}' does not appear to exist! class='{s2c_class_name}', level='{s2c_spell_level}'")



if not len(errors):
  print("No errors found!")
else:
  print("Errors found!")
  print(f"Spell file: {spell_json}")
  print(f"Class file: {class_json}")
  print(f"Spell to class file: {spell_to_class_json}")
  for e in errors:
    print(f"\t{e}")
