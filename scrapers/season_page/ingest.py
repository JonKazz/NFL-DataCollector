import re
from urllib.parse import urlsplit
import pandas as pd
from scrapers.scraper import PageScraper

class SeasonPageScraper(PageScraper):
    def __init__(self):
        super().__init__()
        self.season_info = {}

    def load_page(self, url: str) -> None:
        super().load_page(url)
        self.season_info['url'] = url

    def get_season_info(self) -> pd.DataFrame:
        """Parse awards + leaders from #meta and set season_year from the page DOM."""
        self._get_award_winners()
        self._set_season_year()
        return pd.DataFrame([self.season_info])

    # ----- constants / regexes -----
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

    # /players/M/MahoPa00.htm -> MahoPa00
    _PLAYER_ID_RE = re.compile(r"/players/[A-Z]/([A-Za-z0-9]+)\.htm")
    # /teams/kan/2023.htm     -> kan
    _TEAM_ID_RE   = re.compile(r"/teams/([A-Za-z]{3})/\d{4}\.htm")
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

    def _extract_player_name_from_paragraph(self, p) -> str | None:
        """Extract player name from a paragraph element containing award information."""
        # Look for the player name in the paragraph text
        # The name is usually the text content of the <a> tag
        a_tag = p.find("a")
        if a_tag:
            player_name = a_tag.get_text(strip=True)
            if player_name:
                return player_name
        
        # Fallback: try to extract from the paragraph text
        # Look for text that might be a player name (usually after the award label)
        p_text = p.get_text(strip=True)
        
        # For awards like "AP MVP", the player name is usually after the colon or in the link
        if ":" in p_text:
            # Split by colon and take the part after it
            parts = p_text.split(":", 1)
            if len(parts) > 1:
                # Clean up the text after the colon
                name_part = parts[1].strip()
                # Remove any extra text like team names, stats, etc.
                # Look for the first word or two that might be the player name
                name_words = name_part.split()
                if name_words:
                    # Take first 2-3 words as likely player name
                    potential_name = " ".join(name_words[:3])
                    # Clean up any remaining punctuation or extra text
                    potential_name = potential_name.strip(".,()")
                    if potential_name and len(potential_name) > 2:
                        return potential_name
        
        return None

    def _get_award_winners(self) -> None:
        meta_div = self._extract_div('meta')
        if meta_div is None:
            return

        # Find the child <div> that actually contains the <p><strong>...</strong></p> lines
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
                # Store both player_id and player_name
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["receiving_leader_id"] = player_id
                self.season_info["receiving_leader_name"] = player_name

            elif label == "Super Bowl Champion":
                # Store 3-letter team_id (e.g., 'kan')
                team_id = self._team_id_from_href(href)
                self.season_info["sb_champ"] = team_id

            elif label == "AP MVP":
                # Player awards → store both player ID and name
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["mvp_id"] = player_id
                self.season_info["mvp_name"] = player_name

            elif label == "AP Offensive Player of the Year":
                # Player awards → store both player ID and name
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["opoy_id"] = player_id
                self.season_info["opoy_name"] = player_name

            elif label == "AP Defensive Player of the Year":
                # Player awards → store both player ID and name
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["dpoy_id"] = player_id
                self.season_info["dpoy_name"] = player_name

            elif label == "AP Offensive Rookie of the Year":
                # Player awards → store both player ID and name
                player_id = self._player_id_from_href(href)
                player_name = self._extract_player_name_from_paragraph(p)
                self.season_info["oroy_id"] = player_id
                self.season_info["oroy_name"] = player_name

            elif label == "AP Defensive Rookie of the Year":
                # Player awards → store both player ID and name
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

        self.season_info['season_year'] = year

    def extract_team_links_from_season_page(self) -> list[str]:
        team_links = []
        for table_id in ['AFC', 'NFC']:
            table = self._extract_table(table_id)
            if table is None:
                raise ValueError(f'Season standings table not found at table_id: {table_id}')

            links = [td.find("a")["href"] for td in table.find_all(attrs={"data-stat": "team"}) if td.find("a")]
            team_links += links

        return team_links
