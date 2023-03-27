import pygame
from pygame import *
import time
import requests
import random
class Game:
    def __init__(self):
        pygame.init()
        screen.fill("BLACK")
        self.updateScreen()
        self.boxes = Boxes()
        self.word_ls = []
        self.generateWord()
        self.boxes.createStartingBoxes()
        self.guesses = Guesses(self.boxes.getBoxList(), self.getWordList())
        pygame.display.set_caption("WORDLE")
        self.showWordleText()
        self.guesses.showUsedLetters()
        self.playGame()

    def getWordList(self):
        return self.word_ls
    
    def getWord(self):
        return self.word

    def showWordleText(self):
        self.wordleFontColor = (255,255,255)
        self.wordleFont = pygame.font.Font("freesansbold.ttf", 115)
        self.wordleText = self.wordleFont.render("WORDLE", True, self.wordleFontColor)
        screen.blit(self.wordleText, (900, 300))
        self.funFont = pygame.font.Font("C:\Windows\Fonts\comici.ttf", 30)
        self.funText = self.funFont.render("but worse", True, self.wordleFontColor)
        screen.blit(self.funText, (1070, 410))
        self.textshown = False
        self.updateScreen()

    def updateScreen(self):
        pygame.display.flip()
        pygame.display.update()

    def playGame(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key != 13 and event.key != 8 and event.key != K_SLASH: #if not enter (13) or backspace (8)
                        if 97 <= event.key and event.key <= 122: #if letter
                            self.guesses.showLetter(event.key)
                    elif event.key == 13:
                        if self.guesses.getX() == 5:
                            if self.guesses.validGuess(self.getAllWords()):
                                self.guesses.checkGuess()
                                if self.guesses.checkEnd():
                                    self.endGame()
                                else:
                                    self.guesses.newLine()

                    elif event.key == 8:
                        self.guesses.recreateBox((self.guesses.getX()-1), self.guesses.getY())

                    elif event.key == K_SLASH:
                        if self.textshown:
                            self.hideText()
                            self.textshown = False
                        else:
                            self.showText()
                            self.textshown = True

    def showText(self):
        self.weirdFont = pygame.font.Font("freesansbold.ttf", 30)
        self.weirdText = self.weirdFont.render(self.word, True, (32,32,32))
        screen.blit(self.weirdText, (1350, 870))
        self.updateScreen()

    def hideText(self):
        self.hintrect = pygame.Rect(1350, 870, 150, 80)
        pygame.draw.rect(screen, "black", self.hintrect)
        self.updateScreen()

    def generateWord(self):
        self.word_url = "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt"
        self.allwords = requests.get(self.word_url, allow_redirects=True)
        self.word = random.choice(self.allwords.text.split("\n"))
        self.word = self.word.upper()
        for i in range(len(self.word)):
            self.word_ls.append(self.word[i])
    
    def getAllWords(self):
        return self.allwords.text
    
    def endGame(self):
        if self.guesses.checkLoss():
            self.showLosingText()

    def showLosingText(self):
        self.lostTextFontColor = (255,255,255)
        self.lostTextFont = pygame.font.Font("freesansbold.ttf", 40)
        self.lostText = self.lostTextFont.render(("The word was " + self.getWord()), True, self.lostTextFontColor)
        screen.blit(self.lostText, (945, 700))
        self.updateScreen()

class Boxes():
    def __init__(self):
        self.boxlist = []
        self.boxlist_s = []

    def createStartingBoxes(self):
        for i in range(5):
            for j in range(5):
                self.rect = pygame.Rect((55+150*i), (90+150*j), 100, 100)
                self.drawBox(self.rect, "gray")
                self.updateScreen()
                self.boxlist_s.append(self.rect)
            self.boxlist.append(self.boxlist_s)
            self.boxlist_s = []
    
    def drawBox(self, rectd, color):
        self.color = color
        self.rectd = rectd
        pygame.draw.rect(screen, self.color, self.rectd)

    def updateScreen(self):
        pygame.display.flip()

    def setBoxColor(self, x, y, color):
        self.newx = x
        self.newy = y
        self.newcolor = color
        pygame.draw.rect(screen, self.newcolor, self.boxlist[self.newx][self.newy])
        self.updateScreen()

    def getBoxList(self):
        return self.boxlist


class Guesses(Boxes):
    def __init__(self, boxlist, word_ls):
        Boxes.__init__(self)
        self.guess_ls = []
        self.guess_str = ""
        self.pressedkey = ""
        self.chr_loc_x = 0 #keeping the text indexed
        self.chr_loc_y = 0
        self.letterFontColor = (255,255,255)
        self.letterFont = pygame.font.Font(("freesansbold.ttf"), 90)
        self.usedLetterFont = pygame.font.Font(("freesansbold.ttf"), 40)
        self.boxlist = boxlist
        self.wordls = word_ls
        self.no_correct = 0
        self.ideal_word = ['', '', '', '', '']
        self.letterlist = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"], ["A", "S", "D", "F", "G", "H", "J", "K", "L"], ["Z", "X", "C", "V", "B", "N", "M"]]
        self.letterlistcoords = [["", "", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", ""]]

    def showUsedLetters(self):
        for i in range(len(self.letterlist)):
            for j in range(len(self.letterlist[i])):
                self.usedLetterText = self.usedLetterFont.render(self.letterlist[i][j], True, self.letterFontColor)
                screen.blit(self.usedLetterText, ((925+50*j),((500+50*i))))
                self.letterlistcoords[i][j] = [(34+20*j), (30+25*i)]
                self.updateScreen()

    def updateUsedLetters(self, color, letter):
        self.usedLetterColor = color
        self.usedLetter = letter
        self.usedLetterText = self.usedLetterFont.render(self.usedLetter, True, self.usedLetterColor)
        self.usedLetterCoords = self.findUsedLetterLoc(self.usedLetter)
        screen.blit(self.usedLetterText, ((925+50*self.usedLetterCoords[1]),((500+50*self.usedLetterCoords[0]))))


    def findUsedLetterLoc(self, usedletter):
        self.usedlettertofind = usedletter
        for i in range(len(self.letterlist)):
            for j in range(len(self.letterlist[i])):
                if self.letterlist[i][j] == self.usedlettertofind:
                    return [i, j]
    
    def showLetter(self, key):
        self.key = key
        if self.chr_loc_x <= 4 and self.chr_loc_y <= 4:
            if self.key > 96:
                self.key = (key - 32)
            self.letterText = self.letterFont.render(chr(self.key), True, self.letterFontColor)
            screen.blit(self.letterText, ((69+150*self.chr_loc_x),((100+150*self.chr_loc_y))))
            self.updateScreen()
            self.chr_loc_x += 1
            self.guess_ls.append(chr(self.key))
            self.guess_str += chr(self.key)

    def overwriteBox(self, letter, x):
        self.overwrite_letter = letter
        self.overwrite_x = x
        self.overwriteLetterText = self.letterFont.render(self.overwrite_letter, True, self.letterFontColor)
        screen.blit(self.overwriteLetterText, ((69+150*self.overwrite_x),((100+150*self.chr_loc_y))))
        self.updateScreen()

    def validGuess(self, allwords):
        self.allwords = allwords
        self.guess_str = self.guess_str.lower()
        if self.guess_str in self.allwords:
            return True
        else:
            return False

    def newLine(self):
        if self.chr_loc_y < 4:
            self.chr_loc_y += 1
        self.chr_loc_x = 0
        self.guess_ls = []
        self.guess_str = ""
        self.checkEnd()

    def checkGuess(self):
        self.wordlsmod = []
        for i in range(len(self.wordls)):
            self.wordlsmod.append(self.wordls[i])
            self.getGreenIndices()
        for i in range(len(self.greenindices)):
            self.wordlsmod[self.greenindices[i]] = " "
        for i in range(5):
            if self.guess_ls[i] in self.wordlsmod: #half correct
                self.wordlsmod[self.wordlsmod.index(self.guess_ls[i])] = " " #blank the space with the letter with the index value of the of the guessed letter in the guess list
                self.drawBox((self.boxlist[i][self.chr_loc_y]), "gold")
                self.overwriteBox(self.guess_ls[i], i)
                self.updateUsedLetters("gold", self.guess_ls[i])
                self.updateScreen()
            elif self.guess_ls[i] == self.wordls[i] : #fully correct
                self.wordlsmod[i] = " "
                self.drawBox((self.boxlist[i][self.chr_loc_y]), "chartreuse3")
                self.overwriteBox(self.guess_ls[i], i)
                self.ideal_word[i] = self.guess_ls[i] #basically just add every correct letter to its space a list pre-filled with blank spaces
                self.updateUsedLetters("chartreuse3", self.guess_ls[i])
                
            else:
                self.drawBox((self.boxlist[i][self.chr_loc_y]), "dimgray")
                self.overwriteBox(self.guess_ls[i], i)
                if not (self.guess_ls[i] in self.wordls):
                    self.updateUsedLetters("dimgray", self.guess_ls[i])
                    self.updateScreen()

            time.sleep(0.02+0.005*i)
            self.no_correct_counter = 0
            for j in range(5):
                    if self.ideal_word[j] != '':
                        self.no_correct_counter += 1
            self.no_correct = self.no_correct_counter #how many letters are in the correct space
        self.wordlsmod = self.wordls

    def getGreenIndices(self): #AXAOI
      
        '''Create an index with all the green letter position, 
        and then in checkGuess make sure that when making a letter
        yellow the index isn't in one of the green letters'''
        
        self.greenindices = []
        for i in range(5):
            if self.guess_ls[i] == self.wordls[i]:
                self.greenindices.append(i)

        
        
    def getX(self):
        return self.chr_loc_x

    def getY(self):
        return self.chr_loc_y
    
    def recreateBox(self, x, y):
        if x >= 0:
            self.x = 55+150*x
            self.y = 90+150*y
            self.rect = pygame.Rect(self.x, self.y, 100, 100)
            self.drawBox(self.rect, "gray")
            self.updateScreen()
            if self.chr_loc_x > 0:
                self.chr_loc_x -= 1
            if len(self.guess_ls) > 0:
                self.guess_ls.remove(self.guess_ls[-1])
                self.guess_str = self.guess_str[:-1]

    
    def checkEnd(self):
        if self.no_correct == 5:
            return True
        elif self.chr_loc_y >= 4:
            return True
        else:
            return False
        
    def checkLoss(self):
        if self.no_correct == 5:
            return False
        else:
            return True

screen = pygame.display.set_mode([1500, 940])        
game = Game()
