# Python Bank project
# Author: Jagadish Rao, Oct 2019


from pathlib import Path
import fileinput

filcount = 0
banktotchkacc = banktotsavacc = banktotchkamt = banktotsavamt = bankhibal = banklowbal = 0
bankcusthibal = bankcustlowbal = ""
path = Path("c:\pyproj\ABC_Bank\data")
mergedfil = "c:\\pyproj\\ABC_Bank\\data\\append.txt"


def write_to_file(infil, inrec):
    fil = open(infil, "a")
    fil.write(inrec)
    fil.close()


def process_file(fil):

    custhibal = custlowbal = ""
    lowbal = 999999999999
    hibal = sumchk = sumsav = numchkacc = numsavacc = numrecs = 0

    for line in fileinput.input(fil):
        fline = line.split(",")

        if "ID" in fline[0].upper():
            if filcount == 0:
                write_to_file(mergedfil, line)      # write the header into the merged file, only the first time
            continue

        bal = float(fline[-2])
        customer = fline[1] + " " + fline[2]

        if "CHECKING" in fline[-1].upper():         # track the number of checking accounts, total amount
            sumchk += bal
            numchkacc += 1
        else:
            if "SAVING" in fline[-1].upper():       # track the number of savings accounts, total amount
                sumsav += bal
                numsavacc += 1

        if bal > hibal:                             # set the highest, lowest customer
            hibal = bal
            custhibal = customer
        else:
            if bal < lowbal:
                lowbal = bal
                custlowbal = customer

        numrecs += 1

        write_to_file(mergedfil, line)              # write the input record into the merged file

    return custhibal, hibal, custlowbal, lowbal, sumchk, sumsav, numchkacc, numsavacc, numrecs


def drawline():
    print()
    print("-" * 45)


### Main program

for fhandle in path.glob("*.csv"):          # loop over the input files

    fret = process_file(fhandle)

    banktotchkacc += fret[6]                # total checking/savings in bank along with amounts
    banktotsavacc += fret[7]
    banktotchkamt += fret[4]
    banktotsavamt += fret[5]

    if filcount == 0:                      # customer with highest / lowest balance in bank
        bankcusthibal = fret[0]
        bankhibal = fret[1]
        bankcustlowbal = fret[2]
        banklowbal = fret[3]
    else:
        if fret[1] > bankhibal:
            bankcusthibal = fret[0]
            bankhibal = fret[1]
        if fret[3] < banklowbal:
            bankcustlowbal = fret[2]
            banklowbal = fret[3]


    drawline()

    print("File: " + str(filcount + 1) + "\n")
    print(fhandle)
    print("Data records: " + str(fret[8]))
    print("Max balance: " + fret[0] + ", $" + str(fret[1]))
    print("Min balance: " + fret[2] + ", $" + str(fret[3]))

    filcount += 1


drawline()
print("Summary: \n")
print("Total number of files: " + str(filcount))
print("Highest balance: " + bankcusthibal + ", $" + str(bankhibal))
print("Lowest balance : " + bankcustlowbal + ", $" + str(banklowbal))
print("Checking accounts: " + str(banktotchkacc) + ", Amount: $" + str(banktotchkamt))
print("Savings accounts : " + str(banktotsavacc) + ", Amount: $" + str(banktotsavamt))
drawline()

#############################################################################################################


