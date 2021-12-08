import pandas as pd
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
from fx_games_scraper_template import *

def extract_all_page_links() -> None:
    """
    This function loops though each of the gamelist links and generates page links to scrape game details
    """
    
    with ThreadPoolExecutor() as executor:
        executor.map(generate_page_links, all_gamelist_links)
    return

def scrape_all_game_details() -> None:
    """
    This function loops through all the page links and scrapes the game details; that are get added to 'all_games' list
    """
    
    with ThreadPoolExecutor() as executor:
        executor.map(scrape_content, all_page_links)
    return

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    games_df = pd.DataFrame(all_games)
    games_df.to_csv('gr_games_raw_data.csv', encoding='utf-8', index=False)
    return

if __name__ == '__main__':
    
    scraper_title = "GAMEREVOLUTION GAMES COLLECTOR"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    start_time = datetime.now()
    
    print('\n\n')
    print(ascii_art_title)
    print('Collecting Games...')
    
    extract_gamelists_links()
    
    print(f'Total gamelists to consider: {len(all_gamelist_links)}')
    print('Gathering all page links to scrape...')
    
    extract_all_page_links()
    
    print(f'Total pages to scrape: {len(all_page_links)}')
    print('\n')
    print('Scraping game details from each page link...')
    
    scrape_all_game_details()
    
    end_time = datetime.now()
    scraping_time = end_time - start_time
    
    print('\n')
    print('All Games Collected...')
    print(f'Time spent on scraping: {scraping_time}')
    print(f'Total games collected: {len(all_games)}')
    print('\n')
    print('Loading data into CSV...')
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Webscraping Completed !!!')