import pygame, simpleGE, random

""" catch.py 
    slide and catch Demo
    Andy
"""

class Car(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("car.png")
        self.setSize(30, 25)
        self.minSpeed = 4
        self.maxSpeed = 10
        self.reset()
        
    def reset(self):
        #move to right of screen
        self.x = 10
        
        #y is random 0 - screen width
        self.y = random.randint(50, self.screenHeight)
        
        #dy is random minSpeed to maxSpeed
        self.dx = random.randint(self.minSpeed, self.maxSpeed)
        
        
    def checkBounds(self):
        if self.right > self.screenWidth:
            self.reset()


class Fish(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("cuttlefish.png")
        self.setSize(40, 40)
        self.position = (320, 50)
        self.moveSpeed = 5
        
    def reset(self):
        self.y = 50
        
    def process(self):
        if self.isKeyPressed(pygame.K_UP):
            self.y -= self.moveSpeed
        if self.isKeyPressed(pygame.K_DOWN):
            self.y += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 25"
        self.center = (500, 30)
    
 
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("Road.png")
        self.music = simpleGE.Sound("roadrage.wav")
        self.music.play()
        self.sndCar = simpleGE.Sound("horn.wav")
        self.numCars = 8
        self.score = 0
        self.lblScore = LblScore()

        self.timer = simpleGE.Timer()
        self.timer.totalTime = 25
        self.lblTime = LblTime()
        
        self.fish = Fish(self)
        
        self.car = []
        for i in range(self.numCars):
            self.car.append(Car(self))
            
        self.sprites = [self.car, 
                        self.fish,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        for cars in self.car:        
            if cars.collidesWith(self.fish):
                self.fish.reset()
                self.sndCar.play()
                self.score -= 150
                
            else:
                self.score += 1
        self.lblScore.text = f"Score: {self.score}"
                
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        
        if self.timer.getTimeLeft() < 0:
            print(f"Score: {self.score}")
            self.stop()

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()

        self.prevScore = prevScore

        self.setImage("Street.png")
        self.response = "Quit"
        
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are Cuddle the Cuttlefish", 
        "Move with up and down arrow keys.",
        "Dodge the cars as long as you can",
        "in the time provided",
        "",
        "Good luck!"]
        
        self.directions.center = (320, 200)
        self.directions.size = (500, 250)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)        
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.clearBack = True
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last score: {self.prevScore}"

        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
    
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
        
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()


def main():
    
    keepGoing = True
    lastScore = 0

    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        
        if instructions.response == "Play":    
            game = Game()
            game.start()
            lastScore = game.score
            
        else:
            keepGoing = False
            
if __name__ == "__main__":
    main()