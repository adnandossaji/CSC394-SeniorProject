import copy
import collections
from app.preq_tree import *
from app.models import *


class Node:
	'''node object representing each assignment'''
	def __init__(self, num_quarters, assigned, taken, taken_overall, days, units_left, quarter, year, per_quarter, parent):
		# how many terms needed so far
		self.num_quarters = num_quarters

		# courses assigned to this term
		self.assigned = assigned

		# set of courses taken so far (not including those assigned to current quarter for checking prerequisites)
		self.taken = taken

		# set of courses taken overall (including those assigned to current quarter)
		self.taken_overall = taken_overall

		# list of days already occupied (not online)
		self.days = days

		# units left to graduate
		self.units_left = units_left 

		# current quarter 
		self.quarter = quarter

		# current year
		self.year = year

		# max classes to assign per quarter
		self.per_quarter = per_quarter


		# parent node
		self.parent = parent

	'''adds course to current term, updates term/cost, returns new node'''
	def addChild(self, course):
		# copy courses taken so far and overall
		new_taken = copy.copy(self.taken)
		new_taken_overall = copy.copy(self.taken_overall)

		# if assigned is full, this is a new quarter, start with new quarter lists, update number of terms
		if (len(self.assigned) == self.per_quarter):
			new_assigned = []
			new_days = []
			(new_quarter, new_year) = self.getNextQuarter()
			new_num_quarters = self.num_quarters + 1
			new_taken.update(self.assigned)
		else:
			new_assigned = self.assigned[:]
			new_days = self.days[:]
			new_quarter = self.quarter
			new_year = self.year
			new_num_quarters = self.num_quarters

		

		# add given course to node and set of taken classes
		new_assigned.append("{} {}".format(course.subject, course.course_number))
		
		# add course to taken overall
		new_taken_overall.add("{} {}".format(course.subject, course.course_number))
		
		# # add day if not online 
		# if (course.day_of_week != 0) and (delivery_type >= 0):
		# 	new_days.append(course.day_of_week)

		return Node(new_num_quarters, new_assigned,  new_taken, new_taken_overall, new_days, 
					self.units_left - course.credits, new_quarter, new_year, self.per_quarter, self)


	''' generates solution by working up to root of tree '''
	def solution(self):
		# store path in dictionary
		path = collections.OrderedDict()

		# copy terminal node to consume up to root
		current = self
		
		while (current.parent != None):
			current_term = current.quarter + " " + str(current.year)
			# keep going up tree until a novel term is reached
			if current_term in path:
				current = current.parent
				continue
			else:
				# if novel term, add assigned courses; filter dummy courses
				assigned = [course for course in current.assigned if course != "None None"]
				path[current_term] = assigned

			current = current.parent

		return path
		

	''' checks if course has prerequisites already met '''
	def preqCheck(self, course):
		# check if this is dummy course
		if course.subject == "None":
			return True

		# check cases for no prequisite
		if course.prereq == "None":
			return True
		elif course.prereq == "":
			return True
		elif not course.prereq:
			return True
		# check if single course in taken
		elif course.prereq in self.taken:
			return True
		# if no courses assigned and prereq not empty
		elif not self.taken:
			return False
		else:
			# build boolean expression tree, evaluate and return
			a = bool_tree()
			a.root = a.tree_from_prereq_str(course.prereq)
			return a.evaluate(list(self.taken))

	''' helper function to get next quarter '''
	def getNextQuarter(self):
		# dictionary to switch with
		nextQuarters = {"Autumn": ("Winter", self.year+1) , "Winter": ("Spring", self.year), 
						"Spring": ("Summer", self.year), "Summer": ("Autumn", self.year)}

		return nextQuarters[self.quarter]


	def __lt__(self, other):
		return f(self) < f(other)



