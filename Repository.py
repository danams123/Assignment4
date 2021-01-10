import sqlite3
import atexit

import Clinics
import Logistics
import Suppliers
import Vaccines


# DTO objects
# class Vaccine(object):
#     def __init__(self, id, date, supplier, quantity):
#         self.id = id
#         self.date = date
#         self.supplier = supplier
#         self.quantity = quantity
#
#
# class Supplier(object):
#     def __init__(self, id, name, logistic):
#         self.id = id
#         self.name = name
#         self.logistic = logistic
#
#
# class Clinic(object):
#     def __init__(self, id, location, demand, logistic):
#         self.id = id
#         self.location = location
#         self.demand = demand
#         self.logistic = logistic
#
#
# class Logistic(object):
#     def __init__(self, id, name, count_sent, count_received):
#         self.id = id
#         self.name = name
#         self.count_sent = count_sent
#         self.count_received = count_received


# Repository
class _Repository(object):

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._conn.text_factory = bytes
        self.vaccines = Vaccines.Vaccines(self._conn)
        self.suppliers = Suppliers.Suppliers(self._conn)
        self.clinics = Clinics.Clinics(self._conn)
        self.logistics = Logistics.Logistics(self._conn)
        # self.vaccines = dao.dao(Vaccine, self._conn)
        # self.suppliers = dao.dao(Supplier, self._conn)
        # self.clinics = dao.dao(Clinic, self._conn)
        # self.logistics = dao.dao(Logistic, self._conn)
        self.create_tables()  # is it ok?


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
