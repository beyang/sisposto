# -*- coding: utf8 -*-
import re
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import RedirectView
from .models import Pessoa


from django.utils import six

import logging
logger = logging.getLogger(__name__)


URLS_EXCLUIDAS = [
    # casa exatamente com a string
    r'^(%s)$' % '|'.join([reverse('users:update'), reverse('account_logout')]),

    # casa obrigatoriamente com o inicio da string
    r'^(?:%s)' % '|'.join([settings.MEDIA_URL,
                           settings.STATIC_URL]),
]


profile_update_url_re = re.compile(r'%s' % '|'.join(URLS_EXCLUIDAS))

# TODO - checar implementacao
class UsersMiddleware(object):
    def process_request(self, request):
        usuario = request.user
        if usuario:
            if usuario.is_authenticated():
                try:
                    profile = Pessoa.objects.get(user=usuario)
                    if not profile.cadastro_concluido:
                        if not profile_update_url_re.match(request.path):
                            return redirect('users:update')
                except Pessoa.DoesNotExist as e:
                    logger.debug(e.message)
                    if not profile_update_url_re.match(request.path):
                        return redirect('users:update')
            else:
                print('NÃO esta autenticado')
                #request.session['postos_disponiveis'] = "MUITOS POSTOS"

