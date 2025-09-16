import re
import pandas as pd
from scrapers.scraper import PageScraper

AFC_PLAYOFF_STANDINGS_TABLE = 'afc_playoff_standings'
NFC_PLAYOFF_STANDINGS_TABLE = 'nfc_playoff_standings'

class SeasonPageScraper(PageScraper):
    def __init__(self):
        super().__init__()
        self.season_info = {}
        self.season_team_seeds_df = pd.DataFrame()
        self.season_year = None

    def load_page(self, url: str) -> None:
        super().load_page(url)
        self.season_info['url'] = url
        self._set_season_year()

    def get_season_info(self) -> pd.DataFrame:
        self._get_award_winners()
        self._set_season_and_conference_columns()
        return pd.DataFrame([self.season_info])
    
    def get_season_team_seeds(self) -> pd.DataFrame:
        self._get_team_seeds()
        return self.season_team_seeds_df
        

    _AWARD_LABELS = {
        "Super Bowl Champion",
        "AP MVP",
        "AP Offensive Rookie of the Year",
        "AP Defensive Rookie of the Year",
        "AP Offensive Player of the Year",
        "AP Defensive Player of the Year",
        "Passing Leader",
        "Rushing Leader",
        "Receiving Leader",
    }
    
    _PLAYER_ID_RE = re.compile(r"/players/[A-Z]/([A-Za-z0-9]+)\.htm") # /players/M/MahoPa00.htm -> MahoPa00
    _TEAM_ID_RE   = re.compile(r"/teams/([A-Za-z]{3})/\d{4}\.htm")     # /teams/kan/2023.htm    -> kan
    _YEAR_IN_H1_RE = re.compile(r"\b(19|20)\d{2}\b")


    @staticmethod
    def _player_id_from_href(href: str | None) -> str | None:
        if not href:
            return None
        m = SeasonPageScraper._PLAYER_ID_RE.search(href)
        return m.group(1) if m else None

    @staticmethod
    def _team_id_from_href(href: str | None) -> str | None:
        if not href:
            return None
        m = SeasonPageScraper._TEAM_ID_RE.search(href)
        return m.group(1).lower() if m else None

    def _set_season_and_conference_columns(self) -> None:
        self.season_info['season_year'] = self.season_year
        self.season_info['afc_team_seed_id'] = 'AFC_' + str(self.season_year)
        self.season_info['nfc_team_seed_id'] = 'NFC_' + str(self.season_year)
    
    def _extract_player_name_from_paragraph(self, p) -> str | None:
        a_tag = p.find("a")
        if a_tag:
            player_name = a_tag.get_text(strip=True)
            if player_name:
                return player_name
        
        p_text = p.get_text(strip=True)
        
        if ":" in p_text:
            parts = p_text.split(":", 1)
            if len(parts) > 1:
                name_part = parts[1].strip()
                name_words = name_part.split()
                if name_words:
                    potential_name = " ".join(name_words[:3])
                    potential_name = potential_name.strip(".,()")
                    if potential_name and len(potential_name) > 2:
                        return potential_name
        
        return None

    def _get_award_winners(self) -> None:        
        meta_div = self._extract_div('meta')
        if meta_div is None:
            return

        inner_meta_div = None
        for d in meta_div.find_all('div', recursive=False):
            if d.find('p') and d.find('strong'):
                inner_meta_div = d
                break
        if inner_meta_div is None:
            divs = meta_div.find_all('div', recursive=False)
            inner_meta_div = divs[1] if len(divs) > 1 else meta_div

        for p in inner_meta_div.find_all('p'):
            strong = p.find("strong")
            if not strong:
                continue

            label = strong.get_text(strip=True)
            if label not in self._AWARD_LABELS:
                continue

            a = p.find("a")
            href = a.get("href") if a else None

            if label == "Passing Leader":
                # Store both player_id and player_name
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["passing_leader_id"] = player_id
                self.season_info["passing_leader_name"] = player_name

            elif label == "Rushing Leader":
                # Store both player_id and player_name
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["rushing_leader_id"] = player_id
                self.season_info["rushing_leader_name"] = player_name

            elif label == "Receiving Leader":
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["receiving_leader_id"] = player_id
                self.season_info["receiving_leader_name"] = player_name

            elif label == "Super Bowl Champion":
                team_id = self._team_id_from_href(href)
                self.season_info["sb_champ"] = team_id

            elif label == "AP MVP":
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["mvp_id"] = player_id
                self.season_info["mvp_name"] = player_name

            elif label == "AP Offensive Player of the Year":
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["opoy_id"] = player_id
                self.season_info["opoy_name"] = player_name

            elif label == "AP Defensive Player of the Year":
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["dpoy_id"] = player_id
                self.season_info["dpoy_name"] = player_name

            elif label == "AP Offensive Rookie of the Year":
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["oroy_id"] = player_id
                self.season_info["oroy_name"] = player_name

            elif label == "AP Defensive Rookie of the Year":
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["droy_id"] = player_id
                self.season_info["droy_name"] = player_name


    def _set_season_year(self) -> None:
        year = None
        meta_div = self._extract_div('meta')
        if meta_div:
            h1 = meta_div.find('h1')
            if h1:
                h1_text = h1.get_text(" ", strip=True)
                m = self._YEAR_IN_H1_RE.search(h1_text)
                if m:
                    year = int(m.group(0))

        if year is None:
            raise ValueError("Could not determine season_year from page")

        self.season_year = year
    
    
    # ---------------------------------------------
    # Seeds Methods
    # ---------------------------------------------
    def _get_team_seeds(self) -> None:
        season_year = self.season_year
        rows = []

        for conf in ('afc', 'nfc'):
            table_id = conf + '_playoff_standings'
            table = self._extract_table(table_id)
            if table is None:
                raise ValueError(f'[!] GamePage table with id/class: ({table_id}) not found')

            tbody = table.find('tbody')
            if not tbody:
                continue

            seeds_map: dict[int, str | None] = {}
            positions_map: dict[int, str | None] = {}

            for tr in tbody.find_all('tr', recursive=False):
                th = tr.find('th', attrs={'data-stat': 'team'})
                if not th:
                    continue

                csk = th.get('csk')
                try:
                    seed = int(csk) if csk is not None else None
                except ValueError:
                    seed = None
                if seed is None:
                    continue

                # team_id -> pd.NA if missing
                a = th.find('a', href=True)
                team_id_raw = self._team_id_from_href(a['href']) if a else None
                team_id = team_id_raw if team_id_raw else pd.NA

                # position -> pd.NA if missing
                pos_td = tr.find('td', attrs={'data-stat': 'why'})
                if pos_td:
                    txt = pos_td.get_text(strip=True)
                    position = txt if txt else pd.NA
                else:
                    position = pd.NA

                seeds_map[seed] = team_id
                positions_map[seed] = position

            row = {
                'id': f'{conf}_{season_year}',
                'conference': conf,
                'season_year': int(season_year)
            }
            for s in range(1, 17):
                row[f"seed_team_{s}"] = seeds_map.get(s, pd.NA)
                row[f"seed_position_{s}"] = positions_map.get(s, pd.NA)

            rows.append(row)

        if rows:
            new_df = pd.DataFrame(rows)
            self.season_team_seeds_df = pd.concat(
                [self.season_team_seeds_df, new_df], ignore_index=True
            )


    # ---------------------------------------------
    # Helper Methods
    # ---------------------------------------------
    def extract_team_links_from_season_page(self) -> list[str]:
        team_links = []
        for table_id in ['AFC', 'NFC']:
            table = self._extract_table(table_id)
            if table is None:
                raise ValueError(f'Season standings table not found at table_id: {table_id}')

            links = [td.find("a")["href"] for td in table.find_all(attrs={"data-stat": "team"}) if td.find("a")]
            team_links += links

        return team_links