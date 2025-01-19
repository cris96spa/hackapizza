from typing import Any, Dict

import pandas as pd
from hackathon.graph.models import PlanetDistanceResponse, Planet
from hackathon.utils.settings.settings_provider import SettingsProvider


def planet_distance(planet: Planet) -> Dict[str, Any]:
    print("---COMPUTE DISTANCE BETWEEN PLANETS---")

    distance_file_path = SettingsProvider().get_distance_csv_path()
    distanze = pd.read_csv(distance_file_path, index_col=0)

    near_planets: PlanetDistanceResponse = list(
        distanze.loc[planet.name][distanze.loc[planet.name] < planet.distance].index
    )

    return near_planets
