import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union

from actions import Action
from images import Img, MatchingResult

BASE_PATH = Path(__file__).parent

class CityManager:

    match_map_templates : Dict[str, Dict[str, Dict[str, Union[Img, str, Path]]] ]= {
        "25" : {},
        "50": {},
        "75": {},
        "150": {},
        "250": {},
    }

    def load_cities(self):
        def cvt(data):
            x, y = data['xy']
            w, h = data['size']
            return (x, y, x+w, y+h)

        for max_level in self.match_map_templates.keys():
            base_path = BASE_PATH / "images" / "maps" / max_level

            for city_path in base_path.iterdir():
                match_map_png = city_path / "template" / "match_map.png"
                match_map_json = city_path / "template" / "match_map.json"
                factory_json =  city_path / "template" / "factory.json"
                prefix = f'{int(max_level):03d}_'

                if not city_path.name.startswith(prefix): continue
                if not match_map_png.exists(): continue
                if not match_map_json.exists(): continue

                name = city_path.name.replace(prefix, '')

                factory_data = json.loads(factory_json.read_text())
                factory_data = sorted(factory_data, key=lambda o: o['index'])

                if name not in self.match_map_templates[max_level]:

                    self.match_map_templates[max_level].update({
                        name: {
                            'match_map': Img(match_map_png),
                            'name': name,
                            'path' : match_map_png,
                            'range': cvt(json.loads(match_map_json.read_text())),
                            'factory': [
                                { 'offset': t['offset'], 'pos': cvt(t['pos']), 'range': cvt(t['range']) } for t in factory_data
                            ]
                        }
                    })



    def _get_name(self, attr, max_level, capture_image: Tuple[Img, Img], threshold = 0.85) -> Optional[str]:
        max_level = str(max_level)
        for name in self.match_map_templates[max_level]:
            d = self.match_map_templates[max_level][name]

            for target in capture_image:
                result = None
                if attr == 'png':
                    result = target.matching_png(d['match_map'], d['range'], threshold )
                elif attr == 'gray':
                    result = target.matching_gray(d['match_map'], d['range'], threshold )
                elif attr == 'hsv':
                    result = target.matching_hsv(d['match_map'], d['range'], threshold )

                if result and result.is_found:
                    return name

    def find_city(self, max_level, capture_image: Tuple[Img, Img], threshold = 0.85) -> Optional[str]:
        return self._get_name('png', max_level, capture_image, 0.90)

    def get_factory_info(self, max_level, name):
        max_level = str(max_level)
        name = str(name)
        return self.match_map_templates.get(max_level, {}).get(name, {}).get('factory', [])
