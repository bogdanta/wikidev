import onem
import datetime
import jwt

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import View as _View
from django.shortcuts import get_object_or_404


class View(_View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *a, **kw):
        return super(View, self).dispatch(*a, **kw)

    def get_user(self):
        #token = self.request.headers.get('Authorization')
        #if token is None:
        #    raise PermissionDenied

        #data = jwt.decode(token.replace('Bearer ', ''), key='87654321')
        #user, created = User.objects.get_or_create(id=data['sub'],
        #                                           username=str(data['sub']))
        user, created = User.objects.get_or_create(id=231243,
                                                   username='Mircea')
        return user

    def to_response(self, menu_or_form):
        return HttpResponse(menu_or_form.as_json(),
                            content_type='application/json')


class HomeView(View):
    http_method_names = ['get']

    def get(self, request):
        # TODO - language setting should stay on User model or a WikiProfile model
        user = self.get_user()

        body = [
            onem.menus.MenuItem('Search', url=reverse('search_wizard')),
            #onem.menus.MenuItem('Random', url=reverse('random')),
            #onem.menus.MenuItem('Language)', url=reverse('language'))
        ]

        return self.to_response(onem.menus.Menu(body, header='menu'))


class SearchWizardView(View):
    http_method_names = ['get', 'post']

    def get(self, request):
        body = [
            onem.forms.FormItem(
                'keyword', onem.forms.FormItemType.STRING, 'Send keyword', header='search'
            )
        ]
        return self.to_response(
            onem.forms.Form(body, reverse('search_wizard'), method='POST')
        )

    def post(self, request):
        import ipdb; ipdb.set_trace()
        keyword = request.POST['keyword']
        # hit wiki API with the keyword and return the results in a body
        # reuse code from services/wiki
        body =['WIP WIP WIP']

        return self.to_response(body)
