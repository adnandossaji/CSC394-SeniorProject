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

        count = 0

        max = int(root.year + ((root.units_left / root.per_quarter) / 4))

        # while queue is non-empty
        while frontier:
            count += 1
            current = frontier.pop()

            # if this meets all requirements, build path dictionary and return it
            if Search.isTerminal(current, required, electives, num_electives, max):
                return current.solution()

            # consider this set of courses as having been explored
            explored.add(tuple(current.taken_overall))

            # for all valid courses
            for course in Search.validCourses(current, offered):
                # import pdb
                # pdb.set_trace()
                # construct child node 
                child = current.addChild(course)
                # if this schedule hasn't been seen before and is not already in the queue
                if (tuple(child.taken_overall) not in explored) and child not in frontier):
                    # add it to the queue
                    frontier.push(child)
                # if it is already on the queue, only consider the least cost one
                elif child in frontier):
                    # replace if less than
                    frontier.replace(child)

        print("=" * 10)
        print(current.__dict__)
        print(offered)
        print("=" * 10)
        print(count)
        print("=" * 10)

        # if queue is empty, search failed
        print("search failed")
        print(current.taken)
        print(current.taken_overall)
        return False

    ''' successor function: returns list of all possible courses that can be assigned '''
    def validCourses(n, offered):
        
        available = []
        new_quarter = n.quarter

        # if assigned is full, this is a new quarter, check next quarter
        if (len(n.assigned) == n.per_quarter):
            (new_quarter, new_year) = n.getNextQuarter()

        for course in offered[new_quarter]:
            subject = course.split(" ")[0]
            number = course.split(" ")[1]
            q_course = Course.query.filter_by(subject = subject).filter_by(course_number = number).first()

            if (subject+" "+number) not in n.taken_overall and n.preqCheck(q_course) and q_course.day_of_week not in n.days:
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
    def isTerminal(n, required, electives, num_electives, max):
        # check that units requirement was met

        if (n.year == (max)):
            return True 

        if (n.units_left > 0):
            return False

        # check if all required courses were taken
        for req in required:
            if req not in n.taken_overall:
                print("=" * 10)
                print(req)
                print("=" * 10)
                return False

        # check that electives were taken
        elec_count = 0
        for elec in electives:
            if elec.course_id in n.taken_overall:
                elec_count += 1

        if elec_count < num_electives:
            return False

        return True

