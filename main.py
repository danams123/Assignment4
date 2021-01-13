import sys
import sqlite3
import datetime

import Clinics
import Repository
import Suppliers
import Vaccines
import Logistics


def main(args):
    # vaccine_size is the counter of the vaccines id so the next time we insert a vaccine the id will be differend
    # than of the rest of te table
    vaccine_size = init(sys.argv[1])
    execute(sys.argv[2], sys.argv[3], vaccine_size)


def init(config):
    # Creating the tables and inserting the line from the config file
    first = 0
    with open(config) as inputfile:
        for line in inputfile:
            x = line.split(",")
            # first case - the first line of the output file with the sizes
            if first == 0:
                vaccine_size = int(x[0])
                size = vaccine_size
                supplier_size = int(x[1])
                clinic_size = int(x[2])
                logistic_size = int(x[3][:-1])
                first = 1
                # vaccines
            elif vaccine_size > 0:
                vaccine = Vaccines.Vaccine(int(x[0]), x[1], int(x[2]), int(x[3][:-1]))
                Repository.repo.vaccines.insert(vaccine)
                vaccine_size -= 1
                # suppliers
            elif supplier_size > 0:
                supplier = Suppliers.Supplier(int(x[0]), x[1], int(x[2][:-1]))
                Repository.repo.suppliers.insert(supplier)
                supplier_size -= 1
                # clinics
            elif clinic_size > 0:
                clinic = Clinics.Clinic(int(x[0]), x[1], int(x[2]), int(x[3][:-1]))
                Repository.repo.clinics.insert(clinic)
                clinic_size -= 1
                # logistics
            elif logistic_size > 0:
                # last line - doesnt have \n in the end
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
                Repository.repo.vaccines.insert(vaccine)
                # getting the logistic from the logistic id of the supplier
                logistic = Repository.repo.logistics.find(supplier.logistic)
                logistic.count_received += int(x[1])
                Repository.repo.logistics.update_received(logistic)
            else:
                clinic = Repository.repo.clinics.find(x[0])
                clinic.demand -= int(x[1])
                Repository.repo.clinics.update(clinic)
                logistic = Repository.repo.logistics.find(clinic.logistic)
                logistic.count_sent += int(x[1])
                Repository.repo.logistics.update_sent(logistic)
                amount = int(x[1])
                # the loop runs over the vaccines table and decreases their quantities until the amount to send is 0
                while amount > 0:
                    vaccine = Repository.repo.vaccines.find_by_date()
                    # if the vaccine quantity is bigger than the amount we just decrease it
                    if vaccine.quantity > amount:
                        vaccine.quantity -= amount
                        Repository.repo.vaccines.update(vaccine)
                        amount = 0
                    # else we delete the vaccine because its quantity is 0
                    else:
                        amount -= vaccine.quantity
                        Repository.repo.vaccines.delete(vaccine)
            # creating a new line of the totals required for the output file
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
    # we save each line in a string for each iteration and when the loop ends we write the whole string to the output
    # file
    with open(output, 'w') as f:
        f.write(s)
        f.close()


if __name__ == '__main__':
    main(sys.argv)