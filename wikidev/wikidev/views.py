import onemsdk
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

from onemsdk.schema.v1 import (
    Response, Menu, MenuItem, MenuItemType, Form, FormItemContent,
    FormItemContentType, FormMeta
)


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
        return user

    def to_response(self, content):
        response = Response(content=content)
        response.correlation_id = self.request.headers['X-Onem-Correlation-Id']

        return HttpResponse(response.json(), content_type='application/json')


class HomeView(View):
    http_method_names = ['get']

    def get(self, request):
        #user = self.get_user()  # TODO

        menu_items = [
            MenuItem(type=MenuItemType.option,
                     description='Search',
                     method='GET',
                     path=reverse('search_wizard')),
            MenuItem(type=MenuItemType.option,
                     description='Random',
                     method='GET',
                     path=reverse('random')),
            MenuItem(type=MenuItemType.option,
                     description='Language',
                     method='GET',
                     path=reverse('language'))
        ]

        menu = Menu(body=menu_items)

        return self.to_response(menu)


class SearchWizardView(View, WikiMixin):
    http_method_names = ['get', 'post']

    def get(self, request):
        form_items = [
            FormItemContent(type=FormItemContentType.string,
                     name='keyword',
                     description='Send keyword',
                     header='search',
                     footer='Send keyword')
        ]
        form = Form(body=form_items,
                    method='POST',
                    path=reverse('search_wizard'),
                    meta=FormMeta(confirmation_needed=False,
                                  completion_status_in_header=False,
                                  completion_status_show=False))

        return self.to_response(form)

    def post(self, request):
        keyword = request.POST['keyword'].replace(' ', '_').replace('#', '')
        title, content, props, page_type = self.page_type(keyword)
        url = self.build_url(keyword)
        response = requests.get(url)

        try:
            page_id, page_value = [*response.json()['query']['pages'].items()][0]
            if page_id == '-1':
                raise ValueError
            body = MenuItem(type=MenuItemType.content,
                            description=page_value.get('extract').split('==')[0].strip())
        except ValueError:
            body = MenuItem(type=MenuItemType.content,
                            description='Please try again later')

        menu = Menu(body=[body],
                    header='(ENGLISH) {keyword} SEARCH'.format(keyword=keyword.title()),
                    footer='Send MENU')

        return self.to_response(menu)


class RandomView(View, WikiMixin):
    http_method_names = ['get']

    def get(self, request):
        try:
            response = requests.get(self.build_random_url())
            response = response.json()
            article_details = response['query']['pages']
            article_id, article_details = [*article_details.items()][0]
            title = article_details['title']

            body = MenuItem(type=MenuItemType.content,
                            description=article_details.get('extract', '').split('==')[0].strip())
        except:
            body = MenuItem(type=MenuItemType.content,
                            description='Please try again later')

        menu = Menu(body=[body], header='random',footer='Reply MENU')

        return self.to_response(menu)


class LanguageView(View):
    http_method_names = ['get']

    def get(self, request):
        body = MenuItem(type=MenuItemType.content,
                        description='Currently only English is supported. More languages to be added soon.')

        menu = Menu(body=[body], header='language',footer='Reply MENU')

        return self.to_response(menu)
