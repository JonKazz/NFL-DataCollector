import requests
from nfl_datacollector.utils import polite_sleep
from bs4 import BeautifulSoup, Comment, Tag

class PageScraper:
    def __init__(self):
        self.url = None
        self.soup = None
        
    
    def load_page(self, url: str) -> None:
        self.url = url
        html = requests.get(url)
        self.soup = BeautifulSoup(html.text, 'html.parser')
        polite_sleep(6, 8)
        
    def _extract_table(self, table_id_or_class: str) -> Tag:
        if self.soup is None:
            raise ValueError('Page has not been loaded yet')
        
        # Searching for id
        table = self.soup.find('table', id=table_id_or_class)
        if table:
            return table

        # Searching for class
        table = self.soup.find('table', class_=table_id_or_class)
        if table:
            return table

        # If not found, look through HTML comments
        comments = self.soup.find_all(string=lambda text: isinstance(text, Comment))
        for c in comments:
            if 'table' in c and table_id_or_class in c:
                comment_soup = BeautifulSoup(c, 'html.parser')
                
                table = comment_soup.find('table', id=table_id_or_class)
                if table:
                    return table
                
                table = comment_soup.find('table', class_=table_id_or_class)
                if table:
                    return table

        return None
        

    def _extract_div(self, div_id: str) -> Tag:
        if self.soup is None:
            raise ValueError('Page has not been loaded yet')
        
        # Searching for id
        div = self.soup.find('div', id=div_id)
        if div:
            return div

        # Searching for class
        div = self.soup.find('div', class_=div_id)
        if div:
            return div
        
        # If not found, look through HTML comments
        comments = self.soup.find_all(string=lambda text: isinstance(text, Comment))
        for c in comments:
            if div_id in c:
                comment_soup = BeautifulSoup(c, 'html.parser')

                div = comment_soup.find('div', id=div_id)
                if div:
                    return div
                
                div = comment_soup.find('div', class_=div_id)
                if div:
                    return div

        return None
    
    
    