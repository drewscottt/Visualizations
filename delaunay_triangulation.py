'''
    File: delaunay_triangulation.py
    Author: Drew Scott
    Description:
'''

from random import randint, choice
from turtle import Turtle, Screen
from time import sleep
import sys

from convex_hull import divide_conquer
from util import get_side, prev_ccw, next_ccw, draw_connect_points, DOT_RADIUS, BORDER_PADDING, DCEL, Vertex_DCEL, HalfEdge_DCEL, Face_DCEL

N_POINTS = 100
BOTTOM_TEXT_HEIGHT = 0

def main(args):
    # set up the screen
    screen = Screen()
    width, height = screen.window_width(), screen.window_height()
    screen.tracer(0, 0)

    # generate and draw the points
    points = []
    points = [(-190, 68), (-55, -95), (-153, 35), (-152, -172), (-215, -214), (-275, -31), (115, 17), (94, 296), (-142, 149), (-78, -8), (-84, 251), (-259, 53), (194, -66), (-177, -179), (21, -51), (269, 110), (-226, -114), (-152, 103), (245, 100), (-162, 59), (-159, 96), (90, 23), (-302, 305), (209, -201), (-327, -236), (-82, -139), (196, 172), (46, -17), (-33, 229), (-178, -148), (286, -287), (-327, 78), (64, 61), (186, -298), (-272, 197), (140, -306), (-195, 291), (309, 64), (65, -20), (-76, 95), (-103, 50), (-273, 202), (284, 267), (41, -209), (-173, 134), (91, 52), (1, -46), (-45, -304), (-203, -4), (244, -293), (-143, 249), (-256, 50), (52, -10), (-217, -191), (306, -64), (71, 101), (-309, -207), (224, -107), (291, 17), (279, 120), (-228, 44), (-338, -197), (261, 99), (295, 307), (278, 45), (314, -242), (184, -114), (201, 283), (125, -247), (248, -247), (281, 18), (55, 307), (79, 215), (-304, -143), (313, -75), (251, -151), (175, 146), (189, 311), (-122, 166), (-168, 259), (-5, -39), (308, 140), (159, 240), (276, -235), (6, -191), (184, -110), (-261, 82), (-181, 118), (-206, -269), (-318, -128), (220, 202), (110, 169), (253, 93), (82, 205), (-288, -204), (-43, 275), (-92, -52), (-228, 175), (-46, 311), (-249, 254)]
    points_turtle = Turtle(visible=False)
    points_turtle.speed(0)
    for i in range(N_POINTS):
#        new_loc = (randint((-width//2) + BORDER_PADDING, (width//2) - BORDER_PADDING), randint((-height//2) + BORDER_PADDING + BOTTOM_TEXT_HEIGHT, (height//2) - BORDER_PADDING))
#        points.append(new_loc)
        points_turtle.penup()
        points_turtle.setposition(points[i])
        points_turtle.pendown()
        points_turtle.dot(DOT_RADIUS, 'black')
    screen.update()
    print(points)

    # compute the triangulation
    delaunay_dag = delaunay_triangulation(points, screen, True)
    draw_dag(delaunay_dag, screen)

    screen.exitonclick()

def draw_dag(dag, screen):
    if len(dag.children) == 0:
        # at the leaf, so draw this triangle
        turtle = Turtle(visible=False)
        turtle.speed(0)
        turtle.penup()
        turtle.setposition(dag.vertices[0])
        turtle.pendown()
        turtle.goto(dag.vertices[1])
        turtle.goto(dag.vertices[2])
        turtle.goto(dag.vertices[0])
        screen.update()
    else:
        for child in dag.children:
            draw_dag(child, screen)

class Delaunay_DAG_Node():
    def __init__(self):
        self.children = []
        self.vertices = None
        self.dcel_face: Face_DCEL = None

    def add_child(self, child_node):
        self.children.append(child_node)

    def set_vertices(self, vertices):
        self.vertices = vertices

    def is_inside(self, point):
        if self.vertices is None:
            return False

        # a point is inside this triangle if is to the left of all the segments or the right of all the segments
        if (
            (get_side(self.vertices[0], self.vertices[1], point) > 0 and
            get_side(self.vertices[1], self.vertices[2], point) > 0 and
            get_side(self.vertices[2], self.vertices[0], point) > 0)
            or
            (get_side(self.vertices[0], self.vertices[1], point) < 0 and
            get_side(self.vertices[1], self.vertices[2], point) < 0 and
            get_side(self.vertices[2], self.vertices[0], point) < 0)
        ):
            return True
        else:
            return False

    def on_edge(self, point):
        if (
            (get_side(self.vertices[0], self.vertices[1], point) == 0 or
            get_side(self.vertices[1], self.vertices[2], point) == 0 or
            get_side(self.vertices[2], self.vertices[0], point) == 0)
        ):
            return True
        else:
            return False

def delaunay_triangulation(points, screen, show_states):
    '''
    '''

    # compute and draw the convex hull
    convex_hull = divide_conquer(points, screen, False)
    convex_hull_set = set(convex_hull)
    if show_states:
        ch_turtle = Turtle(visible=False)
        ch_turtle.speed(0)
        draw_connect_points(convex_hull, screen, ch_turtle)

    # build the triangulation
    root = None
    dcel = DCEL()
    for point in points:
        if point in convex_hull_set:
            continue

        if root is None:
            # connect the first point to all the points on the convex hull
            root = Delaunay_DAG_Node()
            center_vertex: Vertex_DCEL = Vertex_DCEL(point)
            prev_vertex: Vertex_DCEL = None
            first_edge: HalfEdge_DCEL = None
            prev_edge: HalfEdge_DCEL = None

            for i, ch_point in enumerate(convex_hull):
                if i == 0:
                    prev_vertex = Vertex_DCEL(ch_point)
                    continue

                # add this triangle to the DCEL
                new_vertex = Vertex_DCEL(ch_point)
                edge1 = HalfEdge_DCEL(prev_vertex)
                edge2 = HalfEdge_DCEL(new_vertex)
                edge3 = HalfEdge_DCEL(center_vertex)
                new_face = Face_DCEL()

                new_vertex.incident_edge = edge1
                new_face.edge = edge1
                edge1.incident_face = new_face 
                edge2.incident_face = new_face 
                edge3.incident_face = new_face 
                edge1.next = edge2 
                edge2.next = edge3
                edge3.next = edge1 
                edge1.prev = edge3
                edge2.prev = edge1
                edge3.prev = edge2
                if i > 1:
                    edge3.twin = prev_edge
                    prev_edge.twin = edge3
                    if i == len(convex_hull) - 1:
                        first_edge.twin = edge2
                        edge2.twin = first_edge
                else:
                    first_edge = edge3
                    prev_edge = edge2 

                dcel.vertices.append(new_vertex)
                dcel.half_edges.append(edge1)
                dcel.half_edges.append(edge2)
                dcel.half_edges.append(edge3)
                dcel.faces.append(new_face)

                prev_vertex = new_vertex 

                # add this triangle to the DAG
                new_node = Delaunay_DAG_Node()
                new_node.set_vertices([convex_hull[i - 1], ch_point, point])
                new_node.dcel_face = new_face
                root.add_child(new_node)
        else:
            # traverse the DAG into the leaf node which contains the point
            cur_node = root
            on_edge = False
            is_inside = False
            while len(cur_node.children) > 0:
                for child_node in cur_node.children:
                    is_inside = child_node.is_inside(point)
                    on_edge = child_node.on_edge(point)
                    if is_inside or on_edge:
                        cur_node = child_node
                        break

                if not is_inside and not on_edge:
                    assert(False)

            # split the triangle appropriately
            if is_inside:
                new_vertex = Vertex_DCEL(point)
                dcel.vertices.append(new_vertex)

                # get the face which contains this point from the dcel
                big_face = cur_node.dcel_face
                outer_edge1 = big_face.edge
                outer_edge2 = outer_edge1.next
                outer_edge3 = outer_edge2.next
                dcel.faces.remove(big_face)

                # create the new half edges for the 3 newly created faces
                new_face1 = Face_DCEL()
                new_edge11 = HalfEdge_DCEL(new_vertex)
                new_edge11.next = outer_edge1
                outer_edge1.prev = new_edge11
                new_edge12 = HalfEdge_DCEL(outer_edge1.next.origin_vertex)
                outer_edge1.next = new_edge12
                new_edge12.prev = outer_edge1
                new_edge12.next = new_edge11
                new_edge11.prev = new_edge12
                dcel.faces.append(new_face1)
                dcel.half_edges.append(new_edge11)
                dcel.half_edges.append(new_edge12)

                new_face2 = Face_DCEL()
                new_edge21 = HalfEdge_DCEL(new_vertex)
                new_edge21.next = outer_edge2
                outer_edge2.prev = new_edge21
                new_edge22 = HalfEdge_DCEL(outer_edge2.next.origin_vertex)
                outer_edge2.next = new_edge22
                new_edge22.prev = outer_edge2
                new_edge22.next = new_edge21
                new_edge21.prev = new_edge22
                dcel.faces.append(new_face2)
                dcel.half_edges.append(new_edge21)
                dcel.half_edges.append(new_edge22)

                new_face3 = Face_DCEL()
                new_edge31 = HalfEdge_DCEL(new_vertex)
                new_edge31.next = outer_edge3
                outer_edge3.prev = new_edge31
                new_edge32 = HalfEdge_DCEL(outer_edge3.next.origin_vertex)
                outer_edge3.next = new_edge32
                new_edge32.prev = outer_edge3
                new_edge32.next = new_edge31
                new_edge31.prev = new_edge32
                dcel.faces.append(new_face3)
                dcel.half_edges.append(new_edge31)
                dcel.half_edges.append(new_edge32)

                # set the twin edges for each new edge
                new_edge11.twin = new_edge32
                new_edge32.twin = new_edge11
                new_edge21.twin = new_edge12
                new_edge12.twin = new_edge21
                new_edge31.twin = new_edge22
                new_edge22.twin = new_edge31

                # create DAG nodes for the faces
                new_node1 = Delaunay_DAG_Node()
                new_node1.set_vertices([point, outer_edge1.origin_vertex.coordinate, new_edge12.origin_vertex.coordinate])
                new_node1.dcel_face = new_face1`
                cur_node.add_child(new_node1)
                new_node2 = Delaunay_DAG_Node()
                new_node1.set_vertices([point, outer_edge2.origin_vertex.coordinate, new_edge22.origin_vertex.coordinate])
                new_node2.dcel_face = new_face2
                cur_node.add_child(new_node2)
                new_node3 = Delaunay_DAG_Node()
                new_node1.set_vertices([point, outer_edge3.origin_vertex.coordinate, new_edge32.origin_vertex.coordinate])
                new_node3.dcel_face = new_face3
                cur_node.add_child(new_node3)

                # check for edge flips
                edge_flip(outer_edge1)
                edge_flip(outer_edge2)
                edge_flip(outer_edge3)
            elif on_edge:
                # TODO
                turtle.penup()
                turtle.setposition(point)
                turtle.pendown()
                turtle.dot(DOT_RADIUS, 'green')
            else:
                assert(False)

    return root

def edge_flip(dcel_edge):
    # TODO
   pass  

if __name__ == '__main__':
    main(sys.argv)
