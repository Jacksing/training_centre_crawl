from urlparse import urljoin
import os

from bs4 import BeautifulSoup

from consts import *
from utils import *


site_url = 'http://directory.stclassifieds.sg/'
category_url = 'http://directory.stclassifieds.sg/singapore-directory/tuition+centres/c/offset/{offset}/page/n'

available_detail = (
    ('add', ADD),
    ('website', WEBSITE),
    ('email', EMAIL),
    ('tel', TEL),
)


cache_folder = 'cache'


def _log(msg):
    log(msg)


def get_details(soup, key='sr-details'):
    details_dict = {}
    details = get_tag_by_class(soup, key)
    details = get_all_tags(details, None, 'li')
    if not details:
        return details_dict
    for li in details:
        all_p = get_all_tags(li, None, 'p')
        if not all_p.__len__() == 3:
            _log('detail item is not in pattern <name : value> %s' % li.text.strip())
        else:
            for t in available_detail:
                if inline_string(all_p[0].text).lower() == t[0]:
                    details_dict.update({t[1]: inline_string(all_p[2].text)})
                    break
    return details_dict


def get_section_information(section):
    title_with_logo = get_tag_by_class(section, 'sr-title-with-logo')
    if title_with_logo:
        name = get_tag_text(title_with_logo, 'strong')
        #
        url = get_tag(title_with_logo, None, 'a')
        url = get_tag_attrib(url, 'href')
        #
        img = get_tag_by_class(section, 'sr-img', 'span')
        img = get_tag(img, None, 'img')
        img = get_tag_attrib(img, 'src')
    else:
        title = get_tag_by_class(section, 'sr-title')
        name = get_tag_text(title, 'h2')
        #
        url = get_tag(title, None, 'a')
        url = get_tag_attrib(url, 'href')
        #
        img = None

    details_dict = {NAME: name, URL: urljoin(site_url, url), IMG: img}
    if name == 'A & A EDUCATION CENTRE':
        print(name)

    details_dict.update(get_details(section))

    return details_dict


def get_course_page_information(course_soup):
    info = {}
    profile = get_tag(course_soup, {'id': 'profileTitleScroll'})
    if not profile:
        profile = get_tag(course_soup, {'id': 'profileTitle'})
    if profile:
        info[PROFILE] = profile.text.strip()
    else:
        info[PROFILE] = None

    info.update(get_details(course_soup, 'srd-details'))

    return info


def begin():
    all_courses_info = []
    for i in range(0, 8):
        try:
            cache_file = os.path.join(cache_folder, 'category_offset_%s' % (i * 20).__str__())
            soup = load_page(category_url.format(**{'offset': (i * 20).__str__()}), cache_file)
            soup = BeautifulSoup(soup)
            course_sections = get_all_tags_by_class(soup, 'sr-results')

            for section in course_sections:
                info = get_section_information(section)

                cache_file = os.path.join(cache_folder, info[NAME].lower())
                cache_file = load_page(info[URL], cache_file)
                course_soup = BeautifulSoup(cache_file)
                info.update(get_course_page_information(course_soup))

                all_courses_info.append(info)

                keys = info.keys()
                keys.sort()
                for key in keys:
                    print('%s\t%s' % (key, info[key]))
                print('=======================================')

        except Exception as ex:
            print("[ERR:%s]" % ex.message)

    print('OK!')


begin()