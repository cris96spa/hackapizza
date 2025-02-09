from typing import Any, Dict

import polars as pl
from hackathon.utils.settings.settings_provider import SettingsProvider
from langchain_core.tools import tool
from hackathon.utils.file_utils import load_json
from hackathon.models import Chef


@tool(name_or_callable="get_available_restaurants")
def get_available_restaurants() -> list[str]:
    """Restituisce il nome dei ristoranti disponibili
    Utilizza il seguente tool per ottenere la lista dei ristoranti disponibili.

    Esempio:
    Input: "Quali piatti sono preparati nel ristorante di Asgard utilizzando Essenza di Speziaria?"
    Chain of thought: Il nome del ristorante sembra essere Asgard, tuttavia non è chiaro se è un ristorante o un
    pianeta. Posso utilizzare il tool get_available_restaurants per ottenere la lista dei ristoranti disponibili.
    Chiamata al tool: get_available_restaurants()
    """
    chef_file_path = SettingsProvider().get_chefs_json_path()
    chefs = load_json(chef_file_path)
    return list(set([chef["restaurant"] for chef in chefs]))


@tool(name_or_callable="get_available_dishes")
def get_available_dishes() -> list[str]:
    """Restituisce il nome dei piatti disponibili
    Utilizza il seguente tool per ottenere la lista dei piatti disponibili.
    """
    dishes_file_path = SettingsProvider().get_dishes_json_path()
    dishes = load_json(dishes_file_path)
    return list(set([dish["dish_name"] for dish in dishes]))


def get_available_techniques() -> list[str]:
    """Restituisce il nome delle tecniche disponibili
    Utilizza il seguente tool per ottenere la lista delle tecniche disponibili.
    """
    dishes_file_path = SettingsProvider().get_dishes_json_path()
    dishes = load_json(dishes_file_path)
    return list(set([technique for dish in dishes for technique in dish["techniques"]]))


if __name__ == "__main__":
    # print(get_available_restaurants())
    print(get_available_dishes())
