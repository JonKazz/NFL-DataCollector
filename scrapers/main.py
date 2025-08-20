from .games_page.ingest import get_urls_by_week_and_year, GamePageScraper
from .games_page.transform import GamePageTransformer
from load import get_all_db_game_urls, get_all_db_player_urls

from .team_page.ingest import TeamPageScraper
from .team_page.transform import transform_teams_table

from .player_page.ingest import PlayerProfilePageScraper

from .season_page.ingest import SeasonPageScraper


def extract_player_urls_from_game_page(url):
    scraper = GamePageScraper()
    scraper.load_page(url)
    player_ids = scraper.extract_player_ids_from_game_page()
    urls = [f'https://www.pro-football-reference.com/players/{player_id[0]}/{player_id}.htm' for player_id in player_ids]
    return urls


def extract_game_links_from_team_page(url):
    team_page = TeamPageScraper()
    team_page.load_page(url)
    game_links = team_page.extract_game_pages_urls()
    return game_links


def extract_team_links_from_season_page(url):
    season_page = SeasonPageScraper()
    season_page.load_page(url)
    team_links = season_page.extract_team_links_from_season_page()
    return team_links
    
    
def ETL_games_season_year(year: int, loader):
    logged_urls = get_all_db_game_urls()
    for week in [str(x) for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]]:
        game_urls = get_urls_by_week_and_year(week, year)
        for url in game_urls:
            if url not in logged_urls:
                ETL_game_page(url, loader)
            else:
                print(f'{url} already logged. Skipping')


def ETL_games_season_year_and_week(year: int, week: int, loader):
    logged_urls = get_all_db_game_urls()
    game_urls = get_urls_by_week_and_year(week, year)
    for url in game_urls:
        if url not in logged_urls:
            ETL_game_page(url, loader)
        else:
            print(f'{url} already logged. Skipping')


def ETL_game_page(url, loader):
    print('Scraping and inserting for:', url)
    scraper = GamePageScraper()
    scraper.load_page(url)
    
    df_game_info = scraper.get_game_info()
    df_team_stats = scraper.get_game_stats()
    df_player_stats = scraper.get_game_player_stats()
    
    transformer = GamePageTransformer(df_game_info, df_team_stats, df_player_stats)
    df_game_info = transformer.transform_game_info_df()
    df_team_stats = transformer.transform_game_stats_df()
    df_player_stats = transformer.transform_player_stats_df()
    
    loader.insert_game_info_df(df_game_info)
    loader.insert_game_stats_df(df_team_stats)
    loader.insert_game_player_stats_df(df_player_stats)    
    
    

def ETL_season_team_info(url, loader):
    team_page = TeamPageScraper()
    team_page.load_page(url)
    
    season_team_info_df = team_page.scrape_team_summary()
    season_team_info_df = transform_teams_table(season_team_info_df)    
    loader.insert_season_team_info_df(season_team_info_df)


def ETL_player_profile(url, loader):
    scraper = PlayerProfilePageScraper()
    scraper.load_page(url)
    player_profile_df = scraper.get_player_profile()
    loader.insert_player_profile_df(player_profile_df)