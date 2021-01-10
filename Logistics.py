from Clinics import Clinic


class Logistic(object):
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


class Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
                 INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
          """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM logistics WHERE id = ?
        """, [logistic_id])
        return Logistic(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT id, name, count_sent, count_received FROM logistics
        """).fetchall()
        return [Logistic(*row) for row in all]

    def update_received(self, logistic):
        self._conn.execute("""
               UPDATE logistics SET count_received=(?) WHERE id=(?)
           """, [logistic.count_received, logistic.id])

    def update_sent(self, logistic):
        self._conn.execute("""
               UPDATE logistics SET count_sent=(?) WHERE id=(?)
           """, [logistic.count_sent, logistic.id])


