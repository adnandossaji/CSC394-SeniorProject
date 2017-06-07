import sqlite3

def main():
    conn = sqlite3.connect('database.db')

    sql_file = open("seed.sql", "r").read()

    try:
        conn.executescript(sql_file)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()