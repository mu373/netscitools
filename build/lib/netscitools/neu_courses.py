__all__ = ["get_northeastern_course_info", "create_course_prerequisite_network"]


import pandas as pd
from bs4 import BeautifulSoup

def get_northeastern_course_info(dept_html):
    """
    Given a string of raw html (dept_html) that contains a department's course titles and descriptions, this returns a useful data structure that contains the titles, descriptions, and prerequisites.

    Parameters
    ----------
        dept_html: str
            Raw HTML text of a course catalog page for a specific department.
            An example page would be https://catalog.northeastern.edu/course-descriptions/chme/
            ```py
            dept_html = requests.get("https://catalog.northeastern.edu/course-descriptions/CHME/").text
            get_northeastern_course_info(dept_html)
            ```

    Returns
    -------
        courses_info : list
        A list of dictionaries, iterated for all courses in the department.
        [
            {'title': 'CHME 1983.  Special Topics in Chemical Engineering.  (4 Hours)',
                'description': 'The course description goes here.',
                'prerequisite': ['MATH 1234', 'MATH 5678']
            },
            ...
        ]
    """

    def replace_string(s):
        s = s.replace(u'\xa0', ' ')
        return s
        
    soup = BeautifulSoup(dept_html, "html.parser")
    colcontent_div = soup.find('div', id="col-content")
    coursedescs_div = colcontent_div.find('div', class_="sc_sccoursedescs")

    try:
        courseblock_div = coursedescs_div.find_all('div', class_="courseblock")
    except:
        courses_info = {}
        return courses_info
        
    courses_info = []
    for blk in courseblock_div:
        prereqs = []
        course_titles = replace_string(blk.find('p', class_="courseblocktitle").text)

        course_id = course_titles.split(".")[0]
        course_desc = replace_string(blk.find('p', class_="cb_desc").text)

        course_prereq_p_list = blk.find_all('p', class_="courseblockextra")

        # Remove corequisite
        course_prereq_p_list2 = []
        for course_prereq_p in course_prereq_p_list:
            if "Prerequisite" in course_prereq_p.find('strong').text:
                course_prereq_p_list2.append(course_prereq_p)

        for course_prereq_p in course_prereq_p_list2:
            if course_prereq_p:
                course_prereq_links = course_prereq_p.find_all('a')
                for course_prereq_link in course_prereq_links:
                    prereqs.append(replace_string(course_prereq_link.text))
            
        courses_info.append({'id': course_id, 'title': course_titles, 'description': course_desc, 'prerequisite': prereqs})
    
    return courses_info
    # pass

def create_course_prerequisite_network(department_name, courses_info):

    """
    Create a network of course prerequisites. Nodes represent courses, edges represent prerequisites.

    Parameters
    ----------
        department_name: str
            Label for the department, which is usually in capital letters
            e.g. "CHME", "SPNS"
        courses_info: list
            List from get_northeastern_course_info()
            Raw HTML text of a course catalog page for a specific department.

    
    Returns
    -------
        G_prereq : networkx.DiGraph
            Directed network of the course prerequisites.
    """

    df_courses = pd.DataFrame(courses_info)
    
    G_prereq = nx.DiGraph()

    # Return empty graph when there is no course (e.g. ESLG)
    if len(df_courses) == 0:
        return G_prereq


    all_course_ids = set()
    all_course_ids.update(set(df_courses['id']))
    all_course_ids.update(set(itertools.chain.from_iterable(df_courses['prerequisite'])))
    
    for course_id in all_course_ids:
        G_prereq.add_node(course_id,)

    for idx, row in df_courses[['id', 'prerequisite']].iterrows():
        course_id = row['id']
        prereq_course_ids = row['prerequisite']
        for prereq_course_id in prereq_course_ids:
            # If course j requires course i, there will be a directed edge (i,j)
            G_prereq.add_edge(prereq_course_id, course_id)

    # Exception for SPNS courses
    # We could remove all the cycles automatically, but we'll do it manually
    if department_name == "SPNS":
        # Remove "Placement in ...." which results in a cycle
        G_prereq.remove_edge('SPNS 1101','SPNS 1101')
        G_prereq.remove_edge('SPNS 1102','SPNS 1102')
        G_prereq.remove_edge('SPNS 2101','SPNS 2101')
        G_prereq.remove_edge('SPNS 2102','SPNS 2102')
        G_prereq.remove_edge('SPNS 3101','SPNS 3101')
        G_prereq.remove_edge('SPNS 3102','SPNS 3102')
        # SPNS 3603 and SPNS 3602 are cycle in the graph here because this code treats
        # all the classes listed in the prerequisites section as prerequisites,
        # even if they are listed as "OR"
        G_prereq.remove_edge('SPNS 3603','SPNS 3602') 
    
    return G_prereq