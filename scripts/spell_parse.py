import json
from itertools import groupby
from operator import itemgetter
from datetime import datetime

file = 'spells_tashas'

with open(f"data_raw/{file}.json", "r") as input:
  as_json = json.load(input)
  
  as_list = [json.loads(v) for _, v in as_json.items()]

  # IF JSON STRING
  first_element = as_list[0]
  if type(first_element) is str:
    as_list = [json.loads(v) for v in as_list]

  # well one of those items is actually a list
  as_list_dicts = [item for item in as_list if type(item) is dict]
  # this should be our one non-dict
  as_list_non_dicts = [item for item in as_list if type(item) is not dict]

  grouped_dict = {}
  datetime_now = f"{datetime.now()}"
  for d in as_list_dicts:
    d = {
      'id': d.get('Id').lower(),
      'version': d.get('Version'),
      'name': d.get('Name').lower(),
      'path': d.get('Path') if d.get('Path') else None,
      'source': d.get('Source') if d.get('Source') else None,
      'source_id': -1, # TODO: id based on source for links
      'casting_time': d.get('CastingTime'),
      'classes': [c.lower() for c in d.get('Classes', [])],
      'components': d.get('Components', '').lower(),
      'description': d.get('Description'),
      'duration': d.get('Duration', '').lower(),
      'level': d.get('Level'),
      'range': d.get('Range', '').lower(),
      'ritual': d.get('Ritual'),
      'school': d.get('School', '').lower(),
      'last_updated': datetime_now,
      'created_at': datetime_now,
      'created_by': 'admin:system',
      'updated_by': 'admin:system',
      'homebrew': False,
    }
    source = d.get('source')
    level = d.get('level')
    if type(level) is str:
      level = int(level)
    if source not in grouped_dict.keys():
      grouped_dict[source] = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: []
      }
      grouped_dict[source][level] = [d]
    elif level not in grouped_dict[source].keys():
      grouped_dict[source][level] = [d]
    else:
      grouped_dict[source][level].append(d)  
  for key, value in grouped_dict.items():
    print(key if key else '>>>>>> NO NAME <<<<<<')
    for k, v in value.items():
      # print(f"\t{k}: {len(v)}")
      grouped_dict[key][k] = sorted(v, key=lambda x: x.get('name'))
    
with open(f"data_parsed/{file}.json", "w") as output:
  output.write(json.dumps(grouped_dict))
