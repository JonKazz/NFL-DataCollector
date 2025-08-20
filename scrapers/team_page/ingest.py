import pandas as pd
from scrapers.scraper import PageScraper

class TeamPageScraper(PageScraper):
    def __init__(self):
        super().__init__()
        self.season_team_stats_df = {}

    
    def scrape_team_summary(self):        
        summary_div = self.soup.find('div', {'data-template': 'Partials/Teams/Summary'})
        if not summary_div:
            raise ValueError(f'Summary section not found for {self.url}')

        logo_img = self.soup.find('img', class_='teamlogo')
        if not logo_img:
            raise ValueError(f'Logo image not found for {self.url}')
        
        logo_src = logo_img['src']
        
        headers = {'Coach', 'Points For', 'Points Against', 'Record', 'Playoffs', 'Offensive Coordinator', 
                'Defensive Coordinator', 'Stadium', 'Offensive Scheme', 'Defensive Alignment'}
        self.season_team_stats_df = {header: None for header in headers}
        
        for p in summary_div.find_all('p'):
            strong = p.find('strong')
            if strong:
                key = strong.text.strip(':')
                if key in headers:
                    strong.extract()
                    value = p.get_text(strip=True)
                    self.season_team_stats_df[key] = value

        team_id = self.url.split('/')[4]
        year = self.url.split('/')[5].split('.')[0]
        
        self.season_team_stats_df['team_id'] = team_id
        self.season_team_stats_df['year'] = year
        self.season_team_stats_df['logo'] = logo_src
        return pd.DataFrame([self.season_team_stats_df])


    def extract_game_pages_urls(self) -> list[str]:
        games_table = self._extract_table('games')
        
        game_links = []
        for td in games_table.find_all('td', {'data-stat': 'boxscore_word'}):
            a_tag = td.find('a')
            if a_tag and 'href' in a_tag.attrs:
                url = 'https://www.pro-football-reference.com' + a_tag['href']
                game_links.append(url)

        return game_links
        
