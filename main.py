# import sys
# import sqlite3
# import datetime
#
# import Repository
# import dao
#
#
# def main(args):
#     vaccine_size = init(sys.argv[1])
#     execute(sys.argv[2], sys.argv[3], vaccine_size)
#
#
# def init(config):
#     # Creating the tables and inserting the line from the config file
#     first = 0
#     with open(config) as inputfile:
#         for line in inputfile:
#             x = line.split(",")
#             if first == 0:
#                 vaccine_size = int(x[0])
#                 size = vaccine_size
#                 supplier_size = int(x[1])
#                 clinic_size = int(x[2])
#                 logistic_size = int(x[3][:-1])
#                 first = 1
#             elif vaccine_size > 0:
#                 vaccine = Repository.Vaccine(int(x[0]), x[1], int(x[2]), int(x[3][:-1]))
#                 Repository.repo.vaccines.insert(vaccine)
#                 vaccine_size -= 1
#             elif supplier_size > 0:
#                 supplier = Repository.Supplier(int(x[0]), x[1], int(x[2][:-1]))
#                 Repository.repo.suppliers.insert(supplier)
#                 supplier_size -= 1
#             elif clinic_size > 0:
#                 clinic = Repository.Clinic(int(x[0]), x[1], int(x[2]), int(x[3][:-1]))
#                 Repository.repo.clinics.insert(clinic)
#                 clinic_size -= 1
#             elif logistic_size > 0:
#                 logistic = Repository.Logistic(int(x[0]), x[1], int(x[2]), int(x[3][:-1]))
#                 Repository.repo.logistics.insert(logistic)
#                 logistic_size -= 1
#     return size
#
#
# def execute(orders, output, vaccine_size):
#     # a while the input file isn't empty loop that has if and else on the type of order and does the fitting actions
#     # after each iteration, getting the current status and inserting it to the output file
#     with open(orders) as inputfile:
#         for line in inputfile:
#             x = line.split(",")
#             if len(x) == 3:
#                 # getting the supplier of the supplier id in the shipment
#                 supplier = Repository.repo.suppliers.find({'name': x[0]})
#                 # creating a new vaccine object to add to the table of vaccines
#                 vaccine = Repository.Vaccine(vaccine_size + 1, x[2], supplier.id, x[1])
#                 # adding the vaccine to the table
#                 Repository.repo.vaccines.insert(vaccine)
#                 # getting the logistic from the logistic id of the supplier
#                 logistic = Repository.repo.logistics.find({'id': supplier.logistic})
#                 # updating the logistics table with the id of the logistic in the count received
#                 Repository.repo.logistics.update({'count_received': logistic.count_received + x[1]}, {'id': logistic.logistic})
#             else:
#                 clinic = Repository.repo.clinics.find({'location': x[0]})
#                 Repository.repo.clinics.update({'demand': clinic.demand - x[1]}, {'id': clinic.id})
#                 logistic = Repository.repo.logistics.find({'id': clinic.logistic})
#                 Repository.repo.logistics.update({'count_sent': logistic.count_sent + x[1]},
#                                                  {'id': logistic.id})
#                 amount = x[1]
#                 while amount > 0:
#                     vaccine = Repository.repo.vaccines.find_by_date()
#                     if vaccine.quantity > amount:
#                        Repository.repo.vaccines.update({'quantity': vaccine.quantity - amount}, {'id': vaccine.id})
#                        amount = 0
#                     else:
#                         Repository.repo.vaccines.delete({'id': vaccine.id})
#                         amount -= vaccine.quantity
#
#             amount = 0
#             for vaccine in Repository.repo.vaccines.find_all():
#                 amount += vaccine.quantity
#             demand = 0
#             for clinic in Repository.repo.clinics.find_all():
#                 demand += clinic.demand
#             received = 0
#             sent = 0
#             for logistic in Repository.repo.logistics.find_all():
#                 received += logistic.count_received
#                 sent += logistic.count_sent
#             str = amount + "," + demand + "," + received + "," + sent
#             output.write(str)
#     output.close()
#
#
# if __name__ == '__main__':
#     main(sys.argv)

#TODO check what happens if we have more amount in the input than the vaccines we actually have
#TODO check how we get the supplier from the supplier name which is not a primary key and another thing

import sys
import sqlite3
import datetime

import Clinics
import Repository
import Suppliers
import Vaccines
import Logistics


def main(args):
    vaccine_size = init(sys.argv[1])
    execute(sys.argv[2], sys.argv[3], vaccine_size)


def init(config):
    # Creating the tables and inserting the line from the config file
    first = 0
    with open(config) as inputfile:
        for line in inputfile:
            x = line.split(",")
            if first == 0:
                vaccine_size = int(x[0])
                size = vaccine_size
                supplier_size = int(x[1])
                clinic_size = int(x[2])
                logistic_size = int(x[3][:-1])
                first = 1
            elif vaccine_size > 0:
                vaccine = Vaccines.Vaccine(int(x[0]), x[1], int(x[2]), int(x[3][:-1]))
                Repository.repo.vaccines.insert(vaccine)
                vaccine_size -= 1
            elif supplier_size > 0:
                supplier = Suppliers.Supplier(int(x[0]), x[1], int(x[2][:-1]))
                Repository.repo.suppliers.insert(supplier)
                supplier_size -= 1
            elif clinic_size > 0:
                clinic = Clinics.Clinic(int(x[0]), x[1], int(x[2]), int(x[3][:-1]))
                Repository.repo.clinics.insert(clinic)
                clinic_size -= 1
            elif logistic_size > 0:
                if logistic_size == 1:
                    count_received = int(x[3])
                else:
                    count_received = int(x[3][:-1])
                logistic = Logistics.Logistic(int(x[0]), x[1], int(x[2]), count_received)
                Repository.repo.logistics.insert(logistic)
                logistic_size -= 1
    return size


def execute(orders, output, vaccine_size):
    s = ''
    # a while the input file isn't empty loop that has if and else on the type of order and does the fitting actions
    # after each iteration, getting the current status and inserting it to the output file
    with open(orders) as inputfile:
        for line in inputfile:
            x = line.split(",")
            if len(x) == 3:
                # getting the supplier of the supplier id in the shipment
                supplier = Repository.repo.suppliers.find(x[0])
                # creating a new vaccine object to add to the table of vaccines
                vaccine_size += 1
                vaccine = Vaccines.Vaccine(vaccine_size, x[2], supplier.id, x[1])
                # adding the vaccine to the table
                Repository.repo.vaccines.insert(vaccine)
                # getting the logistic from the logistic id of the supplier
                logistic = Repository.repo.logistics.find(supplier.logistic)
                logistic.count_received += int(x[1])
                # updating the logistics table with the id of the logistic in the count received
                Repository.repo.logistics.update_received(logistic)
            else:
                clinic = Repository.repo.clinics.find(x[0])
                clinic.demand -= int(x[1])
                Repository.repo.clinics.update(clinic)
                logistic = Repository.repo.logistics.find(clinic.logistic)
                logistic.count_sent += int(x[1])
                Repository.repo.logistics.update_sent(logistic)
                amount = int(x[1])
                while amount > 0:
                    vaccine = Repository.repo.vaccines.find_by_date()
                    if vaccine.quantity > amount:
                        vaccine.quantity -= amount
                        Repository.repo.vaccines.update(vaccine)
                        amount = 0
                    else:
                        amount -= vaccine.quantity
                        Repository.repo.vaccines.delete(vaccine)

            amount = 0
            for vaccine in Repository.repo.vaccines.find_all():
                amount += vaccine.quantity
            demand = 0
            for clinic in Repository.repo.clinics.find_all():
                demand += clinic.demand
            received = 0
            sent = 0
            for logistic in Repository.repo.logistics.find_all():
                received += logistic.count_received
                sent += logistic.count_sent
            s += str(amount) + "," + str(demand) + "," + str(received) + "," + str(sent) + "\n"

    with open(output, 'w') as f:
        f.write(s)
        f.close()


if __name__ == '__main__':
    main(sys.argv)

# TODO check what happens if we have more amount in the input than the vaccines we actually have
# TODO check how we get the supplier from the supplier name which is not a primary key and another thing