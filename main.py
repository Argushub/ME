import tkinter as tk
from tkinter import ttk
from PIL import Image
from PIL import ImageTk


class CharacterRaceList:
    
    def __init__(self, parent, racePreview, gag):
        self.parent = parent
        self.characteNameRaceList = [gag.raceName]
        self.characterRaceList = [gag]
        self.currentRaceName = tk.StringVar()
        self.currentRace = gag
        self.previusRace = None
        self.comboBox = ttk.Combobox(self.parent, values = self.characteNameRaceList, textvariable = self.currentRaceName, state = "readonly", font='arial 14')
        self.comboBox.set(self.characteNameRaceList[0])
        self.comboBox.bind("<<ComboboxSelected>>", self.chooseRace)
        self.racePreview = racePreview
        self.buttonsList = []
        self.specials = None
    
    def addSpec(self, specials):
        self.specials = specials
        
    def addRaceToList(self, race):
        self.characterRaceList.append(race)
        self.characteNameRaceList.append(race.raceName)
        self.comboBox['values'] = self.characteNameRaceList
            
    def chooseRace(self, event):
        self.racePreview.changeImage(self.characteNameRaceList[self.comboBox.current()])
        self.currentRace = self.characterRaceList[self.comboBox.current()]
        for curRace in self.characterRaceList:
            curRace.resetStats()
        self.update()
    
    def update(self):
        for stats in self.buttonsList:
            stats.updateStats()
            stats.resetPrize()
        self.specials.update()
        if self.characterRaceList[self.comboBox.current()].metaPrizeStats == 0:      
            for button in self.buttonsList:
                if button.displayButton:
                    button.prizeButton.grid_remove()
        else:
            for button in self.buttonsList:
                if button.displayButton:
                    button.prizeButton.grid()            
    def addStats(self, stats):
        self.buttonsList.append(stats)
        
        
    def display(self):
        self.comboBox.grid(row = 0, column = 0, columnspan = 4)
        

        
class CharacterRacePreview:
    
    def __init__(self, parent, pathToGagImg):
        self.parent = parent
        self.widthImg = 320
        self.heightImg = 480
        self.characterRaceDict = {}
        self.addRacePreview(raceName = "Choose Race", pathToManImage = pathToGagImg, pathToWomanImage = pathToGagImg)
        self.currentRace = "Choose Race"
        self.currentRaceSex = "man"
        self.buttonMaleSex = tk.Button(self.parent, text = "Man", command = self.switchSexToMale, font='arial 14')
        self.buttonFemaleSex = tk.Button(self.parent, text = "Woman", command = self.switchSexToFemale, font='arial 14')
        race = self.characterRaceDict.get(self.currentRace)
        self.image = tk.Label(self.parent, image = race.get(self.currentRaceSex))
        self.characterList = None
        
    def addRacePreview(self, raceName, pathToManImage, pathToWomanImage = None):
        if pathToWomanImage == None:
            pathToWomanImage = pathToManImage
        manPreImage = Image.open(pathToManImage)     
        womanPreImage = Image.open(pathToWomanImage)
        manPreImage = manPreImage.resize((self.widthImg, self.heightImg), Image.ANTIALIAS)
        womanPreImage = womanPreImage.resize((self.widthImg, self.heightImg), Image.ANTIALIAS) 
        manImage =  ImageTk.PhotoImage(manPreImage)
        womanImage =  ImageTk.PhotoImage(womanPreImage)
        self.imageDict = {"man": manImage, "woman": womanImage}
        self.characterRaceDict[raceName] = self.imageDict
        
    def switchSexToMale(self):
        self.currentRaceSex = "man"
        self.changeImage(self.currentRace)
    
    def switchSexToFemale(self):
        self.currentRaceSex = "woman"
        self.changeImage(self.currentRace)        
        
    def display(self):
        self.image.grid(row = 0, column = 0, columnspan = 2, sticky = "n")
        self.buttonFemaleSex.grid(row = 1, column = 0, sticky = "ew")
        self.buttonMaleSex.grid(row = 1, column = 1, sticky = "ew")
        
    def addCharacterList(self, characterList):
        self.characterList = characterList
    
    def changeImage(self, currentRace):
        self.currentRace = currentRace
        raceDict = self.characterRaceDict.get(self.currentRace)
        self.image.config(image = raceDict.get(self.currentRaceSex))

    
class MetaCharacterRace:
    
    def __init__(self, raceName, pathToManImage, pathToWomanImage):
        self.raceName = raceName
        self.pathToManImage = pathToManImage
        self.pathToWomanImage = pathToWomanImage
        self.statsDict = {"Сила": 10, "Ловкость": 10, "Телосложение": 10,
"Интеллект": 10, "Мудрость": 10, "Харизма": 10, "Скорость": 30}
        self.metaStatsDict = self.statsDict.copy()
        self.prizeStats = 0
        self.metaPrizeStats = self.prizeStats
        self.statsPoints = 15
        self.metaStatsPoints = self.statsPoints
        self.specialAbilities = {}
    
    def addSpec(self, specialAbilities):
        self.specialAbilities = specialAbilities        
    
    def resetStats(self):
        self.statsDict = self.metaStatsDict.copy()
        self.prizeStats = self.metaPrizeStats
        self.statsPoints = self.metaStatsPoints
        
    def addToRaceList(self, raceList):
        raceList.addRaceToList(self)
        
    def addToRacePreview(self, racePreview):
        racePreview.addRacePreview(self.raceName, self.pathToManImage, self.pathToWomanImage)
        
    def raceStats(self, raceStatsDict, prize = 0):
        for raceStats in raceStatsDict.keys():
            for metaStats in self.statsDict.keys():
                if raceStats == metaStats:
                    self.statsDict[metaStats] += raceStatsDict[raceStats]
        self.metaStatsDict = self.statsDict.copy()
        self.prizeStats = prize
        self.metaPrizeStats = self.prizeStats


class StatsInfo:
    
    def __init__(self, parent, statsName, raceList, info, statsRow, displayButton = True):
        self.parent = parent
        self.statsName = statsName
        self.raceList = raceList
        race = raceList.currentRace
        self.statsValue = race.statsDict.get(self.statsName)
        self.label = tk.Label(self.parent, text = self.statsName+"\n"+str(self.statsValue), font='arial 14')
        self.addButton = None
        self.subButton = None
        self.prizeButton = None
        self.prize = True
        self.info = info
        self.statsRow = statsRow
        self.displayButton = displayButton
        self.addStatsButtons()
     
    def resetPrize(self):
        self.prize = True
        self.prizeButton.config(bg = "gray")
        
    def updateStats(self):
        race = self.raceList.currentRace        
        self.statsValue = race.statsDict.get(self.statsName)        
        self.label.config(text = self.statsName+"\n"+str(self.statsValue))
        self.info.update()
        
    def display(self):
        self.label.grid(row = self.statsRow, column = 1)
        if self.displayButton:
            self.addButton.grid(row = self.statsRow, column = 2)
            self.subButton.grid(row = self.statsRow, column = 0)
            self.prizeButton.grid(row = self.statsRow, column = 3)
    
    def addStatsButtons(self):
        self.addButton = tk.Button(self.parent, text = "+", command = self.addStats, font='arial 14')
        self.subButton = tk.Button(self.parent, text = "-", command = self.subStats, font='arial 14')
        self.prizeButton = tk.Button(self.parent, text = "+2", command = self.addPrizeStats, font='arial 14', bg = "gray")
    
    def addStats(self):
        race = self.raceList.currentRace
        if (race.statsPoints > 0) and (race.statsDict[self.statsName] < 18) and (race != gag):
            race.statsDict[self.statsName] += 1
            race.statsPoints -= 1
        self.updateStats()
    
    def subStats(self):
        race = self.raceList.currentRace
        if (race.statsDict[self.statsName] > 7) and (race != gag) and (not((race.statsDict[self.statsName] < 10) and (self.prize == False))):
            race.statsDict[self.statsName] -= 1
            race.statsPoints += 1
        self.updateStats()
    
    def addPrizeStats(self):
        race = self.raceList.currentRace
        if (race.prizeStats > 0) and (race.statsDict[self.statsName] < 17) and (race != gag):
            if self.prize == True:
                race.statsDict[self.statsName] += 2
                race.prizeStats -= 1
                self.prizeButton.config(bg = "green")
                self.prize = False
            else:            
                race.statsDict[self.statsName] -= 2
                race.prizeStats += 1
                self.prizeButton.config(bg = "gray")
                self.prize = True
        else:
            if self.prize == False:
                race.statsDict[self.statsName] -= 2
                self.prizeButton.config(bg = "gray")                
                race.prizeStats += 1
                self.prize = True            
        self.updateStats()           
            
        
class StatsPoints:
    
    def __init__(self, raceList, parent):
        self.parent = parent
        self.raceList = raceList
        self.currentRace = self.raceList.characterRaceList[self.raceList.comboBox.current()]
        self.pointsValue = self.currentRace.statsPoints
        self.prizeValue = self.currentRace.prizeStats
        self.statsLabel = tk.Label(self.parent, text = "Статов можно распределить\n"+str(self.pointsValue), font='arial 14')
        self.prizeLabel = tk.Label(self.parent, text = "Бонусов на +2 стата осталось\n"+str(self.prizeValue), font='arial 14')
        
    def update(self):
        self.currentRace = self.raceList.characterRaceList[self.raceList.comboBox.current()]
        self.pointsValue = self.currentRace.statsPoints
        self.prizeValue = self.currentRace.prizeStats        
        self.statsLabel.config(text = "Статов можно распределить\n"+str(self.pointsValue))
        self.prizeLabel.config(text = "Бонусов на +2 стата осталось\n"+str(self.prizeValue))
    
    def display(self):
        self.statsLabel.grid(row = 1, column = 0, columnspan = 4)
        self.prizeLabel.grid(row = 2, column = 0, columnspan = 4)
        

class Specials:
    
    def __init__(self, parent, raceList):
        self.parent = parent
        self.raceList = raceList
        self.abilities = {}
        self.currentRace = None
        self.label = tk.Label(self.parent, text = "")
    
    def update(self):    
        self.currentRace = self.raceList.characterRaceList[self.raceList.comboBox.current()]
        self.abilities = self.currentRace.specialAbilities
        self.removeAbilities()
        self.addAbilities()
        
    def addAbilities(self):
        thisAbility = ""
        for ability in self.abilities.keys():
            thisAbility = thisAbility + ability + "\n" + self.abilities.get(ability) + "\n"
        self.label.config(text = thisAbility) 
            
    def removeAbilities(self):
        self.label.config(text = "")
    
    def display(self):
        self.label.pack()
            
        
class MyCharacter:
    def __init__(self):
        pass
    
root = tk.Tk()
root.state('zoomed')
imageFrame = tk.Frame(root, height = 100)
imageFrame.place(x = 0, y = 0)
infoFrame = tk.Frame(root, height = 800)
infoFrame.place(x = 620, y = 0)
textFrame = tk.Frame(root, height = 800)
textFrame.place(x = 1200, y = 0)

gag = "Gag/gag.gif"
gag = MetaCharacterRace(raceName = "Choose Race", pathToManImage = gag, pathToWomanImage = gag)
racePreview = CharacterRacePreview(parent = imageFrame, pathToGagImg = gag.pathToManImage)
racePreview.display()

chooseRaceList = CharacterRaceList(parent = infoFrame, racePreview = racePreview, gag = gag)
chooseRaceList.display()

statsPoints = StatsPoints(parent = infoFrame, raceList = chooseRaceList)
statsPoints.display()

spec = Specials(parent = textFrame, raceList = chooseRaceList)
chooseRaceList.addSpec(spec)
spec.display()

strStat = StatsInfo(parent = infoFrame, statsName = "Сила", raceList = chooseRaceList, info = statsPoints, statsRow = 3)
chooseRaceList.addStats(strStat)
strStat.display()

dexStat = StatsInfo(parent = infoFrame, statsName = "Ловкость", raceList = chooseRaceList, info = statsPoints, statsRow = 4)
chooseRaceList.addStats(dexStat)
dexStat.display()

conStat = StatsInfo(parent = infoFrame, statsName = "Телосложение", raceList = chooseRaceList, info = statsPoints, statsRow = 5)
chooseRaceList.addStats(conStat)
conStat.display()

intStat = StatsInfo(parent = infoFrame, statsName = "Интеллект", raceList = chooseRaceList, info = statsPoints, statsRow = 6)
chooseRaceList.addStats(intStat)
intStat.display()

wizStat = StatsInfo(parent = infoFrame, statsName = "Мудрость", raceList = chooseRaceList, info = statsPoints, statsRow = 7)
chooseRaceList.addStats(wizStat)
wizStat.display()

charStat = StatsInfo(parent = infoFrame, statsName = "Харизма", raceList = chooseRaceList, info = statsPoints, statsRow = 8)
chooseRaceList.addStats(charStat)
charStat.display()

speedStat = StatsInfo(parent = infoFrame, statsName = "Скорость", raceList = chooseRaceList, info = statsPoints, statsRow = 9, displayButton = False)
chooseRaceList.addStats(speedStat)
speedStat.display()

humanMaleImg ="Human/humanMan.gif"
humanFemaleImg ="Human/humanWoman.gif"
humanStats = {"Скорость": 5}
humanSpec = {"how":"much?", "no":"charge"}
human = MetaCharacterRace(raceName = "Human", pathToManImage = humanMaleImg, pathToWomanImage = humanFemaleImg)
human.raceStats(humanStats, prize = 1)
human.addToRaceList(chooseRaceList)
human.addToRacePreview(racePreview)
human.addSpec(humanSpec)

turianMaleImg = "Turian/turianMan.gif"
turianFemaleImg = "Turian/turianWoman.gif"
turianStats = {"Харизма": -2, "Мудрость": 2, "Ловкость": 2}
turian = MetaCharacterRace(raceName = "Turian", pathToManImage = turianMaleImg, pathToWomanImage = turianFemaleImg)
turian.raceStats(turianStats)
turian.addToRaceList(chooseRaceList)
turian.addToRacePreview(racePreview)

asariMaleImg = "Asari/asariMan.gif"
asariFemaleImg = "Asari/asariMan.gif"
asariStats = {"Ловкость": 2, "Мудрость": 2, "Харизма": 2, "Сила": -2, "Телосложение": -2}
asari = MetaCharacterRace(raceName = "Asari", pathToManImage = asariMaleImg, pathToWomanImage = asariFemaleImg)
asari.raceStats(asariStats)
asari.addToRaceList(chooseRaceList)
asari.addToRacePreview(racePreview)

batarianMaleImg = "Batarian/batarianMan.gif"
batarianFemaleImg = "Batarian/batarianWoman.gif"
batarianStats = {"Мудрость": -2}
batarian= MetaCharacterRace(raceName = "Batarian", pathToManImage = batarianMaleImg, pathToWomanImage = batarianFemaleImg)
batarian.raceStats(batarianStats, prize = 2)
batarian.addToRaceList(chooseRaceList)
batarian.addToRacePreview(racePreview)

root.mainloop()

