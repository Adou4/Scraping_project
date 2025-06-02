from scraper.spider import BookScraper
from scraper.pipelines import DataPipeline
import logging
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    # Créer les dossiers si nécessaire
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # Scraping
    scraper = BookScraper()
    books_df = scraper.scrape_books(max_pages=2)
    
    # Sauvegarder les données brutes
    raw_path = 'data/raw/books_raw.csv'
    books_df.to_csv(raw_path, index=False)
    logging.info(f"Raw data saved to {raw_path}")
    
    # Traitement des données
    pipeline = DataPipeline()
    processed_df = pipeline.process(books_df)
    
    # Sauvegarder les données traitées
    processed_path = 'data/processed/books_processed.csv'
    pipeline.save_to_csv(processed_df, processed_path)
    
    db_path = 'data/processed/books.db'
    pipeline.save_to_sqlite(processed_df, db_path)
    
    logging.info(f"Processed data saved to {processed_path} and SQLite database")

if __name__ == "__main__":
    main()