import onem
import datetime
import jwt
import requests

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import View as _View
from django.shortcuts import get_object_or_404

from .helpers import WikiMixin


class View(_View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *a, **kw):
        return super(View, self).dispatch(*a, **kw)

    def get_user(self):
        token = self.request.headers.get('Authorization')
        if token is None:
            raise PermissionDenied

        data = jwt.decode(token.replace('Bearer ', ''), key='87654321')
        user, created = User.objects.get_or_create(id=data['sub'],
                                                   username=str(data['sub']))
       # user, created = User.objects.get_or_create(id=231243,
       #                                            username='Mircea')
        return user

    def to_response(self, menu_or_form):
        response = onem.Response(menu_or_form, self.request.GET['corr_id'])
        return HttpResponse(response.as_json(), content_type='application/json')


class HomeView(View):
    http_method_names = ['get']

    def get(self, request):
        #user = self.get_user()

        body = [
            onem.menus.MenuItem('Search', url=reverse('search_wizard')),
            onem.menus.MenuItem('Random', url=reverse('random')),
            onem.menus.MenuItem('Language', url=reverse('language'))
        ]

        return self.to_response(onem.menus.Menu(body, header='menu'))


class SearchWizardView(View, WikiMixin):
    http_method_names = ['get', 'post']

    def get(self, request):
        body = [
            onem.forms.FormItem(
                'keyword', onem.forms.FormItemType.STRING, 'Send keyword',
                header='search', footer='Send keyword'
            )
        ]
        return self.to_response(
                onem.forms.Form(body, reverse('search_wizard'), method='POST',
                meta=onem.forms.FormMeta(confirm=False)
        ))

    def post(self, request):
        keyword = request.POST['keyword'].replace(' ', '_').replace('#', '')
        title, content, props, page_type = self.page_type(keyword)
        url = self.build_url(keyword)
        response = requests.get(url)
        try:
            page_id, page_value = [*response.json()['query']['pages'].items()][0]
            if page_id == '-1':
                raise ValueError
            body = onem.menus.MenuItem(
                page_value.get('extract').split('==')[0].strip(),
                is_option=False
            )
        except ValueError:
            body = onem.menus.MenuItem('Please try again later', is_option=False)

        return self.to_response(onem.menus.Menu(
            [body],
            header='(ENGLISH) {keyword} SEARCH'.format(keyword=keyword.title()),
            footer='Send MENU'
        ))


class RandomView(View, WikiMixin):
    http_method_names = ['get']

    def get(self, request):
        try:
            response = requests.get(self.build_random_url())
            response = response.json()
            article_details = response['query']['pages']
            article_id, article_details = [*article_details.items()][0]
            title = article_details['title']

            body = [
                onem.menus.MenuItem(
                    article_details.get('extract', '').split('==')[0].strip(),
                    is_option=False
                )
            ]
        except:
             body = [onem.menus.MenuItem('Please try again later', is_option=False)]

        return self.to_response(
            onem.menus.Menu(body, header='random', footer='Reply MENU')
        )


class LanguageView(View):
    http_method_names = ['get']

    def get(self, request):
        return self.to_response(
            onem.menus.Menu(
                [
                    onem.menus.MenuItem(
                        'Currently only English is supported. More languages to be added soon.',
                        is_option=False
                    )
                ],
                header='Language',
                footer='Reply MENU'
            )
        )
