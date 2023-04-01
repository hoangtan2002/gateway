def writecsv(temp, humid):
    csvFile = open("data.csv", "w")
    csvFile.write(str(temp) + ',' + str(humid) + '\n')
    csvFile.close()