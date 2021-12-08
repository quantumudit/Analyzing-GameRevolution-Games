from requests_html import HTMLSession
from datetime import datetime, timezone
import time

SESSION = HTMLSession()

all_gamelist_links = []
all_page_links = []
all_games = []

def extract_gamelists_links() -> None:
    """
    This function returns a list of URLs where games are grouped by a certain criteria. These URLs serves as input URL for further scraping.
    """
    base_url = 'https://www.gamerevolution.com/games/'
    response = SESSION.get(base_url)
    
    game_list_urls = list(response.html.find('div.list-navigation ul', first=True).absolute_links)
    game_list_urls.sort()
    
    [all_gamelist_links.append(x) for x in game_list_urls]
    return

def generate_page_links(gamelist_url: str) -> None:
    """
    This functions takes the gamelist URL as an input and generates the page URLs that are used to scrape games.
    Args:
        gamelist_url (str): The gamelist URL string
    Returns:
        This function appends the page links to 'all_page_links' list
    """
    
    print('\n')
    print(f'Collecting page links from: {gamelist_url}')
    
    response = SESSION.get(gamelist_url)
    
    last_page = int(response.html.find('div.list-pagination span.current ~a.page-numbers:nth-last-child(2)', first=True).text)
    
    for pgno in range(1, last_page+1):
        page_url = f'{gamelist_url}page/{pgno}'
        all_page_links.append(page_url)
        
    time.sleep(0.5)
    return

def scrape_content(page_url: str) -> None:
    """
    This function takes a page URL; scrapes all the game details and adds them to 'all_games' list
    Args:
        page_url (str): The page URL string 
    Returns:
        It returns nothing but, adds the scraped data to the list
    """
    
    utc_timezone = timezone.utc
    current_utc_timestamp = datetime.now(utc_timezone).strftime('%d-%b-%Y %H:%M:%S')
    
    response = SESSION.get(page_url)
    
    print('\n')
    print(f'Scraping details from: {page_url}')
    
    gamelist_type = response.html.find('div.list-search ~ h3.title', first=True).text.title()
    games_content = response.html.find('div.list-games ul:nth-child(2) >li')
    
    for game in games_content:
        gamelist_category = gamelist_type
        title = game.find('li.l-title a.list-table-title', first=True).text
        game_details_url = game.find('li.l-title a.list-table-title', first=True).attrs.get('href')
        rating = game.find('li.l-grade span.rating-points', first=True).text
        release_date = game.find('li.l-created', first=True).text
        
        try:
            game_cover_image = game.find('li.l-title a.list-table-image img', first=True).attrs.get('data-lazy-src')
        except:
            game_cover_image = None
        
        try:
            genre = game.find('li.l-genre', first=True).text
        except:
            genre = None
        
        try:
            publisher = game.find('li.l-publisher', first=True).text
        except:
            publisher = None
        
        game_details = {
            'title': title,
            'rating': rating,
            'genre': genre,
            'publisher': publisher,
            'release_date': release_date,
            'game_cover_image': game_cover_image,
            'game_details_url': game_details_url,
            'gamelist_category': gamelist_category,
            'last_updated_at_UTC': current_utc_timestamp
        }
        
        all_games.append(game_details)
        
    time.sleep(0.5)
    return

# Testing the scraper template #
# ---------------------------- #

if __name__ == '__main__':

    extract_gamelists_links()
    
    print('\n')
    print(f'Total gamelists to consider: {len(all_gamelist_links)}')
    print('\n')
    print(all_gamelist_links)
    
    gamelist_url = 'https://www.gamerevolution.com/games/g/'
    
    generate_page_links(gamelist_url)
    
    print('\n')
    print(f'Total pages to scrape: {len(all_page_links)}')
    print('\n')
    print(all_page_links)
    
    page_url = 'https://www.gamerevolution.com/games/g/page/3'
    scrape_content(page_url)
    
    print('\n')
    print(f'Total games scraped: {len(all_games)}')
    print('\n')
    print(all_games)