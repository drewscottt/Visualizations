'''
    File: convex_hull.py
    Author: Drew Scott
    Description: Displays various methods of computing the convex hull of a set of points
    Usage: python3 convex_hull.py <method>
        * method can be: graham_scan, gift_wrap, divide_conquer
'''

from random import randint, choice
from turtle import Turtle, Screen
from time import sleep
import sys

from util import get_side, prev_ccw, next_ccw, draw_connect_points, DOT_RADIUS, BORDER_PADDING

N_POINTS = 100
TIME_STEP_DELAY = 0.1
BOTTOM_TEXT_HEIGHT = 80
FONT_SIZE = 15

def main(args):
    # set up the screen
    screen = Screen()
    width, height = screen.window_width(), screen.window_height()
    screen.tracer(0, 0)

    # generate and draw the points
    points = []
    points_turtle = Turtle(visible=False)
    points_turtle.speed(0)
    for i in range(N_POINTS):
        new_loc = (randint((-width//2) + BORDER_PADDING, (width//2) - BORDER_PADDING), randint((-height//2) + BORDER_PADDING + BOTTOM_TEXT_HEIGHT, (height//2) - BORDER_PADDING))
        points.append(new_loc)
        points_turtle.penup()
        points_turtle.setposition(points[i])
        points_turtle.pendown()
        points_turtle.dot(DOT_RADIUS, 'black')
    screen.update()

    # compute and draw the convex hull
    ch_turtle = Turtle(visible=False)
    ch_turtle.speed(0)
    text_turtle = Turtle(visible=False)
    text_turtle.speed(0)
    text_turtle.penup()
    if args[1] == 'graham_scan':
        text_turtle.setposition((((-width//2) + BORDER_PADDING), ((-height//2) + BOTTOM_TEXT_HEIGHT - 4*FONT_SIZE)))
        text_turtle.write("Graham Scan: O(n)\nPre-condition: points are sorted by x-value; O(nlogn) preprocessing\nExplanation: Computes the upper and lower hulls then splices them together. Starts with the leftmost\n\tpoint; successive points on the top/bottom must be to the right/left of the previous segment.",
            font=("Arial", FONT_SIZE, "normal"))
        convex_hull = graham_scan(points, screen, True)
        draw_connect_points(convex_hull, screen, ch_turtle)
    elif args[1] == 'gift_wrap':
        text_turtle.setposition((((-width//2) + BORDER_PADDING), ((-height//2) + BOTTOM_TEXT_HEIGHT - 3*FONT_SIZE)))
        text_turtle.write("Gift Wrapping: O(n*k), where k is the number of vertices on the hull\nExplanation: Starts with the lowest point; adds points for which all other points are to the left of the\n\tsegment created by it and the previous added point.",
            font=("Arial", FONT_SIZE, "normal"))
        convex_hull = gift_wrap(points, screen, True)
        draw_connect_points(convex_hull, screen, ch_turtle)
    elif args[1] == 'divide_conquer':
        text_turtle.setposition((((-width//2) + BORDER_PADDING), ((-height//2) + BOTTOM_TEXT_HEIGHT - 4*FONT_SIZE)))
        text_turtle.write("Divide and Conquer: O(nlogn)\nExplanation: Recursively computes the convex hull of the left and right points, then merges them\n\ttogether. The merging process finds the upper and lower common tangents between the\n\tleft and right hulls.",
            font=("Arial", FONT_SIZE, "normal"))
        convex_hull = divide_conquer(points, screen, True)
        draw_connect_points(convex_hull, screen, ch_turtle)

    screen.exitonclick()

def divide_conquer(points, screen, show_states):
    '''
        Returns the list of points in CCW order of the convex hull of the set of points
        The first and last points in the list are the same
        Draws the steps taken in the processing
        Uses the Divide and Conquer approach: O(nlogn), where n is number of points
        Utilized divide_conquer_util
    '''

    points = sorted(points)
    convex_hull, _ = divide_conquer_util(points, 0, len(points), screen, show_states)
    convex_hull.append(convex_hull[0])
    return convex_hull

def divide_conquer_util(points, l, r, screen, show_states):
    '''
        Computes the convex hull of the points between the lth (inclusive) and rth (exlusive) index in points using a recursive approach
        Returns the points of the computed in CCW order, and the turtle used to draw the merged hull
    '''

    if r - l <= 3:
        # base case: we have 2 or 3 points, so return them in CCW order
        if r - l == 2:
            convex_hull = points[l : r]
        else:
            if get_side(points[l], points[l+1], points[l+2]) > 0:
                # if third point is to the left then its already CCW
                convex_hull = points[l : r]
            else:
                convex_hull = [points[l], points[l+2], points[l+1]]

        merge_turtle = Turtle(visible=False)
        merge_turtle.speed(0)
        if show_states:
            draw_connect_points(convex_hull + [convex_hull[0]], screen, merge_turtle)
        return convex_hull, merge_turtle

    # compute the convex hulls of the left and right halves of the point set recursively
    left_half, left_turtle = divide_conquer_util(points, l, l + (r-l)//2, screen, show_states)
    right_half, right_turtle = divide_conquer_util(points, l + (r-l)//2, r, screen, show_states)

    # merge the left and right halves by finding the common tangents 

    # start by finding the upper tangent
    upper_endpoints = [max(left_half), min(right_half)]
    upper_indices = [left_half.index(max(left_half)), right_half.index(min(right_half))]
    
    # draw each candidate tangent in red
    upper_turtle = Turtle(visible=False)
    if show_states:
        upper_turtle.speed(0)
        upper_turtle.pencolor('red')
        upper_turtle.penup()
        upper_turtle.setposition(upper_endpoints[0])
        upper_turtle.pendown()
        upper_turtle.goto(upper_endpoints[1]) 
        screen.update()

    while (
            get_side(upper_endpoints[0], upper_endpoints[1], prev_ccw(right_half, upper_indices[1])) > 0 or 
            get_side(upper_endpoints[1], upper_endpoints[0], next_ccw(left_half, upper_indices[0])) < 0
    ):
        if get_side(upper_endpoints[0], upper_endpoints[1], prev_ccw(right_half, upper_indices[1])) > 0:
            upper_endpoints[1] = prev_ccw(right_half, upper_indices[1]) 
            upper_indices[1] = right_half.index(upper_endpoints[1])
        else:
            upper_endpoints[0] = next_ccw(left_half, upper_indices[0])
            upper_indices[0] = left_half.index(upper_endpoints[0])
    
        if show_states:
            sleep(TIME_STEP_DELAY)
            upper_turtle.clear()
            upper_turtle.penup()
            upper_turtle.setposition(upper_endpoints[0])
            upper_turtle.pendown()
            upper_turtle.goto(upper_endpoints[1]) 
            screen.update()

    # then find the lower tangent
    lower_endpoints = [max(left_half), min(right_half)]
    lower_indices = [left_half.index(max(left_half)), right_half.index(min(right_half))]

    # draw each candidate tangent in red
    lower_turtle = Turtle(visible=False)
    if show_states:
        lower_turtle.speed(0)
        lower_turtle.pencolor('red')
        lower_turtle.penup()
        lower_turtle.setposition(lower_endpoints[0])
        lower_turtle.pendown()
        lower_turtle.goto(lower_endpoints[1]) 
        screen.update()

    while (
            get_side(lower_endpoints[0], lower_endpoints[1], next_ccw(right_half, lower_indices[1])) < 0 or 
            get_side(lower_endpoints[1], lower_endpoints[0], prev_ccw(left_half, lower_indices[0])) > 0
    ):
        if get_side(lower_endpoints[0], lower_endpoints[1], next_ccw(right_half, lower_indices[1])) < 0:
            lower_endpoints[1] = next_ccw(right_half, lower_indices[1]) 
            lower_indices[1] = right_half.index(lower_endpoints[1])
        else:
            lower_endpoints[0] = prev_ccw(left_half, lower_indices[0])
            lower_indices[0] = left_half.index(lower_endpoints[0])

        if show_states:
            sleep(TIME_STEP_DELAY)
            lower_turtle.clear()
            lower_turtle.penup()
            lower_turtle.setposition(lower_endpoints[0])
            lower_turtle.pendown()
            lower_turtle.goto(lower_endpoints[1]) 
            screen.update()

    # merge the left and right hulls using the upper and lower tangents
    if upper_indices[0] <= lower_indices[0]:
        merged_convex_hull = left_half[upper_indices[0] : lower_indices[0] + 1]
    else:
        merged_convex_hull = left_half[upper_indices[0] : ]
        merged_convex_hull.extend(left_half[ : lower_indices[0] + 1])

    if lower_indices[1] <= upper_indices[1]:
        merged_convex_hull.extend(right_half[lower_indices[1] : upper_indices[1] + 1])
    else:
        merged_convex_hull.extend(right_half[lower_indices[1] : ])
        merged_convex_hull.extend(right_half[ : upper_indices[1] + 1])

    upper_turtle.clear()
    lower_turtle.clear()
    left_turtle.clear()
    right_turtle.clear()

    # draw the merge convex hull and return it and the turtle used to draw it
    merge_turtle = Turtle(visible=False)
    if show_states:
        merge_turtle.speed(0)
        draw_connect_points(merged_convex_hull + [merged_convex_hull[0]], screen, merge_turtle)
    return merged_convex_hull, merge_turtle

def gift_wrap(points, screen, show_states):
    '''
        Returns the list of points in CCW order of the convex hull of the set of points
        The first point is the leftmost point
        Draws the steps taken in the processing
        Uses the Gift Wrap approach: O(n*k), where n is number of points and k is the number of points on the convex hull
    '''

    # get the lowest point in points (if there is a tie, take the leftmost one)
    lowest_point = min(points, key = lambda x: (x[1], x[0]))
   
    turtle = Turtle(visible=False)
    turtle.speed(0)

    cur_guess_turtle = Turtle(visible=False)
    cur_guess_turtle.speed(0)
    cur_guess_turtle.pencolor('red')

    # build the convex hull, adding points until the lowest point is reached again 
    convex_hull = []
    added_point = lowest_point
    while len(convex_hull) == 0 or added_point != convex_hull[0]:
        convex_hull.append(added_point)
        
        added_point = points[0]

        if show_states:
            cur_guess_turtle.penup()
            cur_guess_turtle.setposition(convex_hull[-1])
            cur_guess_turtle.pendown()
            cur_guess_turtle.goto(added_point)
            screen.update()

        # find the point which point for which all other points are to the right of the segment made by the last point added to the convex hull and it
        for i, point in enumerate(points):
            if i == 0:
                continue

            # show the current state
            if show_states:
                convex_hull.append(point)
                turtle.clear()
                draw_connect_points(convex_hull, screen, turtle)
                sleep(TIME_STEP_DELAY)
                convex_hull.pop()
            
            if get_side(convex_hull[-1], added_point, point) < 0:
                # if current point is right of current guess, update it to the guess
                added_point = point

                # show the current guess using a red line
                if show_states:
                    cur_guess_turtle.clear()
                    cur_guess_turtle.penup()
                    cur_guess_turtle.setposition(convex_hull[-1])
                    cur_guess_turtle.pendown()
                    cur_guess_turtle.goto(added_point)
                    screen.update()

    convex_hull.append(added_point)
    turtle.clear()
    return convex_hull

def graham_scan(points, screen, show_states):
    '''
        Returns the list of points in CCW order of the convex hull of the set of points
        The first point is the leftmost point
        Draws the steps taken in the processing
        Uses the Graham Scan approach: O(nlogn) where n is the number of points
    '''

    # sort the points by x value then by y value
    points = sorted(points)

    # build the upper hull
    upper_turtle = Turtle(visible=False)
    upper_turtle.speed(0)
    upper_hull_stack = []
    for i, point in enumerate(points):
        while len(upper_hull_stack) >= 2 and get_side(upper_hull_stack[-2], upper_hull_stack[-1], point) > 0:
            # display the current state of the upper hull
            if show_states:
                draw_connect_points(upper_hull_stack, screen, upper_turtle)
                sleep(TIME_STEP_DELAY)
                upper_turtle.clear()
             
            # if current point is a left turn, remove the last item
            upper_hull_stack.pop()

        upper_hull_stack.append(point)

    # show the upper hull 
    if show_states:
        draw_connect_points(upper_hull_stack, screen, upper_turtle)

    # build the lower hull
    lower_turtle = Turtle(visible=False)
    lower_turtle.speed(0)
    lower_hull_stack = []
    for i, point in enumerate(points):
        while len(lower_hull_stack) >= 2 and get_side(lower_hull_stack[-2], lower_hull_stack[-1], point) < 0:
            # display the current state of the lower hull
            if show_states:
                draw_connect_points(lower_hull_stack, screen, lower_turtle)
                sleep(TIME_STEP_DELAY)
                lower_turtle.clear()

            # if current point is a right turn, remove the last item
            lower_hull_stack.pop()

        lower_hull_stack.append(point)

    # show the lower hull
    if show_states:
        draw_connect_points(lower_hull_stack, screen, lower_turtle)

    # clear the hulls
    upper_turtle.clear()
    lower_turtle.clear()

    # put the upper and lower hull together and return them    
    upper_hull_stack.reverse()
    lower_hull_stack.extend(upper_hull_stack)
    return lower_hull_stack

if __name__ == "__main__":
    main(sys.argv)
