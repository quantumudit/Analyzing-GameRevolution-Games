import pandas as pd
import asyncio
import time
import pyfiglet
from fx_gamerevolution_games_scraper_template import *

GAMELIST_URLS = extract_gamelists()

async def gamelist_scraper(games_url: str) -> None:
    """
    This functions takes a gamelist URL as input and scrapes all the games related to that particular gamelist.
    Args:
        url (str): The gamelist URL
    Returns:
        None: This function adds games to the 'all_games' list
    """
        
    last_page_num = lastpage_number(games_url)
    
    print('\n')
    print(f'Total pages to scrape: {last_page_num}')
    
    for pgno in range(1, last_page_num+1):
        
        url = f'{games_url}page/{pgno}'
        
        print('\n')
        print(f'Scraping Page: {pgno}')
        print(f'Scaping Page URL: {url}')
        
        content = extract_content(url)
        scrape_content(content)
        
        print(f'Total games scraped: {len(all_games)}')
        print(f'Page-{pgno} Scraped...')
        print(f'Remaining pages to scrape: {last_page_num - pgno}')
        
    await asyncio.sleep(1)
    return

async def main() -> None:
    """
    This function loops through each gamelist URLs and calls child functions to load data into 'all_games' list
    """
        
    loop_counter=0
    
    for games_url in GAMELIST_URLS:
        print('\n')
        print(f'Gamelist URL to scrape: {games_url}')
        
        task = asyncio.create_task(gamelist_scraper(games_url))
        
        loop_counter += 1
        print(f'Remaining gamelist URLs to scrape: {total_gamelist_urls - loop_counter}')
        await task
    await asyncio.sleep(1)

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    games_df = pd.DataFrame(all_games)
    games_df.to_csv('gamerevolution_games_data.csv', index=False)

if __name__ == '__main__':
    
    scraper_title = "GAMEREVOLUTION GAMES COLLECTOR"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    print('\n\n')
    print(ascii_art_title)
    print('Collecting Games...')
    
    total_gamelist_urls = len(GAMELIST_URLS)
    
    start_time = time.perf_counter()
    
    asyncio.run(main())
    
    end_time = time.perf_counter()
    
    scraping_time = start_time - end_time
    
    print('\n')
    print('All Games Collected...')
    print(f'Time spent on scraping: {scraping_time} seconds')
    print(f'Total beers grabbed: {len(all_games)}')
    print('\n')
    print('Loading data into CSV...')
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Webscraping completed !!!')