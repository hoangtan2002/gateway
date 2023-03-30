def writecsv(temp, humid):
    csvFile = open("data.csv", "a")
    csvFile.write(str(temp) + ',' + str(humid) + '\n')
    csvFile.close()