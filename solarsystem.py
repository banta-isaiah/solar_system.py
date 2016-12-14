import math
import turtle
import random
from pair import *
from vector import *


class System:
    """A two-dimensional world class."""
    
    def __init__(self, width, height):
        """Construct a new flat world with the given dimensions."""
           
        self._width = width
        self._height = height
        self._agents = { }
        
    def getWidth(self):
        """Return the width of self."""
        
        return self._width
        
    def getHeight(self):
        """Return the height of self."""
        
        return self._height
    
    def __getitem__(self, position):
        """Return the agent at the given position."""
       
        if position in self._agents:
            return self._agents[position]
        return None
    
    def __setitem__(self, position, agent):
        """Set the given position to contain agent."""
       
        if (position not in self._agents) and \
           (position[0] >= 0) and (position[0] < self._width) and \
           (position[1] >= 0) and (position[1] < self._height):
            self._agents[position] = agent
            
    def __delitem__(self, position):
        """Delete the agent at the given position."""
        
        if position in self._agents:
            del self._agents[position]
        
    def neighbors(self, position, distance):
        """Return a list of agents within distance of
           position (a tuple)."""
        
        neighbors = []
        for otherPosition in self._agents:
            if (position != otherPosition) and \
               (_distance(position, otherPosition) <= distance):
                neighbors.append(self._agents[otherPosition])
        return neighbors

    def stepAll(self):
        """All agents advance one step in the simulation."""
        
        agents = list(self._agents.values())
        for agent in agents:
            agent.step()

class Sun:
    """A sun object"""
    def __init__(self, mySystem):
        
        self._system = mySystem
        self._turtle = turtle.Turtle()
        self._turtle.hideturtle()
        self._turtle.speed(0)
        self._turtle.penup()
        self._turtle.goto(0,-50)
        self._turtle.begin_fill()
        self._turtle.pendown()
        self._turtle.fillcolor("yellow")
        self._turtle.circle(50)
        self._turtle.end_fill()
        
            
class Planet:
    """A planet object"""
    
    def __init__(self, mySystem, distance, size, color, velocity):
        
        self._system = mySystem
        mySystem._agents[self] = self
        self._velocity = velocity
        self._color = color
        self._distance = distance
        self._size = size
        self._position = [distance, 0]
        self._angle = 90
        
        #MAKE PLANET
        self._turtle = turtle.Turtle(shape = 'circle')
        self._turtle.hideturtle()
        
        #INITIALIZE PLANET
        self._turtle.fillcolor(color)
        self._turtle.penup()
        self._turtle.goto(self._position)
        self._turtle.turtlesize(size,size,size)
        self._turtle.showturtle()
        
    def getmySystem(self):
        return self._mySystem
    
    def getdistance(self):
        return self._distance
    
    def getposition(self):
        return self._position
    
    def getvelocity(self):
        return self._velocity
    
    def step(self):
        xvar = self._position[0]
        yvar = self._position[1]
        
        newx = int(self._distance*math.cos(math.radians(90-self._angle)))
        newy = int(self._distance*math.sin(math.radians(90-self._angle)))
        
        self._turtle.goto(newx, newy)
                   
        self._angle = self._angle - self._velocity
        
        """
        self._turtle.hideturtle()
        self._turtle.goto(0,0)
        self._turtle.right(self._velocity)
        self._turtle.forward(self._distance)
        self._turtle.showturtle()"""

class Boid:
    """A boid in a agent-based flocking simulation."""
    
    def __init__(self, myWorld):
        """Construct a boid at a random position in the given world."""

        self._system = myWorld
        (x, y) = (random.randrange(self._system.getWidth()), 
                  random.randrange(self._system.getHeight()))
        while self._system[x, y] != None:
            (x, y) = (random.randrange(self._system.getWidth()), 
                      random.randrange(self._system.getHeight()))
        self._position = Pair(x, y)
        self._system[x, y] = self
        self._velocity = Vector((random.uniform(-1, 1), 
                                 random.uniform(-1, 1))).unit()
        self._turtle = turtle.Turtle()
        self._turtle.speed(0)
        self._turtle.up()
        self._turtle.setheading(self._velocity.angle())

    def move(self):
        """Move self to a new position in its world."""
    
        self._turtle.setheading(self._velocity.angle())
        
        width = self._system.getWidth()
        height = self._system.getHeight()
        
        newX = self._position[0] + self._velocity[0]
        newX = min(max(0, newX), width - 1)
        newY = self._position[1] + self._velocity[1]
        newY = min(max(0, newY), height - 1)
        
        if self._world[newX, newY] == None:
            self._world[newX, newY] = self
            del self._system[self._position.get()]
            self._position = Pair(newX, newY)
            self._turtle.goto(newX, newY)
            
        if (self._velocity[0] < 0 and newX < 5) or \
           (self._velocity[0] > 0 and newX > width - 5) or \
           (self._velocity[1] < 0 and newY < 5) or \
           (self._velocity[1] > 0 and newY > height - 5):
            self._velocity.turn(30)
    
def main():

    #MAKE THE WINDOW
    worldTurtle = turtle.Turtle()
    screen = worldTurtle.getscreen()
    screen.setworldcoordinates(-400, -400, 400, 400)
    worldTurtle.hideturtle()

    screen.bgpic("Space-1.gif")
    space = System(800, 800)
    
    #MAKE ALL THE PLANETS
    sun = Sun(space)
    mercury = Planet(space, 120, .2, "gray", 1.607)
    venus = Planet(space, 135, .4, "red", 1.174)
    earth = Planet(space, 150, .45, "green", 1)
    mars = Planet(space, 170, .3, "orange", .802)
    jupiter = Planet(space, 235, 1.2, "#DEB887", .434)
    saturn = Planet(space, 300, 1, "#D2B48C", .323)
    uranus = Planet(space, 380, .4, "#25889d", .228)

    while True:
        space.stepAll()
            
    screen.update()
    screen.exitonclick()
    
main()