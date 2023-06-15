import json

book = 'monsters_monster_manual'
attribute = 'speed' # e.g. school, range
interface_format = False

# items_json = f"data_parsed/{book}.json"
items_json = f"data_manual/{book}_scripted.json"

items = []

unique = []

with open(items_json, "r") as input:
  items = json.load(input)
  assert len(items) > 0, "expected items"

for item in items:
  item_attr = item.get(attribute)
  # is list
  if type(item_attr) is list:
    # for item_attr_item in item_attr:
    #   if item_attr_item not in unique:
    #     unique.append(item_attr_item)
    if f"{item_attr}" not in unique:
      unique.append(f"{item_attr}")
  # not list
  else:
    if item_attr not in unique:
      unique.append(item_attr)

print(f"Found {len(unique)} unique attributes")
for u in sorted([v if v else 'null' for v in unique]):
  if interface_format:
    u_key = u.upper().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
    print(f"{u_key} = \"{u}\"")
  else:
    print(u)