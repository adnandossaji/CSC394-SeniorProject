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
    # basic test data, should link to database here
    # TODO: add summer and spring
    CS301 = Course(301, [[]], 4, 0)
    CS302 = Course(302, [[]], 4, 3)
    CS321 = Course(321, [[301, 302]], 4, 0)
    CS373 = Course(373, [[]], 4, 2)
    CS374 = Course(374, [[CS373], [CS301, CS302]], 4, 3)
    CS347 = Course(347, [[CS373], [CS301, CS302]], 4, 0)
    CS480 = Course(480, [[CS321], [CS302], [CS301], [CS373, CS347]], 4, 0)
    No    = Course(0, [[]], 0, 0)
    Elec = Course(1, [[]], 4, 0)


    off = {"Fall": [CS301, CS373, CS347, No, Elec], "Winter": [CS302, CS480, CS347, No, Elec]}
    ''' term object, TODO: link to database '''
    def __init__(self, name, year, assigned, offered):
        CS301 = Course(301, [[]], 4, 0)
        CS302 = Course(302, [[]], 4, 3)
        CS321 = Course(321, [[301, 302]], 4, 0)
        CS373 = Course(373, [[]], 4, 2)
        CS374 = Course(374, [[CS373], [CS301, CS302]], 4, 3)
        CS347 = Course(347, [[CS373], [CS301, CS302]], 4, 0)
        CS480 = Course(480, [[CS321], [CS302], [CS301], [CS373, CS347]], 4, 0)

        # year of course
        self.year = year
        
        # term name, e.g., summer, winter etc.
        self.name = name
        
        # list of courses (course objects) offered that year
        self.offered = offered
        
        # already assigned courses this term
        self.assigned = assigned

        self.off = {"Fall": [CS301, CS373, CS347], "Winter": [CS301, CS347, CS480]}

    def next(self):
        if self.name == "Fall":
            return Term("Winter", self.year, self.assigned, self.off["Winter"][:])
        else:
            return Term("Fall", self.year + 1, self.assigned, self.off["Fall"][:])
       
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
