import polars as pl
from hackathon.utils.settings.settings_provider import SettingsProvider
from langchain_core.tools import tool


@tool(name_or_callable="get_nearest_planets")
def get_nearest_planets(planet_name: str, distance: float) -> list[str]:
    """Restituisce i pianeti che sono a una distanza minore o uguale a quella specificata.

    Args:
        - planet_name: Il nome del pianeta di riferimento.
        - distance: La distanza massima dal pianeta di riferimento.

    Utilizza il seguente tool quando la richiesta dell'utente include un pianeta specifico e una distanza massima.

    Esempio:
    Input: "Quali piatti possiamo gustare in un ristorante entro 83 anni luce da Cybertron, quest'ultimo incluso, evitando rigorosamente quelli cucinati con Farina di Nettuno?"
    Chain of thought: La richiesta dell'utente include il pianeta Cybertron e una distanza massima di 83 anni luce. Posso utilizzare il tool get_nearest_planets per ottenere
    i pianeti che sono a una distanza minore o uguale a 83 anni luce da Cybertron.
    Chiamata al tool: get_nearest_planets("Cybertron", 83)
    """
    distance_file_path = SettingsProvider().get_distance_csv_path()
    df = pl.read_csv(distance_file_path)
    return pl.Series(
        df.filter(pl.col(planet_name.lower()) <= distance).select(pl.col("/"))
    ).to_list()
