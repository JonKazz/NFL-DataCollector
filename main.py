import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import warnings
from pandas.errors import PerformanceWarning
warnings.simplefilter(action='ignore', category=PerformanceWarning)

from nfl_datacollector.utils import TEAM_ID_TO_CITY_MAP, ALL_SEASONS
from nfl_datacollector.config import DatabaseConfig
from scrapers.main import *
from load import *

# if __name__ == "__main__":
#     config = DatabaseConfig.load()
#     loader = DatabaseLoader(config)
#     logged_urls = get_all_db_player_urls(loader)
#     for team in list(TEAM_ID_TO_CITY_MAP.keys()):
#         game_links = extract_game_links_from_team_page(f'https://www.pro-football-reference.com/teams/{team}/2019.htm')
#         for game_link in game_links:
#             player_urls = extract_player_urls_from_game_page(game_link)
#             for player_url in player_urls:
#                 if player_url not in logged_urls:
#                     ETL_player_profile(player_url, loader)
#                 else:
#                     print(f'{player_url} already logged. Skipping')
#     print('FINISHED ALL GAMES')



    
# if __name__ == '__main__':
#     config = DatabaseConfig.load()
#     loader = DatabaseLoader(config)
#     for year in [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015]:
#         ETL_ap_team_votes_by_year(year, loader)     

if __name__ == '__main__':
    config = DatabaseConfig.load()
    loader = DatabaseLoader(config)
    for year in ALL_SEASONS:
        ETL_season_info_by_year(year, loader)   
