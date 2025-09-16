import pandas as pd
from scrapers.scraper import PageScraper

class TeamPageScraper(PageScraper):
    def __init__(self):
        super().__init__()
        self.season_team_stats_df = {}


    def get_team_info(self) -> pd.DataFrame:
        self._scrape_team_summary()
        self._scrape_team_stats()
        return pd.DataFrame([self.season_team_stats_df])


    def _scrape_team_stats(self) -> None:
        table = self._extract_table('team_stats')
        if not table:
            raise ValueError(f'team_stats table not found for {self.url}')

        tbody = table.find('tbody')
        trs = tbody.find_all('tr', recursive=False)
        if len(trs) < 2:
            raise ValueError('Expected at least two rows (team/opponent) in table id: team_stats')

        def row_to_dict(tr):
            d = {}
            for td in tr.find_all('td'):
                key = td.get('data-stat')
                if key:
                    d[key] = td.get_text(strip=True)
            return d

        team_row = row_to_dict(trs[0])   # Team Stats
        opp_row  = row_to_dict(trs[1])   # Opp Stats

        self.season_team_stats_df.update({
            'points_for':          team_row.get('points'),
            'points_against':      opp_row.get('points'),
            'total_yards_for':     team_row.get('total_yards'),
            'total_yards_against': opp_row.get('total_yards'),
            'turnovers':           team_row.get('turnovers'),   
            'forced_turnovers':    opp_row.get('turnovers'),
            'pass_yards_for':      team_row.get('pass_yds'),
            'pass_yards_against':  opp_row.get('pass_yds'),
            'pass_td_for':         team_row.get('pass_td'),
            'pass_td_against':     opp_row.get('pass_td'),
            'pass_ints_thrown':     team_row.get('pass_int'),
            'pass_ints':  opp_row.get('pass_int'),
            'rush_yards_for':      team_row.get('rush_yds'),
            'rush_yards_against':  opp_row.get('rush_yds'),
            'rush_td_for':         team_row.get('rush_td'),
            'rush_td_against':     opp_row.get('rush_td'),
            'penalties_for':       team_row.get('penalties'),
        })


    def _scrape_team_summary(self) -> None:
        summary_div = self.soup.find('div', {'data-template': 'Partials/Teams/Summary'})
        if not summary_div:
            raise ValueError(f'Summary section not found for {self.url}')
        logo_img = self.soup.find('img', class_='teamlogo')
        if not logo_img:
            raise ValueError(f'Logo image not found for {self.url}')
        logo_src = logo_img['src']
        headers = {'Coach','Points For','Points Against','Record','Playoffs','Offensive Coordinator',
                   'Defensive Coordinator','Stadium','Offensive Scheme','Defensive Alignment'}
        self.season_team_stats_df = {h: None for h in headers}
        for p in summary_div.find_all('p'):
            strong = p.find('strong')
            if strong:
                key = strong.text.strip(':')
                if key in headers:
                    strong.extract()
                    self.season_team_stats_df[key] = p.get_text(strip=True)
        self.season_team_stats_df['team_id'] = self.url.split('/')[4]
        self.season_team_stats_df['year'] = self.url.split('/')[5].split('.')[0]
        self.season_team_stats_df['logo'] = logo_src


    def extract_game_pages_urls(self) -> list[str]:
        games_table = self._extract_table('games')
        game_links = []
        for td in games_table.find_all('td', {'data-stat': 'boxscore_word'}):
            a_tag = td.find('a')
            if a_tag and 'href' in a_tag.attrs:
                game_links.append('https://www.pro-football-reference.com' + a_tag['href'])
        return game_links
