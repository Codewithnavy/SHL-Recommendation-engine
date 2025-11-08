import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SHL_CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"
    DATA_DIR = "data"
    ASSESSMENTS_FILE = os.path.join(DATA_DIR, "assessments.json")
    TRAIN_FILE = os.path.join(DATA_DIR, "train_set.csv")
    TEST_FILE = os.path.join(DATA_DIR, "test_set.csv")
    MIN_RECOMMENDATIONS = 5
    MAX_RECOMMENDATIONS = 10
    EMBEDDING_MODEL = "models/embedding-001"
    
settings = Settings()
