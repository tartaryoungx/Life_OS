import psycopg2
import time
from app.config import settings
from psycopg2.extras import Json, RealDictCursor
from psycopg2.pool import SimpleConnectionPool
import logging

logger = logging.getLogger(__name__)

pool = None
if settings.DATABASE_URL:
    try:
        pool = SimpleConnectionPool(1, 20, dsn=settings.DATABASE_URL)
        print("Successfully initialized PostgreSQL Connection Pool (Railway).")
    except Exception:
        logger.exception("Failed to initialize PostgreSQL Connection Pool.")
        raise
else:
    print("Warning: DATABASE_URL is not configured.")

def get_db():
    if pool is None:
        raise RuntimeError("Database pool is not initialized")
    return Database(pool)
class Database:
    def __init__(self, pool):
        self.pool = pool

    def table(self, table_name):
        return QueryBuilder(table_name, self)
    
    def execute_raw(self, sql, params):
        start = time.perf_counter()
        conn = None
        try:
            conn = self.pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)

                data = []
                if cur.description:
                    data = cur.fetchall()
            conn.commit()
            end = time.perf_counter()
            execution_time = end - start
            return ExecutionResult(data, execution_time, sql)

        except psycopg2.Error:
            logger.exception("Database Error")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn and self.pool:
                self.pool.putconn(conn)


    
class QueryBuilder:
    def __init__(self, table_name, db):
        self.table_name = table_name
        self.db = db
        self.operation = None
        self.columns = "*"
        self.conditions = []
        self.params = []
        self.insert_data = None
        self.update_data = None

    def select(self, columns="*"):
        self.operation = "select"
        self.columns = columns
        return self

    def insert(self, data):
        self.operation = "insert"
        self.insert_data = data
        return self

    def upsert(self, data):
        self.operation = "upsert"
        self.insert_data = data
        return self

    def update(self, data):
        self.operation = "update"
        self.update_data = data
        return self

    def delete(self):
        self.operation = "delete"
        return self

    def eq(self, column, value):
        self.conditions.append(f"{column} = %s")
        self.params.append(value)
        return self
    
    def operation_handler(self):
        sql = ""
        params = []
        if self.operation == "select":
            sql = f"SELECT {self.columns} FROM {self.table_name}"
            if self.conditions:
                sql += " WHERE " + " AND ".join(self.conditions)
                params = self.params
        
        elif self.operation == "insert":
            if isinstance(self.insert_data, dict):
                keys, vals, placeholders = insert(self.insert_data)
                sql = f"INSERT INTO {self.table_name} ({', '.join(keys)}) VALUES ({placeholders}) RETURNING *"
                params = vals

        elif self.operation == "upsert":
            if isinstance(self.insert_data, dict):
                sql, vals = upsert(self.insert_data, self.table_name)
                params = vals
        
        elif self.operation == "update":
            if isinstance(self.update_data, dict):
                set_clauses, vals = update(self.update_data)
                sql = f"UPDATE {self.table_name} SET {', '.join(set_clauses)}"
                params = vals

                if self.conditions:
                    sql += " WHERE " + " AND ".join(self.conditions)
                    params.extend(self.params)
                sql += " RETURNING *"

        elif self.operation == "delete":
            sql = f"DELETE FROM {self.table_name}"
            if self.conditions:
                sql += " WHERE " + " AND ".join(self.conditions)
                params = self.params
            sql += " RETURNING *"

        return sql, params

    def execute(self):
        if self.operation in ("update", "delete") and not self.conditions:
            raise ValueError(f"{self.operation.upper()} requires WHERE condition")
        
        sql, params = self.operation_handler()
        if not sql:
            print("Invalid operation")
            raise ValueError(f"Invalid operation or uninitialized QueryBuilder state.")
        
        return self.db.execute_raw(sql, params)

class ExecutionResult:
    def __init__(
            self,
            data,
            execution_time,
            sql,
            ):
        self.data = data
        self.execution_time = f"{execution_time} s"
        self.sql = sql

def insert(insert_data):
    keys, vals = prepare_data(insert_data)
    
    placeholders = ", ".join(["%s"] * len(keys))

    return keys, vals, placeholders

def upsert(insert_data, table_name):
    keys, vals = prepare_data(insert_data)
    conflict_target = "user_id" if table_name == "sessions" else "id"
    placeholders = ", ".join(["%s"] * len(keys))
    updates = ", ".join([f"{k} = EXCLUDED.{k}" for k in keys if k != conflict_target])
    sql = f"""
            INSERT INTO {table_name} ({', '.join(keys)}) 
            VALUES ({placeholders}) 
            ON CONFLICT ({conflict_target}) 
            DO UPDATE SET {updates} 
            RETURNING *
        """
    return sql, vals

def update(update_data):
    keys, vals = prepare_data(update_data)
    set_clauses = [f"{k} = %s" for k in keys]
    return set_clauses, vals

def prepare_data(data):
    keys = list(data.keys())
    vals = []

    for k in keys:
        v = data[k]
        if isinstance(v, (list, dict)):
            vals.append(Json(v))
        else:
            vals.append(v)

    return keys, vals

"""
# DB easy logic
    conn = psycopg2.connect(settings.DATABASE_URL)
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    return rows
"""