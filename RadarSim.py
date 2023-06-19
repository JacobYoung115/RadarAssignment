from time import sleep, time
from random import random

class RadarSim:
    def __init__(self, intervalInSeconds=1.0, pkRatio=0.8):
        self.intervalInSeconds = intervalInSeconds
        self.pkRatio = pkRatio
        self.numDetections = 0
        self.numMissilesFired = 0
        self.numNeutralzed = 0
        self.numMisses = 0
    

    def reportStatus(self):
        print('\n---------------- STATUS REPORT ----------------')
        print(f'Total number of hostiles detected: {self.numDetections}')
        print(f'Total number of missiles fired: {self.numMissilesFired}')
        print(f'Total number of hostiles neutralized: {self.numNeutralzed}')
        print(f'Total number of missiles missed: {self.numMisses}')


    def convertToDecimal(self, binVal):
        bitLength = len(binVal)
        decimVal = 0
        for idx, char in enumerate(binVal):
            decimVal += (int(char)*(2**(bitLength-idx-1)))
        return decimVal


    def neutralizeTarget(self, numEvens, numOdds):
        if numOdds > numEvens:
            print('Hostile detected.', flush=True)
            self.numDetections += 1
            print('Deploying missile.', flush=True)
            self.numMissilesFired += 1
        
            if self.pkRatio > random():
                print('Target neutralized.', flush=True)
                self.numNeutralzed += 1
            else:
                print('Target NOT neutralized.', flush=True)
                self.numMisses += 1


    def analyzeRadar(self, radarLine):
        decimVals = []
        detections = radarLine.split(';')
        numEvens = 0
        numOdds = 0

        for idx, binVal in enumerate(detections):
            if idx == len(detections)-1:
                binVal = binVal[:len(binVal)-1]     #remove the newline character at the end.
            
            decimVal = self.convertToDecimal(binVal)
            decimVals.append(decimVal)
            #once the values are converted to decimal, check the number of odd value enteries vs even value entries.
            if decimVal % 2 == 0:
                numEvens += 1
            elif decimVal % 2 == 1:
                numOdds += 1
            
        print(decimVals, flush=True)
        self.neutralizeTarget(numEvens, numOdds)


    def readRadarFile(self, fileName, intervalInSeconds=1.0):
        starttime = time()
        passed = 0
        total = 0
        
        radarData = open(fileName)
        radarLine = radarData.readline()
        while radarLine != "":
            passed = intervalInSeconds - ((time() - starttime) % intervalInSeconds)
            total += passed

            self.analyzeRadar(radarLine)

            sleep(passed)
            radarLine = radarData.readline()

        radarData.close()


if __name__ == '__main__':
    simulation = RadarSim()
    simulation.readRadarFile('radar_data.csv')
    simulation.reportStatus()
    