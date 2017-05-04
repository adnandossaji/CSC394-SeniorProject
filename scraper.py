# scraper prototype
import webbrowser
from contextlib import closing
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import deque
import time
import json
import csv
from urllib.parse import urljoin, urlencode, quote_plus


# DEPENDENCIES:
# bs4 (beautiful soup)
# lxml (xml parser that beautiful soup needs)

SUBJECT_LIST = ['CSC', 'IT', 'IS', 'GAM', 'SE', 'CNS', 'HCI', 'TDC', 'GEO', 'ECT', 'GPH', 'IPD']
AREA_NAMES = [
            'CS',
            'IS_bus_an',
            'IS_bus_int',
            'IS_db_admin',
            'IS_IT_ent_mgr',
            'IS'
             ]

class scraper(object):
    ## constructor
    def __init__(self):
        # self.entries, self.page, self.soup = self.init_scraper()
        # self.results = self.separate_course_info(self.entries, self.page, self.soup)
        self.reqs = self.scrape_reqs()

    ## initializes parser and returns soupified xml of given page
    def init_scraper(self):
        # COURSE_CATALOG = "http://www.cdm.depaul.edu/academics/Pages/CourseCatalog.aspx"
        COURSE_CATALOG = "http://odata.cdm.depaul.edu/Cdm.svc/Courses?$filter=IsCdmGeneral"

        with closing(urlopen(COURSE_CATALOG)) as page:
            xml = page.read()
            soup = BeautifulSoup(xml, features="xml")
            print("=============================================")
            print(" >>> COURSE SCRAPER SUCCESSFULLY CREATED <<<  ")
            print("=============================================")
            # separates XML by entry
            entries = soup.findAll('entry')
            # removes everything outside of content tag
            content = [s.find('content') for s in entries]
        return content, page, soup

    def scrape_reqs(self):
        # CS LINK
        AREA_LIST = []

        CS_req_link   = "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-in-Computer-Science.aspx"

        # IS LINKS
        IS_bus_int    = "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Business-Intelligence.aspx"
        IS_bus_an     = "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Business-Systems-Analysis.aspx"
        IS_db_admin   = "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Database-Administration.aspx"
        IS_IT_ent_mgr = "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-IT-Enterprise-Management.aspx"
        IS            = "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Standard.aspx"

        ALL = [CS_req_link, IS_bus_an, IS_bus_int, IS_db_admin, IS_IT_ent_mgr, IS]

        def _get_req_phases(page):
            get_req_div  = [i.contents[0] for i in page.findAll('div',  {'class' : 'reqPhaseTitle'})]
            get_req_span = [i.contents[0] for i in page.findAll('span', {'class': 'reqPhaseTitle'})]
            get_area     = [[area.contents[0].strip() for area in i.findAll('li')] for i in page.findAll('ul', {'class' : 'collapsedCourseList'})]

            has_areas    = False

            # print(" get area" + str(get_area))
            # [print("area : " + str(a)) for a in get_area]

            result = get_req_span
            if (get_area != []):
                has_areas = True
            # [result.append(div) for div in get_req_div]
            # print(get_req_div)
            for i in range(0,len(get_req_div)):
                print(get_req_div[i])
                if get_req_div[i] == 'Major Elective Courses' or get_req_div[i] == 'Research and Thesis Options':
                    # print(get_req_div[i])
                    result.append({'phase': get_req_div[i], 'areas': get_area.pop(0)})
                    if i + 1 < len(get_req_div):
                        i+=1
                if get_req_div[i] not in result:
                    result.append(get_req_div[i])
                # get_req_div.pop()


            print("=============================================")
            print(" >>> REQ PHASES AND AREAS GENERATED <<<")
            [print(r) for r in result]
            print("=============================================")
            return result, has_areas

        #  link/course lambda helpers
        get_link       = lambda course:       course.find('a')
        get_course     = lambda course:       course.contents#.contents[0]

        # getting the correct req_path
        # pack_course    = lambda course, name: {'name': name, 'reqPhases': list_to_dict(course)}
        course_to_list = lambda course:       [element.contents[0] for element in course]

        # list_to_dict   = lambda list:         {'req_phase': , 'courses': list[1::]}
        pack_req       = lambda course:       [get_course(course), get_link(course)]

        for link in ALL:
            with closing(urlopen(link)) as req_page:
                html = req_page.read()
                soup = BeautifulSoup(html, "html.parser")
                print("=============================================")
                print(" >>> REQ SCRAPER SUCCESSFULLY CREATED <<<    ")
                print("=============================================")

                req_phases, has_area = _get_req_phases(soup)

                print("req phases: " + str(req_phases))
                # pack the phase titles for each major

                # print("testing tag parent: " + str(soup.find('table',{"class": "courseList"}).parent.parent.parent))
                course_lists = [course.findAll('td', {'class': 'CDMExtendedCourseInfo'}) for course in soup.findAll('table',{"class": "courseList"})]
                clean_courses = [course_to_list(idx) for idx in course_lists if idx != []]
                print("courses: " + str(clean_courses))
                print("len of course_lists:" + str(len(clean_courses)))

                for i, c in enumerate(clean_courses):
                    # create dict, add reqphase
                    print(req_phases[i])
                    if isinstance(req_phases[i], list):
                        # req_phases[i] could be either Major Course Electives
                        # or
                        print(" electives: " + str(c))
                    else:
                        reqs_and_courses = {'phase' : req_phases[i]}
                        print(reqs_and_courses)
                        reqs_and_courses.update({'courses' : c})
                        print(reqs_and_courses)
                    # for z in c:    # dict.update(c)
                    #     print(z)
                    #     # AREA_LIST.append()

                print(clean_courses)
                # print("area list: " + str(AREA_LIST))
                # print("area list len: " + str(len(AREA_LIST)))

        print(AREA_LIST)
        majors = [pack_course(area, AREA_NAMES[i]) for i, area in enumerate(AREA_LIST)]
        for major in majors:
            [print(prop, key) for prop, key in major.items()]

        # return self.generate_reqs(AREA_LIST)
                # generate_reqs()

    def generate_reqs(self, courses):
        def gen_course_blocks(course_list):
            pass
            # the course section list
            # req_to_dic = lambda course, name: {'name': name, 'courses': course }
            # majors = [pack_course(area, AREA_NAMES[i]) for area, i in enumerate(courses) if i < len(courses)]
        # update info for


    ## separates the parsed xml into courses, packs them into a data dictionary,
    #  and adds them to a list
    @staticmethod
    def separate_course_info(self, entries, page, parser):
        # print(entries)
        # print(page)
        # print(parser)

        ## prerequisite list generator
        def generate_prereq_list(prereq_info):
            stack = deque()
            print(prereq_info)
            first_split = prereq_info.split(')')
            if(len(first_split) >= 1): tmp = [parens.split('(') for parens in first_split]
            # parens = []
            print(tmp)

        # EO == Every Other
        def check_typically_offered(entry):
            if (get_typically_offered(entry)) == " ":
                return ['Not Offered']
            else:
                typ = get_typically_offered(entry).split('/') #.replace(' Terms', '').replace(' Term', '')
                # print(typ)
                if typ[0] == 'Every Term':      return ['Autumn', 'Winter', 'Spring']
                else:                           return [qtr.replace(' Terms', '').replace(' Term', '').replace('Every Other', 'EO') for qtr in typ]

        # strips and formats prerequisites from the parsed XML
        # preps entry data for creating prereq list
        def get_prereqs(entry):
            # print(entry)
            idx = entry.find('PREREQUISITE(S)')
            if idx == -1:
                return 'None'
            tmp = len('PREREQUISITE(S):')

            to_return = entry[idx + tmp::].strip()
            if to_return.find('For specific prerequisites') != -1:
                # TODO: scrape that website and return it?
                return  ['VISIT COURSE WEBSITE']

            close_parens = to_return.find(')')
            open_parens  = to_return.find('(')

            if close_parens >= 1 and open_parens >= 1:
                print("there should be ) or (: " + to_return)
                #return generate_prereq_list(to_return)

            print("there were no parens in this prereq list")
            return to_return


        ## fxn that determines if a class is IS or CS
        #  global SUBJECT_LIST : list(str) should be
        #  modified based on the courseSubjects that
        #  you want to pull in
        def is_csc(entry):
            if get_subject(entry) in SUBJECT_LIST and len(get_course_num(entry)) == 3 and int(get_course_num(entry)) >= 400:
                return True
            else:
                return False

        # 'LEGEND' FOR DELIVERY TYPE:
        #   IC == in class only
        #   O  == online only
        #   B  == inclass and online
        #   N  == Not Offered
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

        #
        fmt_day               = lambda entry: entry.find('properties').find('Effdt').contents[0].split('T')[0]
        get_weekday           = lambda entry: time.strptime(fmt_day(entry), "%Y-%M-%d")
        get_day               = lambda entry: time.strftime("%a", get_weekday(entry)) #

        ## Lambda fxn that packs course information into data dictionary
        #  Legend for results of pack_course
        #  'subject'            : str,              e.g. "IS" or "CSC" or "TDC", etc...
        #  'course_number'      : str,              e.g. "400"
        #  'typically_offered'  : List(str)         e.g. ['Autumn', 'Winter']
        #  'prerequisites'      : List(List(str))   e.g. TODO: []
        #  'delivery_type'      : str               e.g.
        #  'day_of_week'        : str               e.g. "Thu", "Mon"
        pack_course = lambda entry: {
                                    'subject'           : get_subject(entry),
                                    'course_number'     : get_course_num(entry),
                                    'typically_offered' : check_typically_offered(entry),
                                    'prerequisites'     : get_prereqs(get_long_descr(entry)),
                                    'delivery_type'     : pop_delivery_type(entry),
                                    'day_of_week'       : str(get_day(entry))
                                    }

        courses = [pack_course(entry) for entry in entries if is_csc(entry)]

        [print(course) for course in courses if course['typically_offered'][0] != 'Not Offered']

        print(len(courses))
        return courses

if __name__ == "__main__":
    scraper = scraper()

# dealing with campusconnect login (?)

# finding the right html targets to get what we want

    # lay out the requirements


    #REQUIREMENT LIST BY MAJOR:
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


        #Concentration in IS:
            # MS IN : (std)
            # MS IN IS: (std)
            # MS IN IS: (std
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


