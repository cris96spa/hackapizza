from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.utils.file_utils import load_json


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
    return list(set([chef["restaurant"].lower() for chef in chefs]))


def get_available_dishes() -> list[str]:
    """Restituisce il nome dei piatti disponibili
    Utilizza il seguente tool per ottenere la lista dei piatti disponibili.
    """
    dishes_file_path = SettingsProvider().get_dishes_json_path()
    dishes = load_json(dishes_file_path)
    return list(set([dish["name"].lower() for dish in dishes]))


def get_available_techniques() -> list[str]:
    """Restituisce il nome delle tecniche disponibili
    Utilizza il seguente tool per ottenere la lista delle tecniche disponibili.
    """
    techniques_json_path = SettingsProvider().get_techniques_json_path()
    techniques = load_json(techniques_json_path)
    return list(set([technique["name"].lower() for technique in techniques]))


def get_available_licenses() -> list[str]:
    """Restituisce il nome delle licenze disponibili
    Utilizza il seguente tool per ottenere la lista delle licenze disponibili.
    """
    chefs_file_path = SettingsProvider().get_chefs_json_path()
    chefs = load_json(chefs_file_path)
    license_names = []
    for chef in chefs:
        for license in chef["licenses"]:
            license_names.append(license["name"].lower())


def get_available_planets() -> list[str]:
    """Restituisce il nome dei pianeti disponibili
    Utilizza il seguente tool per ottenere la lista dei pianeti disponibili.
    """
    chef_file_path = SettingsProvider().get_chefs_json_path()
    chefs = load_json(chef_file_path)
    return list(set([chef["planet_name"].lower() for chef in chefs]))


def get_available_culinary_orders() -> list[str]:
    """Restituisce il nome degli ordini culinari disponibili
    Utilizza il seguente tool per ottenere la lista degli ordini culinari disponibili.
    """
    dishes_file_path = SettingsProvider().get_dishes_json_path()
    dishes = load_json(dishes_file_path)
    return list(set([dish["culinary_order"].lower() for dish in dishes]))


def get_available_technique_categories() -> list[str]:
    """Restituisce il nome delle categorie delle tecniche disponibili
    Utilizza il seguente tool per ottenere la lista delle categorie delle tecniche disponibili.
    """
    techniques_json_path = SettingsProvider().get_techniques_json_path()
    techniques = load_json(techniques_json_path)
    return list(set([technique["category"].lower() for technique in techniques]))


if __name__ == "__main__":
    print(get_available_restaurants())
    print(get_available_dishes())
    print(get_available_techniques())
    print(get_available_licenses())
    print(get_available_planets())
    print(get_available_culinary_orders())
    print(get_available_technique_categories())
