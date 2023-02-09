from typing import List, Dict
from typing import Dict, List, Tuple
from PIL import Image
from datetime import datetime
import glob
from pathlib import Path
import numpy as np
import yaml


class Radar:

    def __init__(self,
                 rdr_code: str,
                 latitude: float,
                 longitude: float,
                 radius: int,
                 name: str):
        self.rdr_code = rdr_code
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.name = name

    @classmethod
    def from_radar_dict(cls, radar_dict: Dict) -> 'Radar':
        """
        rdr_code: 'cc'
        latitude: 39.428820
        longitude: -6.285380
        radius: 240
        name: 'Cáceres'
        TODO: maybe moved the dict keys as class variables
        :param radar_dict:
        :return:
        """
        return Radar(
            rdr_code=radar_dict['rdr_code'],
            latitude=radar_dict['latitude'],
            longitude=radar_dict['longitude'],
            radius=radar_dict['radius'],
            name=radar_dict['name']
        )


class RadarCollection:
    YAML_FILE_DATA_KEY = 'data'
    YAML_FILE_METADATA_KEY = 'metadata'

    def __init__(self,
                 radars: List[Radar],
                 meta_data_dict: Dict):
        """
        TODO: maybe leave transform metadata into class
        :param radars:
        :param meta_data_dict:
        """
        self.radars = radars
        self.meta_data_dict = meta_data_dict

    def to_dict(self) -> Dict[str, Radar]:  # list out radar code to radar
        """
        :return:
        """
        return {x.rdr_code: x for x in self.radars}

    @classmethod
    def from_file_path(cls, path: str) -> 'RadarCollection':
        with open(path, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
            lst_radar = []
            for radar_key in data_loaded[RadarCollection.YAML_FILE_DATA_KEY].keys():
                radar_dict = data_loaded[RadarCollection.YAML_FILE_DATA_KEY][radar_key]
                radar = Radar.from_radar_dict(radar_dict)
                lst_radar.append(radar)
            return RadarCollection(
                radars=lst_radar,
                meta_data_dict=data_loaded[RadarCollection.YAML_FILE_METADATA_KEY]
            )
