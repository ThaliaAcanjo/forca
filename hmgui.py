from tkinter import *
from tkinter import font
import string, random
import hangman

keys = [ ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
         ['A', 'S', 'D','F', 'G', 'H','J','K','L'],
         ['Z','X','C','V','B','N','M']]


class hmGUIGuess():    
    def __init__(self, ch):        
	    self.theValue = (ch.upper())
    
    def value(self):
        return self.theValue

class hmGUI(Frame, hangman.Hangman):	
    def __init__(self, parent=0):
	    # call the parent constructors
        hangman.Hangman.__init__(self)
        Frame.__init__(self, Tk())
        self.imgpath = '' # put gif files elsewhere if we want
        self.firstImg=self.imgpath+'hm6.gif'
        self.letters = {}
        self.playing = True
        self.master.title('Hangman') # set the app title bar
        self.master.geometry("600x550")  # Tamanho da janela
        self.master.config(bg="#f2f2f2")
        
        self.canvas = None
        self.part_ids = {"head": None, "body": None, "left_arm": None, "right_arm": None, "left_leg": None, "right_leg": None}

        self.status = ''
        self.bind("<KeyPress>", self.letterPress)
        self.focus_set()         
        self.displayStart()
        self.draw(6)
            
    def play(self):
        self.mainloop()

    def quit(self):
        import sys
        sys.exit()

    def reset(self):
        for chr in self.letters:
            self.letters[chr].config(state=ACTIVE, bg="#f2f2f2", fg="black", relief=FLAT)
            self.letters[chr].unbind("<Enter>")  # Remove o efeito de hover
        
        self.lives = 6
        self.guesses = []
        self.theTarget = self.getTarget()
        #self.theImg.configure(file=self.firstImg)    
        self.status.configure(text='')
        txt = self.getResult()        
        self.wordsecret.configure(text=txt)
                
        for part in self.part_ids.values():
            if part:
                self.canvas.delete(part)  # Remove todas as partes do boneco
            self.part_ids = {key: None for key in self.part_ids} 
        self.canvas.delete("all")
        self.playing = True
        self.draw(6)
    
    def disableLetters(self):
        self.playing = False
        for chr in self.letters:
            state = self.letters[chr].cget("state")
            if (state == 'normal') or (state == 'active'):
                self.letters[chr].config(state=DISABLED, background='#AEBEBE', fg='red')
                self.letters[chr].unbind("<Enter>")  # Remove o efeito de hover

    def display(self, chr):        
        lossmsg = 'You lost! The word was  %s'
        successmsg = 'Well done, you guessed it!'
	    
	    # mark letter as used        
        matching_guesses = [guess for guess in self.guesses if guess.theValue == chr]
        if (chr in self.letters) and (not matching_guesses) and (self.playing):
            self.letters[chr].config(state=DISABLED, background='#7BD39C', foreground='black')
                
            # create a guess
            self.guesses.append(hmGUIGuess(chr))
	    
            # decrease lives if wrong
            self.lives = self.theTarget.eval(self.guesses[-1])    		

            txt = self.getResult()
            self.wordsecret.configure(text=txt) 
            
            status = ''
            if self.lives > 0: 
                if '_' not in txt:
                    status = successmsg
                    self.disableLetters()                                
            else:
                status = lossmsg % self.theTarget.getGoal()
            
            if chr not in self.theTarget.getGoal():
                self.letters[chr].config(state=DISABLED, background='#E68888', fg='red')            

            if self.lives >= 0: 
                if chr not in self.theTarget.getGoal():
                    self.draw(self.lives)
                if self.lives == 0:
                    self.swing_animation() 
                    self.disableLetters()                
                #thefile = self.imgpath + 'hm' + str(self.lives) + '.gif'
                #self.theImg.configure(file=thefile)    
                           
            self.status.configure(text=status) 
                                                       
    def displayStart(self): 
        frameHangman = Frame(self, border=1, relief=FLAT)
        self.canvas = Canvas(frameHangman, width=200, height=220 )
        frameHangman.pack()
        self.canvas.pack(fill=BOTH, expand=True)
                        
        frameWord = Frame(self, border=1, relief=FLAT)  
        txt = self.getResult()        
        self.wordsecret = Label(frameWord, 
                                foreground='black',
                                width=35,
                                text=txt, 
                                font= font.Font(root=None, font=None, name=None, exists=False, size=20))
        self.wordsecret.pack()
        frameWord.pack(pady=25)        
        
        frameStatus = Frame(self, border=1, relief=FLAT, width=35, padx=35, bg="#f2f2f2")
        self.status = Label(frameStatus, 
                            anchor=CENTER, 
                            foreground='black',
                            width=35,
                            text=self.status, 
                            font=font.Font(family="Arial", size=12), bg="#f2f2f2", fg="red")
        frameStatus.pack()
        self.status.pack()                

        frameLetters = Frame(self, border=1, relief=GROOVE)
        for row in keys:
            frame = Frame(frameLetters)
            for ch in row:
                action = lambda x=ch, s=self: s.display(x)
                self.letters[ch] = Button(frame, 
                                          text=ch, 
						                  width=2, 
                                          bg="#f2f2f2",
                                          relief=FLAT,
						                  command=action)                 
                self.letters[ch].pack(side=LEFT, padx=10)            
            frame.pack(pady=1)
        frameLetters.pack(pady=20)        
        
        frameControl = Frame(self)
        r = Button(frameControl, text='Reset', padx=10, command=self.reset)
        r.pack(side=LEFT, padx=10, pady=5, anchor=W)
		
        q = Button(frameControl, text='Quit', padx=10, command=self.quit)
        q.pack(side=RIGHT, padx=20, pady=5, anchor=W)
        frameControl.pack()
        
        self.pack()
    
    def letterPress(self, event):
        self.theValue = event.char.upper()
        
        if len(self.theValue) > 1:
            self.theValue = self.theValue[0]
        if self.theValue in string.ascii_letters:    
            self.display(self.theValue)

    def draw(self, lives):        
        ms = 300
        if lives == 6:
            self.animate_line("base", 35, 185, 135, 185)  # Base
            self.master.after(100, lambda: self.animate_line("poste", 85, 185, 85, 35))  # Poste
            self.master.after(600, lambda: self.animate_line("barra", 85, 35, 135, 35))  # Braço superior
            self.master.after(1000, lambda: self.animate_line("corda", 135, 35, 135, 60))  # Corda
        elif lives == 5:            
            if "head" in self.part_ids:
                if self.part_ids["head"]:
                    self.canvas.delete(self.part_ids["head"])
                               
            id = self.canvas.create_oval(122, 60, 147, 85, outline="black", width=3)
            self.part_ids["head"] = id  # Armazena o ID na estrutura

            # Agendar uma ação usando `after`
            self.master.after(ms, lambda: self.canvas.itemconfig(id))
        elif lives == 4:
            self.master.after(ms, lambda: self.animate_line("body", 135, 85, 135, 135))  # Corpo
        elif lives == 3:    
            self.master.after(ms, lambda: self.animate_line("left_leg", 135, 100, 120, 120))  # Braço esquerdo
        elif lives == 2:    
            self.master.after(ms, lambda: self.animate_line("right_leg", 135, 100, 150, 120))  # Braço direito
        elif lives == 1:    
            self.master.after(ms, lambda: self.animate_line("left_arm", 135, 135, 120, 160))  # Perna esquerda
        else:    
            self.animate_line("right_arm", 135, 135, 150, 160, delay=0)
    
    def animate_line(self, partID, x1, y1, x2, y2, color="black", steps=30, delay=10):               
        if partID in self.part_ids:
            if self.part_ids[partID]:
                self.canvas.delete(self.part_ids[partID])  # Remove cabeça antiga, se existir
                  
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps
        line_id = self.canvas.create_line(x1, y1, x1, y1, fill=color, width=3)
        self.part_ids[partID] = line_id        
        
        def update_line(step):
            if step <= steps:
                self.canvas.coords(line_id, x1, y1, x1 + dx * step, y1 + dy * step)
                self.master.after(delay, update_line, step + 1)
        
        update_line(0) 

    def swing_animation(self):    
        self.after(100)

        yHead = -1
        y = -2
        x = 2
                
        self.canvas.move(self.part_ids["right_leg"], x, y)
        self.canvas.move(self.part_ids["left_leg"], x, y)        
        self.canvas.move(self.part_ids["left_arm"], x, y)
        self.canvas.move(self.part_ids["right_arm"], x, y)
        self.canvas.update()
        
        moves = 1
        for _ in range(5):  # Número de ciclos de balanço
            # Move as pernas e braços para a direita
            self.canvas.move(self.part_ids["left_leg"], -moves, 0)
            self.canvas.move(self.part_ids["right_leg"], moves, 0)
            self.canvas.move(self.part_ids["left_arm"], -moves, 0)
            self.canvas.move(self.part_ids["right_arm"], moves, 0)
            self.canvas.update()
            self.after(100)  # Aguarda 100ms para a próxima movimentação

            # Move as pernas e braços para a esquerda
            self.canvas.move(self.part_ids["left_leg"], moves, 0)
            self.canvas.move(self.part_ids["right_leg"], -moves, 0)
            self.canvas.move(self.part_ids["left_arm"], moves, 0)
            self.canvas.move(self.part_ids["right_arm"], -moves, 0)
            self.canvas.update()
            self.after(100)

        self.canvas.move(self.part_ids["head"], 7, yHead)
        self.canvas.move(self.part_ids["body"], 0, yHead-2)

        self.canvas.delete("right_leg")
        self.canvas.delete("left_leg")
        self.canvas.delete("left_arm")
        self.canvas.delete("right_arm")

        self.animate_line("left_leg", 135, 100, 130, 120, steps=1, delay=0)
        self.animate_line("right_leg", 135, 100, 140, 120, steps=1, delay=0)
        self.animate_line("left_arm", 135, 132, 130, 160, steps=1, delay=0)
        self.animate_line("right_arm", 135, 132, 140, 160, steps=1, delay=0)        


if __name__ == "__main__":
    
    hmGUI().play()        
