# scraper prototype
import webbrowser
from contextlib import closing
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlencode, quote_plus


# DEPENDENCIES:
# bs4 (beautiful soup)
# lxml (xml parser that beautiful soup needs)

SUBJECT_LIST = ['CSC', 'IT', 'IS', ]

class parser(object):
    def __init__(self):
        self.entries, self.page, self.soup = self.initParser()
        self.results = self.separateCourseInfo(self.entries, self.page, self.soup)

    def init_parser(self):
        # COURSE_CATALOG = "http://www.cdm.depaul.edu/academics/Pages/CourseCatalog.aspx"
        COURSE_CATALOG = "http://odata.cdm.depaul.edu/Cdm.svc/Courses?$filter=IsCdmGeneral"

        with closing(urlopen(COURSE_CATALOG)) as page:
            xml = page.read()
            soup = BeautifulSoup(xml, features="xml")
            print("=======================================")
            print(" >>> PARSER SUCCESSFULLY CREATED <<<")
            print("=======================================")
            # separates XML by entry
            entries = soup.findAll('entry')
            # removes everything outside of content tag
            content = [s.find('content') for s in entries]
        return content, page, soup

    def separate_course_info(self, entries, page, parser):
        # print(entries)
        # print(page)
        # print(parser)

        # EO == Every Other
        def check_typically_offered(entry):
            if (get_typically_offered(entry)) == " ":
                return ['Not Offered']
            else:
                typ = get_typically_offered(entry).split('/') #.replace(' Terms', '').replace(' Term', '')
                print(typ)
                if typ[0] == 'Every Term':      return ['Autumn', 'Winter', 'Spring']
                else:                           return [qtr.replace(' Terms', '').replace(' Term', '').replace('Every Other', 'EO') for qtr in typ]

        # strips and formats prerequisites from the parsed XML
        def get_prereqs(entry):
            # print(entry)
            idx = entry.find('PREREQUISITE(S)')
            # print(idx)
            if idx == -1:
                return 'None'
            tmp = len('PREREQUISITE(S):')
            # print(entry[idx + tmp::].strip())
            return entry[idx + tmp::].strip()

        ## fxn that determines if a class is IS or CS
        #  global SUBJECT_LIST : list(str) should be
        #  modified based on the courseSubjects that
        #  you want to pull in
        def is_csc(entry):
            if get_subject(entry) in SUBJECT_LIST and len(get_course_num(entry)) == 3 and int(get_course_num(entry)) >= 400:
                return True
            else:
                return False

        # IC == in class only
        # O  == online only
        # B  == inclass and online
        # N  == Not Offered
        def pop_delivery_type(entry):
            if str(in_class_only(entry)).upper() == 'TRUE':
                return 'IC'

            elif str(online_only(entry)).upper() == 'TRUE':
                return 'O'

            elif str(both(entry)).upper() == 'TRUE':
                return 'B'

            elif str(is_offered(entry)).upper() == 'False':
                return 'N'

        # These are lambda functions so that course objects can be created from the parsed xml
        # in a list comprehension
        get_subject           = lambda entry: entry.find('properties').find('SubjectId').contents[0]
        get_course_num        = lambda entry: entry.find('properties').find('CatalogNbr').contents[0] # >= 400
        get_typically_offered = lambda entry: entry.find('properties').find('TypicallyOffered').contents[0]
        get_long_descr        = lambda entry: entry.find('properties').find('DescrLong').contents[0]
        in_class_only         = lambda entry: entry.find('properties').find('IsInClassOnly').contents[0]
        online_only           = lambda entry: entry.find('properties').find('IsOnlineOnly').contents[0]
        both                  = lambda entry: entry.find('properties').find('IsInClassAndOnline').contents[0]
        is_offered            = lambda entry: entry.find('properties').find('IsNotOffered').contents[0]

        # Lambda fxn that packs course information into data dictionary
        pack_course = lambda entry: {
                                    'subject'           : get_subject(entry),
                                    'course_number'     : get_course_num(entry),
                                    'typically_offered' : check_typically_offered(entry),
                                    'prerequisites'     : get_prereqs(get_long_descr(entry)),
                                    'delivery_type'     : pop_delivery_type(entry)
                                    }

        courses = [pack_course(entry) for entry in entries if is_csc(entry)]
        [print(course) for course in courses if course['typically offered'][0] != 'Not Offered']
        return courses

if __name__ == "__main__":
    parser = parser()

# dealing with campusconnect login (?)

# finding the right html targets to get what we want

    # lay out the requirements
        # MS IN CS:
            # INTRODUCTORY COURSES (can be waived)
            # FOUNDATION COURSES
            # ELECTIVES:
            # AREA COURSES
                # 4 COURSES FROM ONE AREA:
                # 4 COURSES FROM ANY AREA:
                        # (INCLUDING:)
                            # 2 COURSE SE STUDIO SEQ.
                            # 2 COURSE GAM STUDIO SEQ.
                            # 1 COURSE CAPSTONE
                            # 2 COURSE GAM STUDIO SEQ.
                            # MS THESIS (HOW MANY CREDITS?)
                            # MS RESEARCH PROJECT
                    #

        # MS IN IS:
            # INTRODUCTORY COURSES (can be waived)
            # FOUNDATION COURSES
            # ELECTIVES:
            # AREA COURSES


# term they enter

# course data:
    # prerequisites = separate object 
    # course Number = 
    # internal course id
    # quarters offered = list()
    # delivery type = list()


# pathToGraduation:
    # INPUTS:
        # start quarter
        # classes per quarter
    # waivedCourses
    # numClassesPerQuarter
    # startQuarter
    # currPath                     ( starting courses + taken courses )
    # thisQuarter                  ( this quarter's courses )
    # remaining requirements       ( all - waivedCourses )


