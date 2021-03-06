import lxml.etree as etree

from scrapy.linkextractors.lxmlhtml import LxmlParserLinkExtractor, FilteringLinkExtractor
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url


class ParsedContent(object):
    def __init__(self):
        self.meta_keywords = None
        self.meta_description = None
        self.title = None
        self.headers = []
        self.paragraphs = []
        self.base_url = None
        self.links = []

    def __dict__(self):
        def _dict_link(l):
            return {'url': l.url, 'text': l.text, 'fragment': l.fragment, 'nofollow': l.nofollow}

        return {
            'meta_keywords': self.meta_keywords,
            'meta_description': self.meta_description,
            'title': self.title,
            'headers': self.headers,
            'paragraphs': self.paragraphs,
            'base_url': self.base_url,
            'links': [_dict_link(link) for link in self.links]
        }


class ContentProcessor(object):
    def __init__(self):
        lx = LxmlParserLinkExtractor()
        self.linkextractor = FilteringLinkExtractor(lx, allow=(), deny=(), allow_domains=(),
                                                    deny_domains=(), restrict_xpaths=(), canonicalize=True,
                                                    deny_extensions=None, restrict_css=None)

    def process_response(self, response):
        html = Selector(response)
        pc = self._extract_text(html)
        pc.base_url = get_base_url(response)
        pc.links = self.linkextractor._extract_links(html, response.url, response.encoding, pc.base_url)
        pc.links = self.linkextractor._process_links(pc.links)
        return pc

    def _extract_text(self, selector):
        def _meta_name(el, values):
            return el.tag == 'meta' and 'name' in el.attrib and 'content' in el.attrib and \
                   el.attrib['name'].lower() in values

        pc = ParsedContent()
        for el in selector._root.iter(etree.Element):
            if _meta_name(el, ['description', 'og:description']):
                pc.meta_description = el.attrib['content']
                continue

            if _meta_name(el, ['keywords']):
                pc.meta_keywords = el.attrib['content']
                continue

            if el.tag == 'title':
                pc.title = el.text
                continue

            if el.tag.startswith('h') and len(el.tag) == 2 and el.text and el.text.strip():
                pc.headers.append(el.text)
                continue

            if el.tag in ('script', 'style',):
                continue

            if el.text and el.text.strip():
                pc.paragraphs.append(el.text)
        return pc
