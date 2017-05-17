from priority import *
from copy import deepcopy

class Node: 
	'''node object for schedule tree'''
	def __init__(self, path, cost, units_left, current_term, per_quarter, taken, required, parent):
		# dictionary of path so far
		self.path = path

		# how many terms are already required/assigned, i.e., actual cost
		self.cost = cost

		# actual number of credits left to graduate
		self.units_left = units_left

		# current term being assigned to
		self.current_term = current_term

		# number of courses to assign per quarter
		self.per_quarter = per_quarter

		# set of courses have already either been previously taken or already assigned 
		self.taken = set(taken)

		# courses that need to be assigned for valid solution
		self.required = required

		# reference to parent
		self.parent = parent



	def addChild(self, course):
		'''returns node having assigned course to current term; increments term if full'''

		# copy path, add course to current term of new path
		new_path = deepcopy(self.path)
		new_path[self.current_term].append(course)

		# assign course to current term
		self.current_term.assigned.append(course)

		# copy full set of taken courses and add course to it
		new_taken = set(deepcopy(self.taken))
		new_taken.add(course)

		# copy term and cost, update if necessary
		next_term = deepcopy(self.current_term)
		new_cost = self.cost

		# check if this term is full
		if (len(next_term.assigned) >= self.per_quarter):
			# check if we're out of terms
			if (next_term.year == 2019 and next_term.name == "Winter"):
				print("out of terms")
				return None
			# otherwise, get next term and update cost
			next_term = self.current_term.next()
			new_cost = self.cost + 1

		return Node(new_path, self.cost, self.units_left - course.units, next_term,
					self.per_quarter, new_taken, self.required, self)

	def successor(self):
		''' returns all valid non-conflicting courses that can follow current node'''
		potential = []
		# if nothing is already assigned to this term, just check prerequisites
		if not self.current_term.assigned:
			potential = [course for course in self.current_term.offered if self.preqCheck(course)]
		# otherwise check prereqs and days
		else:
			potential = [course for course in self.current_term.offered if self.preqCheck(course) and self.dayCheck(course)]

		if not potential: 
			print("there are no successors")
		
		# filter courses that have already been taken
		potential = [course for course in potential if course not in self.taken]
		return potential

	def preqCheck(self, course):
		'''determines if course has all prerequisites met'''
		for and_preqs in course.prereqs:
			for or_preqs in and_preqs:
				if or_preqs in self.taken:
					# if one of the or's is satisfied, break out of inner loop, go back to outer
					break
				else:
					# if not, can't assign course 
					return False
		return True

	def dayCheck(self, course):
		'''checks if that day is open in current term'''
		for set_course in self.current_term.assigned:
			# if a course is already assigned to that day (which is not online)
			if set_course.day == course.day and (set_course.day != 0):
				return False
		return True

	def isTerminal(self):
		# check if units requirement is met
		if (self.units_left > 0):
			return False

		# check if all required courses are assigned
		for req in self.required:
			if req not in self.taken:
				return False

		# otherwise, this is a valid schedule
		return True

	def solution(self):
		return self.path

class Path:
	def __init__(self, taken, concentration, delivery, units):
		#TODO: Only input should be student ID, link these values to database

		# set of classes already taken
		self.taken = set(taken)

		# major concentration
		#TODO: link major concentration to database
		self.concentration = concentration

		# TODO: update courses to account for delivery type
		# delivery type: online-only -> -1 , in person only -> 0, hybrid -> 1
		self.delivery = 1

		# units already earned by student
		self.units = units



	def f(node):
		# heuristic for ordering priority queue: actual cost of this schedule (how many terms) 
		# + estimated heuristic (how many terms would it take without constraints)
		# + how many prereqs it requires (so that less constrained classes are explored first)
		# ideally would also sort by how constrained a course is 
		# i.e., assign courses that are most often prereqs for other courses first 
		# can do this sorting on the database itself after scraping
		return node.cost + (node.units_left - node.per_quarter * 4) 

	def aStar(root):
		''' a* search adapted from Norvig and Russels AI: A Modern Approach '''
		# priority queue sorted by f for checking paths
		frontier = Priority(Path.f)
		frontier.push(root) 

		# set for containing paths that have already been considered
		explored = set()

		count = 0 
		space = 0

		# while queue is not empty
		while frontier:
			current = frontier.pop() # get lowest cost node
			count += 1
			# if this current schedule is complete, this is shortest path
			if current.isTerminal():
				print("Solved")
				print(count )
				return current.path
			# else, consider this set of classes as already having been explored
			explored.add(tuple(current.taken))

			# for all available actions
			for course in current.successor():
				child = current.addChild(course)
				# if this course assignment hasn't been seen before, push it onto the queue
				if (child not in frontier) and (tuple(child.taken) not in explored):
					frontier.push(child)
				# otherwise, if it is already on the queue, take lower costing path
				elif (child in frontier):
					check = frontier.get(child)
					if (f(child) < f(check)):
						frontier.remove(check)
						frontier.push(child)
			# maintain max frontier size
			if len(frontier) > space:
				space = len(frontier)

		print("failed at count of ", count)
		return current.path
