from app.node import Node
from app.priority import Priority
from app.course import *

# this is the only place we need to connect to the database, and only to give parameters to a root node

class Search:
    # TODO: link here to database
    #use database to set up root node () and courses offered by quarter (treated here as a dictionary)


    ''' a* algorithm for searching for shortest path adapted from psuedocode of Norvig and Russel's AI: A Modern Approach '''
    def aStar(root, offered, required, electives):
        # priority queue with quick lookup prioritized by heuristic function f
        frontier = Priority(Search.f)

        # set for determining if schedule has already been considered
        explored = set()

        # push root onto frontier 
        frontier.push(root)

        # while queue is non-empty
        while frontier:
            current = frontier.pop()

            # if this meets all requirements, build path dictionary and return it
            if Search.isTerminal(current, required, electives):
                return current.solution()

            # consider this set of courses as having been explored
            explored.add(tuple(current.taken))

            # for all valid courses
            for course in Search.validCourses(current, offered):
                # construct child node 
                child = current.addChild(course)
                # if this schedule hasn't been seen before and is not already in the queue
                if (tuple(child.taken_overall) not in explored) and (tuple(child.taken_overall) not in frontier):
                    # add it to the queue
                    frontier.push(child)
                # if it is already on the queue, only consider the least cost one
                elif (tuple(child.taken_overall) in frontier):
                    # replace if less than
                    frotier.replace(child)

        # if queue is empty, search failed
        print("search failed")
        print(current.taken)
        return False

    ''' successor function: returns list of all possible courses that can be assigned '''
    def validCourses(n, offered):
        available = [course for course in offered[n.quarter] if course.course_id not in n.taken_overall and 
                     n.preqCheck(course) and course.day not in n.days]

        # add non-course, i.e., not taking a course
        available.append(Course(0, [[]], 0, 0))

        return available

    ''' heuristic function for prioritizing queue '''
    ''' lower bound of path cost given by adding actual terms needed so far + estimate of terms to go from relaxed constraints'''
    def f(n):
        units_to_go = n.units_left
        quarters_so_far = n.num_quarters

        # get number of actual courses
        this_quarter = len([course for course in n.assigned if course != 0])
        
        # if there are already courses assigned this quarter (and this quarter isn't already full)
        if (this_quarter > 0 and this_quarter != n.per_quarter): 
        # add units back from this quarter and decrement quarters taken 
            units_to_go = units_to_go + 4*this_quarter
            quarters_so_far -= 1
        
        # f(n) = cost so far + estimate for cost to go (they can take as many courses as possible every quarter)
        return quarters_so_far + (units_to_go - 4 * n.per_quarter)


    ''' determines if current node is a valid path to graduation ''' 
    def isTerminal(n, required, electives):
        # check that units requirement was met
        if (n.units_left > 0):
            return False

        # check if all required courses were taken
        for req in required:
            if req.course_id not in n.taken_overall:
                return False

        # check that electives were taken
        elec_count = 0
        for elec in electives:
            if elec.course_id not in n.taken_overall:
                elec_count += 1

        if elec_count < 1:
            return False

        return True

