import csv

def read_D(fileName):
    D = []
    with open(fileName) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            res = list(map(int, row))
            D.append(res)
    return D


def read_U(fileName):
    U = []
    utility_Dic = {}
    with open(fileName) as csvDataFile:
        _csvUtility = csv.reader(csvDataFile)
        for row in _csvUtility:
            U.append(row)
            utility_Dic[row[0]] = int(row[1])
    return utility_Dic, U
