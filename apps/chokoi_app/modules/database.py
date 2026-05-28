from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://chokoi:cacao@localhost:5432/chokoi_db"
)

engine = create_engine(DATABASE_URL)

