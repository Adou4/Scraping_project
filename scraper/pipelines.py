import pandas as pd
import sqlite3
from datetime import datetime
import re

class DataPipeline:
    def __init__(self):
        self.cleaning_functions = {
            'price': self._clean_price,
            'price_excl_tax': self._clean_price,
            'price_incl_tax': self._clean_price,
            'tax': self._clean_price,
            'reviews': self._clean_integer,
            'rating': self._clean_rating
        }
    
    def process(self, df):
        """Nettoyer et transformer les données"""
        # Appliquer les fonctions de nettoyage
        for column, func in self.cleaning_functions.items():
            if column in df.columns:
                df[column] = df[column].apply(func)
        
        # Ajouter des métadonnées
        df['scraped_at'] = datetime.now()
        
        return df
    
    def _clean_price(self, value):
        """Convertir les prix en float"""
        if isinstance(value, str):
            return float(re.sub(r'[^\d.]', '', value))
        return value
    
    def _clean_integer(self, value):
        """Convertir en entier"""
        if isinstance(value, str):
            return int(re.sub(r'[^\d]', '', value))
        return value
    
    def _clean_rating(self, value):
        """Convertir les évaluations en nombre (One -> 1)"""
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        return rating_map.get(value, 0)
    
    def save_to_csv(self, df, path):
        """Sauvegarder en CSV"""
        df.to_csv(path, index=False)
    
    def save_to_sqlite(self, df, db_path, table_name='books'):
        """Sauvegarder en base de données SQLite"""
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()