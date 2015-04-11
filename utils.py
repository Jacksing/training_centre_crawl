import cPickle
import requests
import os

__all__ = [
    'log', 'inline_string', 'load_page', 'get_tag_text',
    'get_tag_attrib', 'get_tag', 'get_all_tags', 'get_tag_by_class',
    'get_all_tags_by_class',
]


def log(msg):
    # print('    -> %s' % msg)
    pass


def inline_string(s):
    return ' '.join(s.strip().split())


def load_page(url, cache_file=None):
    if cache_file is None:
        cache_file = url.replace('/', '%s')
    if os.path.exists(cache_file):
        log('loading local page %s' % url)
        f = file(cache_file)
        page = cPickle.load(f)
        f.close()
    else:
        log('loading web page %s' % url)
        page = requests.get(url).text
        f = file(cache_file, 'w')
        cPickle.dump(page, f)
        f.close()
    return page


def get_tag_text(soup, tag_name):
    if not soup:
        return None
    tag = soup.find(tag_name)
    if not tag:
        log("can't find tag <%s>" % tag_name)
        return ''
    else:
        return tag.text.strip()


def get_tag_attrib(soup, attr_name='div'):
    if not soup:
        return None
    return soup[attr_name]


def get_tag(soup, attrs, tag_name='div'):
    if not soup:
        return None
    tag = soup.findAll(tag_name, attrs)
    if tag.__len__() == 0:
        log("can't find tag <%s> with attrs <%s>" % (tag_name, attrs))
        return None
    elif tag.__len__() > 1:
        log("too many tags <%s> with attrs <%s> are found" % (tag_name, attrs))
        return None
    else:
        return tag[0]


def get_all_tags(soup, attrs, tag_name='div'):
    if not soup:
        return None
    return soup.findAll(tag_name, attrs)


def get_tag_by_class(soup, class_value, tag_name='div'):
    if not soup:
        return None
    return get_tag(soup, {'class': class_value}, tag_name)


def get_all_tags_by_class(soup, class_value, tag_name='div'):
    if not soup:
        return None
    return get_all_tags(soup, {'class': class_value}, tag_name)