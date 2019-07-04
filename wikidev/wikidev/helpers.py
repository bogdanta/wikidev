import re
import requests

from bs4 import BeautifulSoup
from difflib import SequenceMatcher

from .disambiguation import DISAMBIGUATION_NAMES


class WikiMixin(object):

    @staticmethod
    def _trim(url):
        """ Eliminates the trailing "(disambiguation)"
        from the titles & URLs of wiki pages
        """
        return url.replace(u'(disambiguation)', '')

    def _build_url(self, params):
        scheme = u'https://'
        netloc = u'en.wikipedia.org'
        path = u'/w/api.php'
        url = u'{scheme}{netloc}{path}?{params}'.format(
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=u'&'.join([u'%s=%s' % item for item in params.items()])
        )
        return url

    def build_url(self, title):
        params = {
            'action': 'query',
            'format': 'json',
            'prop': 'extracts',
            'titles': title,
            'explaintext': '',
            'redirects': 'yes',
        }
        return self._build_url(params)

    def build_random_url(self):
        params = {
            'action': 'query',
            'format': 'json',
            'generator': 'random',
            'prop': 'extracts',
            'grnnamespace': 0,
            'grnlimit': 1,
            'explaintext': 1,
        }
        return self._build_url(params)

    def build_disambiguation_url(self, title):
        params = {
            'action': 'parse',
            'format': 'json',
            'page': title,
            'redirects': 'yes',
        }
        return self._build_url(params)

    def get_page_props(self, page_title):
        return requests.get(
            self.build_disambiguation_url(page_title)
        ).json().get('parse')

    def get_page_data(self, page_title):
        wiki_page_content = requests.get(
            self.build_url(page_title)
        ).json().get('query')
        try:
            page_id = [*[*wiki_page_content.values()][1].keys()][0]
        except IndexError:
            page_id = [*[*wiki_page_content.values()][0].keys()][0]
        except AttributeError:
            page_id = [*[*wiki_page_content.values()][2].keys()][0]

        wiki_page_title = wiki_page_content['pages'][page_id].get('title', 'UPS')
        return wiki_page_title, wiki_page_content

    def get_page_type(self, language, content, props):
        wiki_language = language
        wiki_page_content = content
        wiki_page_properties = props

        if not wiki_page_properties:
            return None
        if not wiki_page_properties['properties']:
            wiki_aux_header = wiki_page_content.values()[0][0].values()[1]
            if 'disambiguation' in wiki_aux_header:
                return "disambiguation_page"
            else:
                for item in DISAMBIGUATION_NAMES:
                    if item['locale'] == wiki_language:
                        local_disambiguation_name = item['string']
                        if local_disambiguation_name in wiki_aux_header:
                            return "disambiguation_page"
                        return "standard_page"

        properties_length = len(wiki_page_properties['properties'])
        if properties_length == 1 and wiki_page_properties.get('properties')[0]['name'] == "wikibase_item":
            return "standard_page"
        elif properties_length > 1:
            prop_name = wiki_page_properties.get('properties')[-2]['name']
            if prop_name == "disambiguation":
                return "disambiguation_page"
            if prop_name == "notoc":
                return "year_page"
            if prop_name == "noeditsection":
                return "main_page"
            # in case a new wiki page type appears, it will be first handled as a standard page
            return "standard_page"

    def page_type(self, keyword, only_page_type=False):                         
        keyword = keyword.replace(' ', '_').replace('#', '')                    
        title, content = self.get_page_data(keyword)                            
        props = self.get_page_props(keyword)                                    
        # TODO - language will by dynamically obtained from user's wiki profile
        page_type = self.get_page_type('en', content, props)                          
        if only_page_type:                                                      
            return page_type                                                    
        return title, content, props, only_page_type
