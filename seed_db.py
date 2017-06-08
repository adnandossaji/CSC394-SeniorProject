import sqlite3

def main():
    con = sqlite3.connect('../database.db')

    sql_file = open("seed.sql", "r").read()

    try:
        con.executescript(sql_file)
    except Exception as e:
        print(e)

    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())


if __name__ == "__main__":
    main()