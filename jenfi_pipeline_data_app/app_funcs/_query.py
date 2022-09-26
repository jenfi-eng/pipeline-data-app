from ..db_cache import DbCache

# Primary use point for Credit
# Should be able to help take snapshot of data and return the cache as necessary.
def df_query(self, query_str, rebuild_cache=False):
    db_cache = self._db_cache()

    return db_cache.df_query(query_str, rebuild_cache)


def query_one(self, query_str, rebuild_cache=False):
    db_cache = self._db_cache()

    return db_cache.query_one(query_str, rebuild_cache)


def query_all(self, query_str, rebuild_cache=False):
    db_cache = self._db_cache()

    return db_cache.query_all(query_str, rebuild_cache)


def _db_cache(self) -> None:
    (step_name, run_id) = self._run_data()
    bucket_name = self.s3_config.S3_DB_QUERY_CACHE_BUCKET

    return DbCache(
        self.db, self.db_engine, step_name, run_id, self.tmp_dir(), bucket_name
    )
