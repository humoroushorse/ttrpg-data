import json

book = 'phb'
attribute = 'components' # e.g. school, range

spell_json = f"data_final/spells_{book}.json"

spells = []

unique = []

with open(spell_json, "r") as input:
  spells = json.load(input)
  assert len(spells) > 0, "expected spells"

longest_len = (0, '')
for spell in spells:
  spell_attr = spell.get(attribute)
  if longest_len[0] < len(spell_attr):
    longest_len = (len(spell_attr), spell.get('name'))
  if spell_attr not in unique:
    unique.append(spell_attr)

print("longest= ", longest_len)

# print(f"Found {len(unique)} unique attributes")
# for u in unique:
#   u_key = u.upper().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
#   print(f"{u_key} = \"{u}\"")