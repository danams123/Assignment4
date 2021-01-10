class Vaccine(object):
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity


class Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
                 INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
          """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines WHERE id = ?
        """, [vaccine_id])
        return Vaccine(*c.fetchone())

    def find_by_date(self):
        c = self._conn.cursor()
        c.execute("""SELECT * FROM vaccines ORDER BY date LIMIT 1""")
        return Vaccine(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT id, date, supplier, quantity FROM vaccines
        """).fetchall()
        return [Vaccine(*row) for row in all]

    def update(self, vaccine):
        self._conn.execute("""
               UPDATE vaccines SET quantity=(?) WHERE id=(?)
           """, [vaccine.quantity, vaccine.id])

    def delete(self, vaccine):
        self._conn.execute("""
                      DELETE FROM vaccines WHERE id=(?)
                  """, [vaccine.id])


