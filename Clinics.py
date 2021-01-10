class Clinic(object):
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
                 INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
          """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_location):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE location = ?
        """, [clinic_location])
        return Clinic(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT id, location, demand, logistic FROM clinics
        """).fetchall()
        return [Clinic(*row) for row in all]

    def update(self, clinic):
        self._conn.execute("""
               UPDATE clinics SET demand=(?) WHERE id=(?)
           """, [clinic.demand, clinic.id])


