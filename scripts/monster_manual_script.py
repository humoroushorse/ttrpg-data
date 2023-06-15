import json
from typing import Tuple

file = 'monsters_monster_manual'
source_short = 'monster_manual'
source = "monster manual"
source_id = 3

with open(f"data_manual/{file}.json", "r") as input:
  as_json = json.load(input)
  for monster in as_json:
    monster['source_name'] = source
    monster['source_id'] = source_id

    monster_id = monster.get('name')
    monster_id = monster_id.replace("'", "")
    monster_id = monster_id.replace(" ", "_")
    monster['id'] = f"{source_short}_{monster_id}"


    def format_for_html(text: str) -> str:
      formatted = f"<p>{text}</p>"
      formatted = formatted.replace('\n\n', '</p> <br /> <p>')
      formatted = formatted.replace('\n', '</p> <p>')
      return formatted

    def format_dict_for_html(d: dict) -> dict:
      for key, value in d.items():
          d[key] = format_for_html(value)

    format_dict_for_html(monster['traits'])
    format_dict_for_html(monster['actions'])
    format_dict_for_html(monster['reactions'])
    format_dict_for_html(monster['legendary_actions'])

    def format_speed(speed: list) -> Tuple[list, list]:
      speed_as_string = f"{speed}"
      tags = []
      # if speed > 0 and is not special
      if speed[0] != '0 ft.' and 'burrow' not in speed[0] and 'climb' not in speed[0] and 'fly' not in speed[0] and 'swim' not in speed[0]:
        tags.append('walk')
      if 'burrow' in speed_as_string:
        tags.append('burrow')
      if 'climb' in speed_as_string:
        tags.append('climb')
      if 'fly' in speed_as_string:
        tags.append('fly')
      if 'swim' in speed_as_string:
        tags.append('swim')

      formatted = []
      # fix one data point
      if "30 ft. when rolling" in speed_as_string:
        speed = [f"{speed[0]}, {speed[1]}"]
      for s in speed:
        s = s.replace('it can hover.', '(hover)')
        s = s.replace('ft', 'ft.').replace('ft..', 'ft.')
        formatted.append(s)
      return formatted, tags
    
    speed, speed_tags = format_speed(monster['speed'])
    monster['speed'] = speed
    monster['speed_tags'] = speed_tags
    
  with open(f"data_manual/{file}_scripted.json", "w") as output:
    output.write(json.dumps(as_json))