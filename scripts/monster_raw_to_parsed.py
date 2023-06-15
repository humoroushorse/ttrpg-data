import json
from itertools import groupby
from operator import itemgetter
from datetime import datetime
import os
from collections import OrderedDict

file = 'monsters_monster_manual'

with open(f"data_raw/{file}.json", "r") as input:
  as_json = json.load(input)
  
  as_list = [v for _, v in as_json.items()][1:] # skip first item (it's a list of moster names)

  # IF JSON STRING
  first_element = as_list[0]
  if type(first_element) is str:
    as_list = [json.loads(v) for v in as_list]

  # well one of those items is actually a list
  as_list_dicts = [item for item in as_list if type(item) is dict]
  # this should be our one non-dict
  as_list_non_dicts = [item for item in as_list if type(item) is not dict]

  def format_to_dict(arr: list, k: str, v: str) -> dict:
    new_dict = {}
    for item in arr:
      key = item[k].lower()
      key = key.replace('�', '-') # else you will get \ufffd for one value
      value = item[v]
      if type(value) is str:
        value = value.replace('\u2019', '\'').replace('\u2014', '-')
      new_dict[key] = value

    return OrderedDict(sorted(new_dict.items()))

  def rename_saves(d: dict) -> dict:
    ret = {}
    if d.get('str'):
      ret['strength'] = d.get('str')
    if d.get('dex'):
      ret['dexterity'] = d.get('dex')
    if d.get('con'):
      ret['constitution'] = d.get('con')
    if d.get('int'):
      ret['intelligence'] = d.get('int')
    if d.get('wis'):
      ret['wisdom'] = d.get('wis')
    if d.get('cha'):
      ret['charisma'] = d.get('cha')
    return ret

  grouped_dict = []
  datetime_now = f"{datetime.now()}"
  for d in as_list_dicts:
    monster_type = d.get('Type').lower()
    creature_comma_split = monster_type.split(',')
    creature_alignment = creature_comma_split[-1].strip()
    creature_space_strip = creature_comma_split[0].split(' ')
    creature_size = creature_space_strip[0]
    if len(creature_size) == 1:
      creature_size = {
        't': 'tiny',
        's': 'small',
        'm': 'medium',
        'l': 'large',
        'h': 'huge',
        'g': 'gargantuan'
      }[creature_size]
    creature_type_full = ' '.join(creature_space_strip[1:])
    creature_type = creature_type_full
    creature_subtype = None
    if creature_type_full == "swarm of tiny beasts":
      creature_type = 'beast'
      creature_subtype = creature_type_full
    else: 
      creature_type_split = creature_type_full.split(' ')
      if len(creature_type_split) > 1:
        creature_type = creature_type_split[0]
        creature_subtype = " ".join(creature_type_split[1:]).replace('(', '').replace(')', '')
    
    d = {
      'id': d.get('Id').lower(),
      'name': d.get('Name').lower(),
      # 'path': d.get('Path') if d.get('Path') else None, # only one record uses path
      'source': d.get('Source').lower() if d.get('Source') else None,
      # 'size_type_alignment': monster_type,
      'alignment': creature_alignment,
      'size': creature_size,
      'type': creature_type,
      'type_notes': creature_subtype,
      'hp_value': d.get('HP').get('Value'),
      'hp_notes': d.get('HP').get('Notes').replace('(', '').replace(')', ''),
      'ac_value': d.get('AC').get('Value'),
      'ac_notes': d.get('AC').get('Notes'),
      'initiative_modifier': d.get('InitiativeModifier'),
      'initiative_advantage': d.get('InitiativeAdvantage'),
      'speed': [v.lower() for v in d.get('Speed')],
      'ability_scores': {
        'strength': d.get('Abilities').get('Str'),
        'dexterity': d.get('Abilities').get('Dex'),
        'constitution': d.get('Abilities').get('Con'),
        'intelligence': d.get('Abilities').get('Int'),
        'wisdom': d.get('Abilities').get('Wis'),
        'charisma': d.get('Abilities').get('Cha'),
      },
      'damage_vulnerabilities': [v.lower() for v in d.get('DamageVulnerabilities')],
      'damage_resistances': [v.lower() for v in d.get('DamageResistances')],
      'damage_immunities': [v.lower() for v in d.get('DamageImmunities')],
      'condition_immunities': [v.lower() for v in d.get('ConditionImmunities')],
      'saves': rename_saves(format_to_dict(d.get('Saves'), 'Name', 'Modifier')),
      'skills': format_to_dict(d.get('Skills'), 'Name', 'Modifier'),
      'senses': [v.lower() for v in d.get('Senses')],
      'languages': [v.lower() for v in d.get('Languages')],
      'challenge': d.get('Challenge').lower(),
      'traits': format_to_dict(d.get('Traits'), 'Name', 'Content'),
      'actions': format_to_dict(d.get('Actions'), 'Name', 'Content'),
      'reactions': format_to_dict(d.get('Reactions'), 'Name', 'Content'),
      'legendary_actions': format_to_dict(d.get('LegendaryActions'), 'Name', 'Content'),
      'description': None, # d.get('Description'), # All are empty strings
      # 'player': d.get('Player').lower(), # All are empty strings
      # 'version': d.get('Version').lower(),
      'version': 1,
      'image_url': None, # d.get('ImageURL').lower(), # All are empty strings
      'updated_at': datetime_now,
      'created_at': datetime_now,
      'created_by': 'admin:system',
      'updated_by': 'admin:system',
      'homebrew': False,
    }
    grouped_dict.append(d)
    
with open(f"data_parsed/{file}.json", "w") as output:
  output.write(json.dumps(grouped_dict))
