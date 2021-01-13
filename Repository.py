import sqlite3
import atexit

import Clinics
import Logistics
import Suppliers
import Vaccines


class _Repository(object):

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._conn.text_factory = bytes
        self.vaccines = Vaccines.Vaccines(self._conn)
        self.suppliers = Suppliers.Suppliers(self._conn)
        self.clinics = Clinics.Clinics(self._conn)
        self.logistics = Logistics.Logistics(self._conn)
        self.create_tables()

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
                CREATE TABLE vaccines (
                    id      INTEGER   PRIMARY KEY,
                    date    DATE      NOT NULL,
                    supplier INTEGER REFERENCES Supplier(id),
                    quantity INTEGER NOT NULL
                );

                CREATE TABLE suppliers (
                    id   INTEGER   PRIMARY KEY,
                    name  TEXT   NOT NULL,
                    logistic INTEGER REFERENCES Logistic(id)    
                );

                CREATE TABLE clinics (
                    id      INTEGER     PRIMARY KEY,
                    location  TEXT       NOT NULL,
                    demand   INTEGER     NOT NULL,
                    logistic INTEGER REFERENCES Logistic(id)    
                );
                
                CREATE TABLE logistics (
                    id   INTEGER   PRIMARY KEY,
                    name  TEXT   NOT NULL,
                    count_sent INTEGER NOT NULL,
                    count_received INTEGER  NOT NULL   
                );
                
            """)


repo = _Repository()
atexit.register(repo._close)
