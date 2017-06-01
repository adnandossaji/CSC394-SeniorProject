class DummyCourse:
    '''course objects'''
    def __init__(self, course_id, prereqs, units, day):
        # course id
        self.course_id = course_id

        # each course has an associated list of prereqs (a list containing other course objects)
        self.prereqs = prereqs

        # int: number of credits the course counts for
        self.units = units
        
        # day that class is held, integer: 1 = Monday, ..., 4 = Thursday, 0 = online; 
        self.day = day

    def __repr__(self):
        return str(self.course_id)

    def __eq__(self, other):
        return self.course_id == other
