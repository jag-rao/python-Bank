# Python Bank project
# Author: Jagadish Rao, Oct 2019


from pathlib import Path
import fileinput

filcount = banktotchkacc = banktotsavacc = banktotchkamt = banktotsavamt = bankhibal = banklowbal = 0
filhibal = fillowbal = filsumchk = filsumsav = filnumchkacc = filnumsavacc = filnumrecs = 0
bankcusthibal = bankcustlowbal = filcusthibal = filcustlowbal = ""

path = Path("c:\pyproj\ABC_Bank\data")
mergedfil = "c:\\pyproj\\ABC_Bank\\data\\append.txt"


def drawline():
    print()
    print("-" * 45)


def write_to_file(infil, inrec):
    fil = open(infil, "a")
    fil.write(inrec)
    fil.close()


def process_file(fil):

# process the provided input file to identify all relevent data points and return to caller

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



### Main program

for fhandle in path.glob("*.csv"):          # loop over the input files

    fret = process_file(fhandle)

    filcusthibal, filhibal, filcustlowbal, fillowbal, filsumchk, filsumsav, filnumchkacc, filnumsavacc, filnumrecs  = fret     # return values from each file

    banktotchkacc += filnumchkacc               # total checking/savings in bank along with amounts
    banktotsavacc += filnumsavacc
    banktotchkamt += filsumchk
    banktotsavamt += filsumsav

    if filcount == 0:
        bankcusthibal = filcusthibal
        bankhibal = filhibal
        bankcustlowbal = filcustlowbal
        banklowbal = fillowbal
    else:
        if filhibal > bankhibal:
            bankcusthibal = filcusthibal
            bankhibal = filhibal
        if fillowbal < banklowbal:
            bankcustlowbal = filcustlowbal
            banklowbal = fillowbal


    drawline()

    print("File: " + str(filcount + 1) + "\n")
    print(fhandle)
    print("Data records: " + str(filnumrecs))
    print("Max balance: " + filcusthibal + ", $" + str(filhibal))
    print("Min balance: " + filcustlowbal + ", $" + str(fillowbal))

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


