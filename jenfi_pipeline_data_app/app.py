import os
import platform
import tempfile
from pathlib import Path
import json
import inspect
import numpy as np
import pandas as pd

from sqlalchemy import create_engine, MetaData, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base

from dotenv import load_dotenv


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class Application(object):
    ROOT_DIR = os.path.abspath(os.curdir)
    RESULT_FILENAME = "output.json"
    PYTHON_ENV = os.getenv("PYTHON_ENV", "development")

    def boot(self):
        self.init_db()

    def cleanup(self):
        self.close_db()

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
            from .config import ProductionConfig

            db_config = ProductionConfig()
        elif self.PYTHON_ENV == "staging":
            from .config import StagingConfig

            db_config = StagingConfig()
        else:
            # ONLY DEV - take environment variables from .env
            load_dotenv()

            from .config import DevelopmentConfig

            db_config = DevelopmentConfig()

        return db_config

    def tmp_filepath(self, rel_filepath):
        if self.PYTHON_ENV == "production":
            tmp_path = "/tmp"
        elif self.PYTHON_ENV == "staging":
            tmp_path = "/tmp"
        else:
            tmp_path = Path(
                "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
            )

        return os.path.join(tmp_path, rel_filepath)

    # Primary use point for Credit
    # Should be able to help take snapshot of data and return the cache as necessary.
    def df_query(self, query_str):
        # if self.PYTHON_ENV == "production":
        #     # Make class that hashes query+company_id+credit_app+pipeline+run_number?
        #     # If the hash is the same as previously seen one in S3, download and return
        #     # Else run the query and save the data back up to S3.
        #     pass
        # else:
        #     pass

        return pd.read_sql(query_str, self.db_engine)

    # This is built specifically to handle loading test variables for papermill.
    # EXTREMELY brittle.
    def load_test_parameters(self, params_dict):
        import sys

        mod = sys.modules['__main__']

        for var_name, var_val in params_dict.items():
            try:
                # If this is defined by papermill or anyone else, we don't want to set it.
                eval(f"mod.{var_name}")
            except (NameError, AttributeError):
                # Papermill nor anyone else defined this variable, let's set it ourselves!
                setattr(mod, var_name, var_val)


    def write_model(self, pickel, pickel_name):
        # Upload Model => S3
        pass

    def load_model(self, pickel, pickel_name):
        # Model => S3 => Download Model
        pass

    def write_result(self, result):
        with open(self.tmp_filepath(self.RESULT_FILENAME), "w") as f:
            json.dump(result, f, cls=NpEncoder, default=str)

    def load_result(self):
        with open(self.tmp_filepath(self.RESULT_FILENAME), "r") as result:
            output_data = json.load(result)

            return output_data

    def __repr__(self):
        return self.__dict__
    
    def __test_direct_module__(self, mod):
        return eval("mod.var_defined_globally")

    # Most of these methods below don't work because of how jupyter runs code.
    def __test_access_global_var__(self):
        # https://stackoverflow.com/questions/1095543/get-name-of-calling-functions-module-in-python
        mod = inspect.getmodule(inspect.stack()[1][0])

        return eval("mod.var_defined_globally")

    def __test_set_global_var__(self):
        mod = inspect.getmodule(inspect.stack()[1][0])

        exec("mod.var_defined_globally = 'bar'")

        pass
