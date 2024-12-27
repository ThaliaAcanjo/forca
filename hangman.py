import game, random, string
from tkinter import *

class Hangman(game.Game):
    wordfile = 'hangman.words'
    def __init__(self):
        game.Game.__init__(self)
        self.GuessType = hmGuess
        self.outcome = 6

    def displayStart(self):
        self.display(6)

    def getTarget(self):
        return hmTarget()
    
    def getResult(self):
        theWord = ''
        guessed = []

        if self.guesses:
            for g in self.guesses:
                guessed.append(g.theValue)

        goal = self.theTarget.getGoal()
        for c in goal:
            if (c in guessed):
                theWord = theWord + ' ' + c
            else:
                theWord = theWord + ' _'
        return theWord                                 

    def display(self, outcome):        
        theWord = self.getResult()
    
        # sort out singular/plural messages
        if outcome == 1: 
            lives = 'life'
        else: 
            lives = 'lives'
        	    
        if '_' in theWord and  outcome == 0:
           print("Sorry you lose, the word was ", self.theTarget.getGoal())
        elif '_' not in theWord:
           print("Well done, you got it!")
           import sys;sys.exit()
        else:
           print("Word to guess: %s\t You have %d %s left" % (theWord, outcome, lives))	    
       
class hmGuess(game.Guess):
    def __init__(self):
        #self.theValue = ''
        
        self.theValue = input("Type a letter:  ")
	
        if len(self.theValue) > 1: 
            self.theValue = self.theValue[0]
        if self.theValue not in string.ascii_letters:
            self.theValue = input("It must be a letter! ")    
        
class hmTarget(game.Target):
    def __init__(self):
        self.lives = 6
        try:
            self.wrdFile = open(Hangman.wordfile, "r")
            self.wordList =  self.wrdFile.readlines()
        except IOError:	
            self.wordList = ['now\n',
	                         'for\n',
			                 'something\n',
			                 'completely\n',
			                 'different\n']
            
        # while self.goal not in listWords:            
        index = int(random.random() * (len(self.wordList)-1))
        self.goal = self.wordList[index][:-1].upper() # lose \n from end
        

    def eval(self, aGuess):
        if aGuess.value() not in self.goal:
            self.lives  = self.lives - 1
        return  self.lives        
    

if __name__ == "__main__":
    Hangman().play()