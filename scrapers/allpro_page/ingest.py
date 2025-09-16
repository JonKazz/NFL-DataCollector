import re
import pandas as pd
from scrapers.scraper import PageScraper
from nfl_datacollector.utils import TEAM_ABR_TO_TEAM_ID_MAP

_YEAR_RE = re.compile(r"/years/(\d{4})/")

class AllProPageScraper(PageScraper):
    def load_page(self, url: str) -> None:
        super().load_page(url)
        self.url = url

    def get_ap_team_votes(self) -> pd.DataFrame:
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
            player_name = None
            if player_td:
                a = player_td.find('a')
                player_id = player_td.get('data-append-csv')
                if not player_id and a and a.get('href'):
                    player_id = a['href'].split('/')[-1].split('.')[0]
                # name text from the anchor if present, else the cell
                player_name = (a.get_text(" ", strip=True) if a else player_td.get_text(" ", strip=True)) or None

            if not player_id:
                continue
            if not team_td:
                continue
            
            a_team = team_td.find('a')
            team_abbr = (a_team.get_text(" ", strip=True) if a_team else team_td.get_text(" ", strip=True) or "").upper()
            team_internal_id = TEAM_ABR_TO_TEAM_ID_MAP.get(team_abbr)
            if team_internal_id is None:
                continue  # STRICT: do not attempt any fallback parsing

            row_id = f"{season_year}_{player_id}" if (season_year is not None and player_id) else None
            if not row_id:
                continue  # keep data clean for your NOT NULL/PK constraints

            rows_out.append({
                'id': row_id,
                'player_id': player_id,
                'player_name': player_name,
                'team_id': team_internal_id,
                'position': pos_cell.get_text(" ", strip=True) if pos_cell else None,
                'ap_team': ap_team_int,
                'season_year': season_year,
            })

        df = pd.DataFrame(rows_out)
        if not df.empty:
            df['ap_team'] = df['ap_team'].astype(int)
            if season_year is not None:
                df['season_year'] = int(season_year)
        return df
