import pandas as pd
import re
from scrapers.scraper import PageScraper

class PlayerProfilePageScraper(PageScraper):
    def __init__(self):
        super().__init__()
        self.player_df = {}
    
    def load_page(self, url: str) -> None:
        super().load_page(url)
        self.player_df['url'] = url
        player_id = url.split('/')[-1].split('.')[0]
        self.player_df['player_id'] = player_id

    def get_player_profile(self) -> pd.DataFrame:
        self._parse_player_metadata()
        return pd.DataFrame([self.player_df])

    
    def _parse_player_metadata(self) -> pd.DataFrame:
        meta = self._extract_div('meta')
        if not meta:
            raise ValueError("[!] Could not find metadata div")
        
        #Name
        name = meta.find('h1').find('span').get_text(strip=True)
        self.player_df['name'] = name
        
        # Height
        match = re.search(r'\d+-\d+', str(meta))
        if not match:
            raise ValueError('[!] Missing height')
        height = match.group(0)
        self.player_df['height'] = height
        
        # Weight
        match = re.search(r'\d+lb', str(meta))
        if not match:
            raise ValueError('[!] Missing weight')
        weight = match.group(0)
        weight = weight.replace('lb', '')
        self.player_df['weight'] = weight
        
        # Date of Birth
        match = re.search(r'data-birth=["\']?(\d{4}-\d{2}-\d{2})', str(meta))
        if not match:
            raise ValueError('[!] Missing date of birth')
        dob = match.group(1)
        self.player_df['dob'] = dob
    
        # College
        college_link = meta.find('strong', string='College')
        if not college_link:
            raise ValueError('[!] Missing college')
        college = college_link.find_next('a').text.strip()
        self.player_df['college'] = college