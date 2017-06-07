'''
TEAM-4
@Copyright: John Pridmore 2017

Scraper Factory
    Scrapes data for when-if path
    Formats data for when-if path
'''

import webbrowser
from contextlib import closing
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import time
import json
import csv
from urllib.parse import urljoin, urlencode, quote_plus


# DEPENDENCIES:
# bs4 (beautiful soup)
# lxml (xml parser that beautiful soup needs)

SUBJECT_LIST = [
    'CSC',
    'IT',
    'IS',
    'GAM',
    'SE',
    'CNS',
    'HCI',
    'TDC',
    'GEO',
    'ECT',
    'GPH',
    'IPD'
]
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
        self.entries, self.page, self.soup = self.init_catalog_scraper()
        # print(self.entries)
        self.results = scraper.separate_course_info(self.entries)
        self.reqs = self.scrape_reqs()

    def init_catalog_scraper(self):
        '''
        content: all xml tags of type content
        page:    raw xml of page
        soup:    parsed soup result of page var
        :return content, page, soup:
        '''
        # COURSE_CATALOG = "http://www.cdm.depaul.edu/academics/Pages/CourseCatalog.aspx"
        COURSE_CATALOG = "http://odata.cdm.depaul.edu/Cdm.svc/Courses?$filter=IsCdmGeneral"

        # storage for xml page to enable consistency on return
        tmpPage = None
        outContent = None
        # open the web page
        with closing(urlopen(COURSE_CATALOG)) as page:
            xml = page.read()
            soup = BeautifulSoup(xml, features="xml")
            # TODO: remove [ used to locate
            print("    =============================================")
            print("    ||      >>> COURSE SCRAPER CREATED <<<     || ")
            print("    =============================================")
            # XML structure:
            # <entry>
            #  ||> <links pertaining to course>
            #  ||> <content>
            #        ||> course information
            #      </content>
            # </entry>
            # entry   = course
            # content = course information inside of entry

            # separates XML by entry
            ents = soup.findAll('entry')
            # removes everything outside of content tag inside of entries
            content = [s.find('content') for s in ents]
            tmpPage = page
            outContent = content
        return outContent, tmpPage, soup

    @staticmethod
    def scrape_reqs():
        '''
        scrapes requirements from respective major pages
        stores and directs scraper through generating major dictionaries and lists
        :return:
        '''

        # initialize variables for scraping reqs
        # # 1: IS_bus_an
        # "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Business-Systems-Analysis.aspx",
        # # 2: IS_bus_int
        # "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Business-Intelligence.aspx",
        # # 3: IS_db_admin
        # "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Database-Administration.aspx",
        # # 4: IS_IT_ent_mgr
        # "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-IT-Enterprise-Management.aspx",
        # # 5: IS
        # "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-IS-Standard.aspx"
        ALL = [
            # 0: CS_req_link
            "http://www.cdm.depaul.edu/academics/Pages/Current/Requirements-MS-in-Computer-Science.aspx",
        ]
        AREA_LIST = []
        # forward declaration of get_req_phases
        def _get_req_phases(page):
            '''
            get_req_phases
            private method
            gets and formats
            :param page: page -
            :return result, has areas:
            '''
            # lambda helper fxn forward declaration
            # retrieves html-div elements with requirement phases in the
            get_req_div  = [i.contents[0] for i in page.findAll('div',  {'class' : 'reqPhaseTitle'})]
            # retrieves html-span elements with requirement phases in them
            get_req_span = [i.contents[0] for i in page.findAll('span', {'class': 'reqPhaseTitle'})]
            # retrieves all list elements with areas of study in them
            get_area     = [[area.contents[0].strip() for area in i.findAll('li')] for i in page.findAll('ul', {'class' : 'collapsedCourseList'})]
            # bool flag for areas
            has_areas    = False



            result = get_req_span
            if (get_area != []):
                has_areas = True

            # TODO: remove
            # [result.append(div) for div in get_req_div]
            # print(get_req_div)

            # if the page in question has collapsed course lists, the major has areas of study/concentration
            if(has_areas):
                for i in range(0,len(get_req_div)):
                    print(get_req_div[i])
                    if get_req_div[i] == 'Major Elective Courses' or get_req_div[i] == 'Research and Thesis Options':
                        # print(get_req_div[i])
                        result.append({'phase': get_req_div[i], 'areas': get_area.pop(0)})
                        if i + 1 < len(get_req_div):
                            i+=1
                    elif get_req_div[i] not in result:
                        result.append(get_req_div[i])

            # print stats
            print("=============================================")
            print(" >>> REQ PHASES AND AREAS GENERATED <<<")
            [print(r) for r in result]
            print("=============================================")
            print("TYPE OF REQ PHASES: " + str(type(result[0])))
            return result, has_areas
        # END GET_REQ_PHASES


        # link/course lambda getters
        get_link = lambda course: course.find('a')
        get_course = lambda course: course.contents  # .contents[0]
        # packing and formatting lists
        # pack_course    = lambda course, name: {'name': name, 'reqPhases': list_to_dict(course)}
        course_to_list = lambda course: [element.contents[0] for element in course]
        # list_to_dict   = lambda list:         {'req_phase': , 'courses': list[1::]}
        pack_req = lambda course: [get_course(course), get_link(course)]
        # print(" get area" + str(get_area))
        # [print("area : " + str(a)) for a in get_area]

        # RESUME SCRAPE_REQS:
        # begin to scrape req links in ALL
        for link in ALL:
            with closing(urlopen(link)) as req_page:
                html = req_page.read()
                soup = BeautifulSoup(html, "html.parser")
                print("=============================================")
                print("   >>> REQ SCRAPER SUCCESSFULLY CREATED <<<    ")
                print("=============================================")

                req_phases, has_area = _get_req_phases(soup)

                print("req phases: " + str(req_phases))
                # pack the phase titles for each major

                # TODO: REMOVE TEST OF TAG PARENT
                # print("testing tag parent: " + str(soup.find('table',{"class": "courseList"}).parent.parent.parent))

                course_lists = [course.findAll('td', {'class': 'CDMExtendedCourseInfo'}) for course in soup.findAll('table',{"class": "courseList"})]
                clean_courses = [course_to_list(idx) for idx in course_lists if idx != []]

                # TODO: REMOVE PRINT CHECKS
                [print(course) for course in clean_courses]
                print("len of course_lists:" + str(len(clean_courses)))

                pack_nested_reqs = lambda phase, course_list: {'phase': phase, 'courses': course_list}

                # adding phase and area information to list of required courses
                # TODO: fix index ==> now does not need to be adjusted to make it 0 indexed
                # adjust index i to be 0-indexed
                reqs_and_courses = {'phase': None}
                print("RIGHT HIAH")
                print(clean_courses)
                return clean_courses
                # for i, c in enumerate(clean_courses):
                #     print(len(req_phases))
                #     print(len(clean_courses))
                #     # TODO: remove verification print
                #     if i < len(req_phases) - 1:
                #         reqs_and_courses = {'phase': req_phases[i]}
                #         # print("checking req_phases: " + str(req_phases[i]))
                #         # print("len of reqphases:" + str(len(req_phases)))
                #         # print(i)
                #         # print("clean courses[{}]:".format(i) + str(clean_courses[i]))
                #         # print(type(req_phases[i]))
                #         # print(req_phases[i-1])
                #
                #         # req_phases[i] is a dict and not Research/Thesis options (only 1 choice per sublist)
                #         if isinstance(req_phases[i], dict) and req_phases[i].get('phase') != 'Research and Thesis Options':
                #             # there are nested course lists
                #             # create dictionary for the name of the phase and course
                #             # replace element in list that has matching req_phase
                #             # print("is dict: " + str(req_phases[i]))
                #             # z = i
                #             for z, phase in enumerate(req_phases[i].get('areas')):
                #                 z += i
                #                 print("z: " +str(z))
                #                 print(phase)
                #                 print(clean_courses[z])
                #                 packed = pack_nested_reqs(phase, clean_courses[z])
                #                 # clean_courses.pop(z)
                #                 reqs_and_courses.update({packed})
                #                 [print(p, v) for p, v in packed.items()]
                #
                #             i = z
                #             # TODO: remove prints
                #             print("END OF NESTED LIST")
                #             print(packed)
                #             print(reqs_and_courses)  # TODO: REMOVE REQS_AND_COURSES PRINT CHECK
                #             print()
                #         else:  # req_phases[i] is NOT a list/dict
                #             # create dict, add reqphase; update the reqs and courses list
                #             options = ['CSC 500', 'CSC 695', 'CSC 698', 'CSC 697']
                #
                #             research_thesis = {
                #                 'phase' : 'Research and Thesis Options',
                #                 'areas' : [
                #                     {
                #                         'phase'   : 'Research Colloquium',
                #                         'courses' : [options[0]]
                #                     },
                #                     {
                #                         'phase'   : 'Master\'s Research',
                #                         'courses' : [options[1]]
                #                     },
                #                     {
                #                         'phase'   : 'Master\'s Thesis',
                #                         'courses' : [options[2]]
                #                     },
                #                     {
                #                         'phase'   : 'Graduate Internship',
                #                         'courses' : [options[3]]
                #                     }
                #                 ]
                #             }
                #             reqs_and_courses.update({'courses': list(c)})
                #             reqs_and_courses.update(research_thesis)
                #             print(reqs_and_courses)

# adding research options
#                     else:
#                         # if outside of the bounds of req_phases
#


#                         print("before" + str(reqs_and_courses))
#                         print("last in req_phases:" + str(req_phases[-1]))
#                         reqs_and_courses.update(research_thesis)
#                         # print(research_thesis.get('areas'))
#                         nested_p = req_phases[-1]
#                         print("after" + str(reqs_and_courses))
#
#                         # nested_l = []
#                         # for j in range(0, len(req_phases.get('areas'))):
#                         #     opt = req_phases[i].get('areas')[j]
#                         #     # print(j)
#                         #     # print(opt)
#                         #     # print(req_phases[i].get('areas'))
#                         #     # print(len(req_phases[i].get('areas')))
#                         #     # print(req_phases[i].get('phase'))
#                         #     # pack research phase with course in option
#                         #     packed = {'phase': opt, 'courses': [options[j]]}
#                         #     # check packed
#                         #     print("Packed RTO : " + str(packed))
#                         #     # add packed to courses sublist
#                         #     # nested['area'].update(packed)
#                         #     # print(packed)  # TODO: REMOVE REQS_AND_COURSES PRINT CHECK
#                         #     nested_p.get('areas').append(packed)
#
#
#                         # [print(n, v) for n, v in nested_p.items()]
#                         print("TESTING WITHOUT ELSE BLOCK: " +  str(reqs_and_courses))
#                         # reqs_and_courses.update(nested_p)
#                         # print()
#                         # print()

        # [print(n, v) for n, v in reqs_and_courses.items()]                # TODO: REMOVE REQS_AND_COURSES PRINT CHECK

        # print(AREA_LIST) # TODO: REMOVE AREA_LIST PRINT CHECK
        # majors = [pack_course(area, AREA_NAMES[i]) for i, area in enumerate(AREA_LIST)]
        # for major in majors:
        #     [print(prop, key) for prop, key in major.items()]
        print("before return" + str(reqs_and_courses))
        return reqs_and_courses
        # return self.generate_reqs(AREA_LIST)
                # generate_reqs()

    def generate_reqs(self, courses):
        def gen_course_blocks(course_list):
            pass
            # the course section list
            # req_to_dic = lambda course, name: {'name': name, 'courses': course }
            # majors = [pack_course(area, AREA_NAMES[i]) for area, i in enumerate(courses) if i < len(courses)]
        # update info for

    # fxn: generateBoolTreeArray
    # ex. prereqs string:
    #   1. ["CSC", "301","and","CSC", "373", "and", "CSC". "374"]
    @staticmethod
    def prereq_edge_cases(prereqs):
        '''
        12. "None"
        :param prereqs:
        :return:
        '''
        if not prereqs:
            return str([])

        if len(prereqs) < 12:
            # case 12
            if prereqs == "None":
                return ""
            # could be one course

        else:
            # case 13
            if prereqs[0:6] == 'Consent':
                return ['ITR CON']
            # case 16
            elif prereqs[0:7] == "Research":
                # IND SDY == Independent Study
                return str(['IND SDY'])
            # case 7
            elif prereqs[0:9] == "PhD status":
                # "PhD status or consent of instructor."
                return ["ITR CON"]
            # case 9
            elif prereqs[0:9] == "Instructor":
                return ["ITR CON"]
            # case 11
            elif prereqs[0:9] == "Permission":
                return ["ITR CON"]
            # case 15
            elif prereqs[0:9] == "Successful":
                # DND THS == Defended Thesis
                return ["DND THS"]
            # case 10
            elif prereqs[0:11] == "For specific":
                # "CRS LNK" == Course Link
                return ["CRS LNK"]
        ## string parsing!!!
        return prereqs



    @staticmethod
    def separate_course_info(entries):
        '''
        separate_course_info
        separates the parsed xml into courses, packs them into a data dictionary, and adds them to a list
        :param self:
        :param entries:
        :param page:
        :param parser:
        :return:
        '''
        # print(entries)
        # print(page)
        # print(parser)

        def get_prereqs(entry):
            # print(entry)
            idx = entry.find('PREREQUISITE(S)')
            if idx == -1:
                return []

            to_return = entry[idx + len('PREREQUISITE(S):')::].strip()
            return scraper.prereq_edge_cases(to_return)

        # EO == Every Other
        def check_typically_offered(entry):
            if (get_typically_offered(entry)) == " ":
                return ['Not Offered']
            else:
                # simplifying and formatting course terms into smaller packages
                typ = get_typically_offered(entry).split('/') #.replace(' Terms', '').replace(' Term', '')
                # print(typ)
                if typ[0] == 'Every Term':
                    # expand 'Every Term' into list of
                    return ['Autumn', 'Winter', 'Spring']
                else:
                    # cut ' Terms'&&' Term'&& off of string
                    # replace instances of 'Every Other' with EO
                    return [qtr.replace(' Terms', '').replace(' Term', '').replace('Every Other', 'EO') for qtr in typ]



        def get_credits(entry):
            descr = entry[0:20]
            # TODO: check for actual credits
            if not "credit" in entry:
                return 4.0
            else:
                return 0.0


        ## fxn that determines if a class is IS or CS
        #  global SUBJECT_LIST : list(str) should be
        #  modified based on the courseSubjects that
        #  you want to pull in
        def is_csc(entry):
            if get_subject(entry) in SUBJECT_LIST and len(get_course_num(entry)) == 3 and int(get_course_num(entry)) >= 400:
                return True
            else:
                return False

        '''
        populates delivery_type field for course dictionaries
        LEGEND FOR DELIVERY TYPE:
        IC == in class only
        O  == online only
        B  == inclass and online
        N  == Not Offer
        :param entry:
        :return:
        '''
        def pop_delivery_type(entry):

            if str(both(entry)).upper() == 'TRUE':
                return 1

            if str(in_class_only(entry)).upper() == 'TRUE':
                return 0

            return 0

        # SEPARATE COURSE INFO
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

        # day formatting lambdas
        fmt_day               = lambda entry: entry.find('properties').find('Effdt').contents[0].split('T')[0]
        get_weekday           = lambda entry: time.strptime(fmt_day(entry), "%Y-%M-%d")
        get_day               = lambda entry: str(time.strftime("%a", get_weekday(entry)))

        ## pack_course
        #  Lambda fxn that packs course information into data dictionary
        #  Legend for results of pack_course
        #  'subject'            : str,              e.g. "IS" or "CSC" or "TDC", etc...
        #  'course_number'      : str,              e.g. "400"
        #  'typically_offered'  : List(str)         e.g. ['Autumn', 'Winter']
        #  'prerequisites'      : List(List(str))   e.g. TODO: []
        #  'delivery_type'      : str               e.g.
        #  'day_of_week'        : str               e.g. "Thu", "Mon"


        # 'prereq'            : scraper.get_prereqs(get_long_descr(entry)),

        pack_course = lambda entry: {
            'subject'           : str(get_subject(entry)),
            'course_number'     : int(get_course_num(entry)),
            'typically_offered' : str(check_typically_offered(entry)),
            'prereq'            : str(get_prereqs(get_long_descr(entry))),

            'delivery_method'   : str(pop_delivery_type(entry)),
            'day_of_week'       : get_day(entry),
            'credits'           : get_credits(get_long_descr(entry)),
            'descr'             : str(get_long_descr(entry))
        }

        courses = [pack_course(entry) for entry in entries if is_csc(entry)]
        # TODO: REMOVE VERIFICATION PRINTS
        [print(course) for course in courses]
        print(len(courses))

        return courses


if __name__ == "__main__":
    tests = [
        "CSC 301 and CSC 373 and CSC 374",
        "CSC 301 or CSC 383 or CSC 393",
        "CSC 301 or CSC 383 and CSC 374",
        "(CSC 301 or CSC 383 or CSC 393) and CSC 373",
        "(IT 240 or CSC 355)  and (CSC 212 or CSC 242 or CSC 243 or CSC 262 or CSC 224 or CSC 300 or CSC 309)"
    ]
    # tree = [scraper.generate_bool_tree_array(test) for test in tests]
    # tree = scraper.generate_bool_tree_array("CSC 301 and CSC 373")
    # [print(t) for t in tree]
    s = scraper()
    print(s.reqs)
    # [print(r) for r in s.results]

