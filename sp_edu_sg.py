import requests
from bs4 import BeautifulSoup


def read_page(html):
    pass

catalogue_url = \
    'http://www.sp.edu.sg/wps/wcm/connect/lib-pace/internet/?' \
    'srv=cmpnt' \
    '&source=library' \
    '&cmpntname=MC-CourseCatalogue-All%20Courses%28Continuing%20Education-Course%20Catalogue%29' \
    '&CONNECTORCACHE=SESSION'

page_base_url = 'http://www.sp.edu.sg/wps/portal/vp-spws/pace.courses.catalogue.details?WCM_GLOBAL_CONTEXT=%s'

resp = requests.get(catalogue_url)
if resp.status_code == 200:
    try:
        soup = BeautifulSoup(resp.text)
        course_list = soup.findAll('li')
        course_list = [
            page_base_url % li.a['onclick'].__str__().lstrip("javascript:showPage(\\'").rstrip("\\');")
            for li in course_list
        ]
        # print('\n'.join(course_list))
        for c in course_list[0:3]:
            read_page(requests.get(c).text)
    except Exception as ex:
        print(ex.message)