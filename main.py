import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import warnings
from pandas.errors import PerformanceWarning
warnings.simplefilter(action='ignore', category=PerformanceWarning)

from nfl_datacollector.utils import TEAM_ID_TO_CITY_MAP
from nfl_datacollector.config import DatabaseConfig
from scrapers.main import *
from load import DatabaseLoader, get_all_db_player_urls, create_season_info_table

# if __name__ == "__main__":
#     config = DatabaseConfig.load()
#     loader = DatabaseLoader(config)
#     logged_urls = get_all_db_player_urls(loader)
#     for key in TEAM_ID_TO_CITY_MAP[::-1]:
#         game_links = extract_game_links_from_team_page(f'https://www.pro-football-reference.com/teams/{key}/2022.htm')
#         for game_link in game_links:
#             player_urls = extract_player_urls_from_game_page(game_link)
#             for player_url in player_urls:
#                 if player_url not in logged_urls:
#                     ETL_player_profile(player_url, loader)
#                 else:
#                     print(f'{player_url} already logged. Skipping')

if __name__ == "__main__":
    config = DatabaseConfig.load()
    loader = DatabaseLoader(config)
    ETL_season_info(2020, loader)


# if __name__ == "__main__":
#     config = DatabaseConfig.load()
#     loader = DatabaseLoader(config)
#     ETL_season_info('https://www.pro-football-reference.com/years/2021/', loader)
    