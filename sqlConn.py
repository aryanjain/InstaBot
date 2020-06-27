import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    #finally:
        #print("in finally")
        #if conn:
            #conn.close()
    
    return conn

def create(conn):
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS Engagements (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        LikeCount integer,
                                        FollowCount integer,
                                        Url text
                                    ); """
    if conn is not None:
        create_table(conn, sql_create_projects_table)
    else:
        print("database error")

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insertData(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO Engagements(LikeCount,FollowCount,Url)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    
    return cur.lastrowid