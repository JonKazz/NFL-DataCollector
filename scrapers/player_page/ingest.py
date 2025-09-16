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
        self.player_df['player_id'] = url[-12:-4]
    def get_player_profile(self) -> pd.DataFrame:
        self._parse_player_metadata()
        return pd.DataFrame([self.player_df])

    def _parse_player_metadata(self) -> None:
        meta = self._extract_div('meta')
        if not meta:
            raise ValueError("[!] Could not find metadata div")

        # Name
        name = meta.find('h1').find('span').get_text(strip=True)
        self.player_df['name'] = name

        # Image
        self.player_df['img'] = self._extract_player_image_url(meta)

        # Height
        match = re.search(r'\d+-\d+', str(meta))
        if not match:
            raise ValueError('[!] Missing height')
        self.player_df['height'] = match.group(0)

        # Weight
        match = re.search(r'\d+lb', str(meta))
        if not match:
            self.player_df['weight'] = pd.NA
        else:
            self.player_df['weight'] = match.group(0).replace('lb', '')

        # Date of Birth
        match = re.search(r'data-birth=["\']?(\d{4}-\d{2}-\d{2})', str(meta))
        if not match:
            raise ValueError('[!] Missing date of birth')
        self.player_df['dob'] = match.group(1)

        # College
        college_link = meta.find('strong', string='College')
        if not college_link:
            self.player_df['college'] = pd.NA
        else:
            self.player_df['college'] = college_link.find_next('a').text.strip()

    def _extract_player_image_url(self, meta) -> str | None:
        media = meta.find('div', class_='media-item')
        if media:
            img = media.find('img')
            if img:
                return img.get('src')

        return None