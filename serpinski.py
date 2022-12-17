'''
    File: serpinski.py
    Author: Drew Scott
    Description: Visualizes the creation of the Serpinski Triangle using points
    Usage: python3 serpinski.py
'''

from random import randint, choice
from turtle import Turtle, Screen

DOT_RADIUS = 3
N_POINTS = 10000

def main():
    # set up the screen
    screen = Screen()
    width, height = screen.window_width(), screen.window_height()
    screen.tracer(0, 0)

    # create the drawer
    turtle = Turtle(visible=False)
    turtle.speed(0)
    turtle.penup()

    # draw the corners of the triange
    corners = [(0,(height//2)-50), (-(width//2)+50,-(height//2)+50), ((width//2)-50,-(height//2)+50)]
    turtle.setposition(corners[0])
    turtle.dot(DOT_RADIUS, 'black')
    turtle.setposition(corners[1])
    turtle.dot(DOT_RADIUS, 'black')
    turtle.setposition(corners[2])
    turtle.dot(DOT_RADIUS, 'black')
    screen.update()

    # go to the center of the triangle
    prev_loc = (-50, 50)

    # place the dots
    for _ in range(N_POINTS):
        corner = choice(corners)
        new_loc = ((prev_loc[0] + corner[0])//2, (prev_loc[1] + corner[1])//2)
        turtle.setposition(new_loc)
        turtle.dot(DOT_RADIUS, 'black')
        screen.update()
        prev_loc = new_loc

    screen.exitonclick()

if __name__ == '__main__':
    main()
