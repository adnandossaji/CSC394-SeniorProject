class Course:
    '''course objects (domains)'''
    def __init__(self, course_id, prereqs, units, day):
        # TODO: link to database
        
        # course id (are these unique?)
        self.course_id = course_id

        # each course has an associated list of prereqs (a list containing other course objects)
        self.prereqs = prereqs
    
        # int: number of credits the course counts for
        self.units = units
        
        # day that class is held, integer: 1 = Monday, ..., 4 = Thursday, 0 = online; 
        self.day = day

    # when representing coures, give just course_id as integer
    def __repr__(self):
        return str(self.course_id)        
    
    def __str__(self):
        return str(self.course_id)
    
    # when adding courses, give course units value as integer
    def __radd__(self, other):
        return self.units + other
    
    def __add__(self, other):
        return self.units + other

    def __hash__(self):
        return self.course_id

    def __eq__(self, other):
        return self.course_id == other.course_id

class Term: 
    ''' term object, TODO: link to database '''
    def __init__(self, name, year, assigned, offered):
        # basic test data, should link to database here
        # intro
        CS400 = Course(400, [[]], 4, 0)
        CS401 = Course(401, [[]], 4, 1)
        CS402 = Course(402, [[CS401]], 4, 2)
        CS403 = Course(403, [[CS402]], 4, 1)
        CS406 = Course(406, [[CS401]], 4, 2)
        CS407 = Course(407, [[CS406], [CS402]], 4, 2)

        intro = [CS400, CS401, CS402, CS403, CS406, CS407]

        # foundation
        CS421 = Course(421, [[CS400], [CS403]], 4, 3)
        CS435 = Course(435, [[CS403], [CS407]], 4, 0)
        CS447 = Course(447, [[CS403], [CS406]], 4, 2)
        CS453 = Course(453, [[CS403]], 4, 0)
        SE450 = Course(450, [[CS403]], 4, 1)

        foundation = [CS421, CS435, CS447, CS453, SE450]

        # concentration (software and systems development)
        CS436 = Course(436, [[CS435], [CS447]], 4, 0)
        CS438 = Course(438, [[CS407]], 4, 2)
        CS461 = Course(461, [[CS400], [CS403], [CS406]], 4, 0)
        CS472 = Course(472, [[CS403], [CS407]], 4, 0)
        CS552 = Course(552, [[SE450], [CS407]], 4, 1)
        CS595 = Course(595, [[]], 4, 0)
        SE452 = Course(452, [[CS403]], 4, 2)
        SE459 = Course(459, [[SE450]], 4, 0)
        SE491 = Course(491, [[SE450]], 4, 3)

        concentration = [CS436, CS438, CS461, CS472, CS552, CS595, SE459, SE491]
        everyterm = intro + foundation + concentration

        self.off = {"Fall": everyterm, "Winter": everyterm, "Spring": everyterm, "Summer": everyterm}
        # year of course
        self.year = year
        
        # term name, e.g., summer, winter etc.
        self.name = name
        
        # list of courses (course objects) offered that year
        self.offered = offered
        
        # already assigned courses this term
        self.assigned = assigned


    def next(self):
        if (self.name == "Winter"):
            return Term("Spring", self.year, [], self.off["Spring"][:])
        elif (self.name == "Spring"):
            return Term("Summer", self.year, [], self.off["Winter"][:])
        elif (self.name == "Summer"):
            return Term("Fall", self.year, [], self.off["Fall"][:])
        else:
            return Term("Winter", self.year + 1, [], self.off["Winter"][:])
       
    def __lt__(self, other):
        return id(self) < other(self)
    
    
    def __eq__(self, other):
        return self.year == other.year and self.name == other.name 
    
    def __hash__(self):
        if self.name == "Fall":
            return self.year*10 + 1 
        elif self.name == "Winter":
            return self.year*10 + 2 
        else:
            return self.year*10 + 3 
    
    def __repr__(self):
        return self.name + str(self.year)
    
    def __str__(self):
        return self.name + str(self.year) 
