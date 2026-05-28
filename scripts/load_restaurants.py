import pandas as pd
from pathlib import Path
import importlib.util
import sys

# Load db_service without triggering app.services __init__
# Directly create a SQLAlchemy engine using the same DB URL as the app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pathlib

# Database URL (matches app/config.py)
DATABASE_URL = f"sqlite:///{pathlib.Path(r'C:\\Users\\david\\Documents\\_open_code_or\\restaurant_system\\restaurant.db')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Load Restaurant model directly
spec2 = importlib.util.spec_from_file_location('restaurant', r'C:\Users\david\Documents\_open_code_or\restaurant_system\app\models\db_base.py')
mod2 = importlib.util.module_from_spec(spec2)
sys.modules['restaurant'] = mod2
spec2.loader.exec_module(mod2)
Restaurant = mod2.Restaurant

EXCEL_PATH = Path(r'C:\Users\david\Documents\_open_code_or\restaurants.xlsx')

def load_restaurants():
    df = pd.read_excel(EXCEL_PATH, engine='openpyxl')
    expected_cols = {
        'name', 'address', 'google_place_url', 'google_map_url',
        'website_url', 'yelp_url', 'visited_yn', 'avg_score', 'review_count'
    }
    missing = expected_cols - set(df.columns.str.lower())
    if missing:
        raise ValueError(f'Missing columns in Excel: {missing}')
    df.columns = df.columns.str.lower()
    with SessionLocal() as db:
        for _, row in df.iterrows():
            restaurant = Restaurant(
                name=row.get('name'),
                address=row.get('address'),
                google_place_url=row.get('google_place_url'),
                google_map_url=row.get('google_map_url'),
                website_url=row.get('website_url'),
                yelp_url=row.get('yelp_url'),
                visited_yn=bool(row.get('visited_yn')) if pd.notna(row.get('visited_yn')) else False,
                avg_score=float(row.get('avg_score')) if pd.notna(row.get('avg_score')) else 0.0,
                review_count=int(row.get('review_count')) if pd.notna(row.get('review_count')) else 0,
            )
            db.add(restaurant)
        db.commit()
    print('Loaded', len(df), 'restaurants.')

if __name__ == '__main__':
    load_restaurants()
