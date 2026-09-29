from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/mi_api"

engine = create_engine(DATABASE_URL)