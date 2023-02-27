from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///dank-downloader.db", echo=True)

