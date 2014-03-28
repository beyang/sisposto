# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

# view imports
from django.utils.encoding import force_text
from django.utils.translation import ugettext
from django.views.generic import DetailView, UpdateView
from django.views.generic import RedirectView
from django.views.generic import ListView

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin, FormValidMessageMixin

from extra_views import UpdateWithInlinesView

# Import the form from users/forms.py

from .forms import UserForm

# Import the customized User model
from .models import User
from users.form_inlines import UserProfileInline


class ViewHasNameAndDescriptionMixin(object):
    """
    Mixin allows you to set a human readable name and description for this
    view through a static property on the class or programmatically by
    overloading the get_view_name and get_view_description methods.
    """
    view_name = None  # Default the view_name to none
    view_description = None  # Default the view_description to none

    def get_context_data(self, **kwargs):
        kwargs = super(ViewHasNameAndDescriptionMixin, self).get_context_data(**kwargs)
        # Update the existing context dict with the provided view_name
        # and view_description.
        kwargs.update({"view_name": self.get_view_name(),
                       "view_description": self.get_view_description()})
        return kwargs

    def get_view_name(self):
        if self.view_name is None:  # If no view_name was provided as a view
                                   # attribute and this method wasn't
                                   # overridden raise a configuration error.
            raise ImproperlyConfigured(
                '{0} is missing a view_name variable. '
                'Define {0}.view_name, or override '
                '{0}.get_view_name().'.format(self.__class__.__name__))
        return force_text(self.view_name)

    def get_view_description(self):
        if self.view_description is None:  # If no view_description was provided
                                   # as a view attribute and this method wasn't
                                   # overridden raise a configuration error.
            raise ImproperlyConfigured(
                '{0} is missing a view_description variable. '
                'Define {0}.view_description, or override '
                '{0}.get_view_description().'.format(self.__class__.__name__))
        return force_text(self.view_description)


class UserDetailView(LoginRequiredMixin, ViewHasNameAndDescriptionMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
    view_name = ugettext(u'Usuário - Detalhes')
    view_description = ugettext(u'Informações detalhadas sobre o usuário')


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
            kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, ViewHasNameAndDescriptionMixin, UpdateView):

    form_class = UserForm
    inlines = [UserProfileInline]
    view_name = ugettext(u'Usuário - Editar')
    view_description = ugettext(u'Edita/Atualiza informações sobre o usuário')
    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                    kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)




class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
