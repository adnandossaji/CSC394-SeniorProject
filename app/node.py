from copy import copy

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
		new_taken = copy(self.taken)
		new_taken_overall = copy(self.taken_overall)

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
		new_assigned.append(course.course_id)
		
		# add course to taken overall
		new_taken_overall.add(course.course_id)

		# add day if not online 
		if (course.day != 0):
			new_days.append(course.day)


		return Node(new_num_quarters, new_assigned,  new_taken, new_taken_overall, new_days, 
					self.units_left - course.units, new_quarter, new_year, self.per_quarter, self)


	''' generates solution by working up to root of tree '''
	def solution(self):
		# store path in dictionary
		path = {}

		# copy terminal node to consume up to root
		current = self
		
		while (current.parent != None):
			current_term = current.quarter + str(current.year)
			# keep going up tree until a novel term is reached
			if current_term in path:
				current = current.parent
				continue
			else:
				# if novel term, add assigned courses
				path[current_term] = current.assigned

			current = current.parent

		return path
		

	''' checks if course has prerequisites already met '''
	def preqCheck(self, course):
		# check if empty		
		if len(course.prereqs) == 1:
			if not course.prereqs[0]:
				return True


		for and_clause in course.prereqs:
			# boolean to see if at least 1 'or' is met (resets every and-clause) 
			someMet = False
			for or_clause in and_clause:
				if or_clause.course_id in self.taken:
					# don't need to check rest of or_clause
					someMet = True
					break
			if (someMet == False):
				return False
		return True

	''' helper function to get next quarter '''
	def getNextQuarter(self):
		# dictionary to switch with
		nextQuarters = {"Fall": ("Winter", self.year+1) , "Winter": ("Spring", self.year), 
						"Spring": ("Summer", self.year), "Summer": ("Fall", self.year)}

		return nextQuarters[self.quarter]





