import sqlite3


class DbInterface:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()


    def clear_products(self) -> None:
        sql = 'DELETE FROM Products'
        try:
            self.cursor.execute(sql)
            print("Data was removed succesfully")
        except Exception as e:
            print(f"ERROR {e}")
        finally:
            self.conn.commit()

    def add_products(self, promt: str, products: list) -> None:
        sql = 'INSERT INTO Products (promt, product) VALUES (?,?)'

        args = []
        for product in products:
            args.append((promt, product))
        try:
            self.cursor.executemany(sql, args)
        except Exception as e:
            print(f"ERROR {e}")
        finally:
            self.conn.commit()

    def add_no_products(self, perm):
        sql = 'INSERT INTO no_products (promt) VALUES (?)'

        args = [perm]
        try:
            self.cursor.execute(sql, args)
        except Exception as e:
            print(f"ERROR {e}")
        finally:
            self.conn.commit()

    def check_products(self):
        sql = 'SELECT DISTINCT promt FROM Products UNION SELECT DISTINCT promt FROM No_products'
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(f"ERROR {e}")
        finally:
            self.conn.commit()
        return [promt[0] for promt in self.cursor.fetchall()]

path = "products.db"
DB = DbInterface(path)
# DB.add_product("perm", ["query"])
# print(DB.check_products())
