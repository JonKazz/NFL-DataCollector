import pandas as pd
from scrapers.scraper import PageScraper

class SeasonPageScraper(PageScraper):
    def __init__(self):
        super().__init__()
        self.season_info = {}
        self.season_team_stats = pd.DataFrame()
    
    
    def _get_award_winners(self):
        meta_div = self._extract_div('meta')
        inner_meta_div = meta_div.find_all('div', recursive=False)[1]
        meta_ps = inner_meta_div.find_all('p')
        for p in meta_ps:
            award = p.find("strong").get_text(strip=True)
            award_winner_link = p.find("a").get("href")
            self.season_info[award] = award_winner_link
        
    
    def extract_team_links_from_season_page(self) -> list[str]:
        team_links = []
        for table_id in ['AFC', 'NFC']:
            table = self._extract_table(table_id)
            if table is None:
                raise ValueError(f'Season standings table not found at table_id: {table_id}')
            
            links = [td.find("a")["href"] for td in table.find_all(attrs={"data-stat": "team"}) if td.find("a")]
            team_links += links
        
        return team_links
        