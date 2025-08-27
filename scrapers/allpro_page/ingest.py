import re
import pandas as pd
from scrapers.scraper import PageScraper

_YEAR_RE = re.compile(r"/years/(\d{4})/")

class AllProPageScraper(PageScraper):
    def load_page(self, url: str) -> None:
        super().load_page(url)
        self.url = url

    def get_ap_team_votes(self) -> pd.DataFrame:
        """
        Parse the #all_pro table and return players who received an
        AP 1st or 2nd team selection.

        Columns: player_id, team, position, ap_team (int: 1 or 2), season_year (int)
        """
        # pull season from the URL, e.g. /years/2022/allpro.htm -> 2022
        season_year = None
        if getattr(self, "url", None):
            m = _YEAR_RE.search(self.url)
            if m:
                season_year = int(m.group(1))

        table = self.soup.find('table', id='all_pro')
        if not table:
            raise ValueError("[!] Could not find All-Pros table")

        tbody = table.find('tbody') or table
        rows_out = []

        for tr in tbody.find_all('tr', recursive=False):
            if 'class' in tr.attrs and 'thead' in tr['class']:
                continue

            ap_cell = tr.find('td', {'data-stat': 'all_pro_string'})
            if not ap_cell:
                continue

            ap_text = ap_cell.get_text(" ", strip=True)
            m = re.search(r'AP\s*:\s*(1st|2nd)\s*Tm', ap_text, flags=re.I)
            if not m:
                continue
            ap_team_int = 1 if m.group(1).startswith('1') else 2

            player_td = tr.find('td', {'data-stat': 'player'})
            team_td   = tr.find('td', {'data-stat': 'team'})
            pos_cell  = tr.find('th', {'data-stat': 'pos'}) or tr.find('td', {'data-stat': 'pos'})

            player_id = None
            if player_td:
                player_id = player_td.get('data-append-csv')
                if not player_id:
                    a = player_td.find('a')
                    if a and a.get('href'):
                        player_id = a['href'].split('/')[-1].split('.')[0]

            rows_out.append({
                'player_id': player_id,
                'team': team_td.get_text(" ", strip=True) if team_td else None,
                'position': pos_cell.get_text(" ", strip=True) if pos_cell else None,
                'ap_team': ap_team_int,      # 1 or 2
                'season_year': season_year,  # e.g., 2022 for your URL
            })

        df = pd.DataFrame(rows_out)
        if not df.empty:
            df['ap_team'] = df['ap_team'].astype(int)
            if season_year is not None:
                df['season_year'] = int(season_year)
        return df
