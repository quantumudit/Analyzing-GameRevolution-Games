from requests_html import HTMLSession

SESSION = HTMLSession()

all_games = []

def extract_gamelists() -> list:
    """
    This function returns a list of URLs where games are grouped by a certain criteria. These URLs serves as input URL for further scraping.
    """
    base_url = 'https://www.gamerevolution.com/games/'
    response = SESSION.get(base_url)
    game_list_urls = list(response.html.find('div.list-navigation ul', first=True).absolute_links)
    game_list_urls.sort()
    return game_list_urls

def lastpage_number(url: str) -> int:
    """
    This functions takes the gamelist URL and returns the last page number.
    Args:
        url (str): The gamelist URL string of the current page
    Returns:
        int: The last page number
    """
    
    response = SESSION.get(url)
    return int(response.html.find('div.list-pagination span.current ~a.page-numbers:nth-last-child(2)', first=True).text)
    
def extract_content(url: str) -> tuple:
    """
    This functions takes a game list URL and returns a tuple that has the gamelist name and HTML table content that has all the games and related information.

    Args: 
        url (str): The gamelist URL string
    Returns:
        tuple: Combination of gamelist category name and HTML Table content with different games in it.
    """
    
    response = SESSION.get(url)
    
    gamelist_type = response.html.find('div.list-search ~ h3.title', first=True).text.title()
    games = response.html.find('div.list-games ul:nth-child(2) >li')
    
    return (gamelist_type, games)

def scrape_content(content: tuple) -> None:
    """
    This function loops through each row of the content extracted from 'extract_content()' function, scrapes the required data and appends it to the 'all_games' list
    Args:
        content (tuple): Combination of gamelist category name and a HTML table content with different games in it. This tuple is extracted from 'extract_content()' function.
    Returns:
        None: It returns nothing but, appends all individual game and its metric dictionary to 'all_games' list
    """
    
    for game in content[1]:
        gamelist_category = content[0]
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
            'gamelist_category': gamelist_category
        }
        
        all_games.append(game_details)
    return



# Testing the scraper template #
# ---------------------------- #

if __name__ == '__main__':
    
    gamelists_categories = extract_gamelists()
    print(gamelists_categories)
    print('\n')
    
    URL = 'https://www.gamerevolution.com/games/a/'
    
    lastpage_num = lastpage_number(URL)
    print(f'The last page number is: {lastpage_num}')
    print('\n')
    
    content = extract_content(URL)
    scrape_content(content)
    
    print(f'Total Items Scraped: {len(all_games)}')
    print('\n')
    print(all_games)
    print('\n')