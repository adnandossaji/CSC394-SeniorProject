from app.node import Node
from app.priority import Priority
from app.dummyCourse import *
from app.models import *

# this is the only place we need to connect to the database, and only to give parameters to a root node

class Search:

    ''' a* algorithm for searching for shortest path adapted from psuedocode of Norvig and Russel's AI: A Modern Approach '''
    def aStar(root, offered, required, electives, num_electives):
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
            if Search.isTerminal(current, required, electives, num_electives):
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
        
        available = []
        new_quarter = n.quarter

        # if assigned is full, this is a new quarter, check next quarter
        if (len(self.assigned) == self.per_quarter):
            (new_quarter, new_year) = self.getNextQuarter()

        for course in offered[new_quarter]:
            subject = course.split(" ")[0]
            number = course.split(" ")[1]
            q_course = Course.query.filter_by(subject = subject).filter_by(course_number = number).first()

            if (subject+" "+number) not in n.taken_overall and n.preqCheck(course) and course.day_of_week not in n.days:
                available.append(q_course)

        # add non-course, i.e., not taking a course
        dummy_course = Course(
            subject = "",
            course_number = "None",
            prereq = "None",
            day_of_week = 0,
            credits = 0,
            description = "",
            quarter_offered = n.quarter,
            delivery_method = ""
        )

        available.append(dummy_course)

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
    def isTerminal(n, required, electives, num_electives):
        # check that units requirement was met
        if (n.year == 2024):
            return True 

        if (n.units_left > 0):
            print("here 1")
            return False

        # check if all required courses were taken
        for req in required:
            if req not in n.taken_overall:
                print("here 2")
                return False

        # check that electives were taken
        elec_count = 0
        for elec in electives:
            if elec.course_id not in n.taken_overall:
                elec_count += 1

        if elec_count < num_electives:
            print("here 3")
            return False

        return True

