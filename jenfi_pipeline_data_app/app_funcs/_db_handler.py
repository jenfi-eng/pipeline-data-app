from sqlalchemy import create_engine, MetaData, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base

from dotenv import load_dotenv


def init_db(self):
    db_config = self.db_config()

    self.db_engine = create_engine(db_config.SQL_ALCHEMY_CONN, echo=False)

    self.db = scoped_session(sessionmaker())
    self.db.configure(bind=self.db_engine)


def close_db(self):
    if self.db is not None:
        self.db.close()
        self.db = None


def db_config(self):
    if self.PYTHON_ENV == "production":
        from ..config import ProductionConfig

        db_config = ProductionConfig()
    elif self.PYTHON_ENV == "staging":
        from ..config import StagingConfig

        db_config = StagingConfig()
    else:
        # ONLY DEV - take environment variables from .env
        load_dotenv()

        from ..config import DevelopmentConfig

        db_config = DevelopmentConfig()

    return db_config
