import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time
import logging

class BookScraper:
    def __init__(self, base_url="http://books.toscrape.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        self.data = []
        
    def scrape_books(self, max_pages=5):
        """Scrape les livres sur plusieurs pages"""
        url = self.base_url
        for page in range(1, max_pages + 1):
            self.logger.info(f"Scraping page {page}")
            
            try:
                response = self.session.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                self._scrape_page(soup)
                
                next_button = soup.select_one('li.next > a')
                if not next_button:
                    break
                    
                url = urljoin(self.base_url, next_button['href'])
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error scraping page {page}: {e}")
                break
                
        return pd.DataFrame(self.data)
    
    def _scrape_page(self, soup):
        """Extraire les données des livres d'une page"""
        books = soup.select('article.product_pod')
        
        for book in books:
            try:
                title = book.h3.a['title']
                price = book.select_one('p.price_color').text
                availability = book.select_one('p.instock').text.strip()
                rating = book.p['class'][1]
                
                detail_url = urljoin(self.base_url, book.h3.a['href'])
                details = self._scrape_details(detail_url)
                
                book_data = {
                    'title': title,
                    'price': price,
                    'availability': availability,
                    'rating': rating,
                    **details
                }
                
                self.data.append(book_data)
                
            except Exception as e:
                self.logger.error(f"Error scraping book: {e}")
    
    def _scrape_details(self, url):
        """Extraire les détails depuis la page d'un livre"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            details = {
                'upc': soup.find('th', text='UPC').find_next_sibling('td').text,
                'product_type': soup.find('th', text='Product Type').find_next_sibling('td').text,
                'price_excl_tax': soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text,
                'price_incl_tax': soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text,
                'tax': soup.find('th', text='Tax').find_next_sibling('td').text,
                'reviews': soup.find('th', text='Number of reviews').find_next_sibling('td').text,
                'description': soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text if soup.find('div', {'id': 'product_description'}) else None
            }
            
            return details
            
        except Exception as e:
            self.logger.error(f"Error scraping details from {url}: {e}")
            return {}