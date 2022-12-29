'''
    File: util.py
    Author: Drew Scott
    Description: Contains several utility functions for visualizations
'''

from turtle import Turtle, Screen
from typing import Tuple, List
from numbers import Number

DOT_RADIUS = 5
BORDER_PADDING = 20

def draw_connect_points(points, screen, turtle):
    '''
        Draws a line between each points[i], points[i+1] pair of points in points
    '''

    prev_point = points[0]
    turtle.penup()
    turtle.setposition(prev_point)
    turtle.pendown()
    turtle.dot(DOT_RADIUS, 'red')
    for i, point in enumerate(points):
        if i == 0:
            continue
        turtle.goto(point)
        turtle.dot(DOT_RADIUS, 'red')
        prev_point = point 

    screen.update()


def prev_ccw(points, index):
    '''
        Returns the point preceding the point at index in ccw order from points
    '''

    if index == 0:
        return points[-1]
    else:
        return points[index - 1]

def next_ccw(points, index):
    '''
        Returns the point succeeding the point at index in ccw order from points
    '''

    if index == len(points) - 1:
        return points[0]
    else:
        return points[index + 1]

def get_side(point1, point2, point3):
    '''
        Returns which side point3 is on of segment point1-point2
        Positive if left, negative if right, 0 if collinear
    '''
    
    return ((point2[0] - point1[0])*(point3[1] - point1[1]) - (point2[1] - point1[1])*(point3[0] - point1[0]))

class DCEL():
    def __init__(self):
        self.vertices: List[Vertex_DCEL] = []
        self.half_edges: List[HalfEdge_DCEL] = []
        self.faces: List[Face_DCEL] = []

class Vertex_DCEL():
    def __init__(self, coordinate: Tuple[Number, Number]):
        self.coordinate: Tuple[Number, Number] = coordinate
        self.incident_edge: HalfEdge_DCEL = None

class HalfEdge_DCEL():
    def __init__(self, origin_vertex: Vertex_DCEL):
        self.origin_vertex: Vertex_DCEL = origin_vertex
        self.incident_face: Face_DCEL = None
        self.twin: HalfEdge_DCEL = None
        self.next: HalfEdge_DCEL = None
        self.prev: HalfEdge_DCEL = None

class Face_DCEL():
    def __init__(self):
        self.edge: HalfEdge_DCEL = None 

