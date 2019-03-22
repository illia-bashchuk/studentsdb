# -*- coding: utf-8 -*-
from datetime import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Submit
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.db.models import ProtectedError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView, ListView, UpdateView

from ..models.groups import Group
from ..util import get_current_group, paginate

# Views for Groups


class GroupList(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'students/group.html'
    paginate_by = 3
    page_kwarg = 'page'

    def get_queryset(self):
        current_group = get_current_group(self.request)
        qs = super(GroupList, self).get_queryset()
        # print current_group

        if current_group:
            return qs.filter(pk=current_group.id)
        else:
            # otherwise show all groups
            return qs.all()


def groups_add(request):
    return None


class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal text-center'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-3'

        # add buttons
        # add buttons
        self.helper.layout.append(Field(
            HTML('<div class="form-group">'
                 '<label class="col-sm-2 control-label" ></label >'
                 '<div class="controls col-sm-3 text-center">'),
            Submit('add_button', u"Зберегти",
                   css_class="btn btn-primary"),
            Submit('cancel_button', u"Скасувати",
                   css_class="btn btn-link"),
            HTML('</div></div>')))


class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/group_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Групу успішно відредаговано!' % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування відмінено!' % reverse('groups')
            )
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/group_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Групу успішно видалено!' \
            % reverse('groups')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        error_text = u'''Групу не можливо видалити так як за нею закріплені студенти. 
        Видаліть або переведіть студентів до іншої групи!'''
        try:
            # Get the single item from the filtered queryset
            self.object.delete()
        except ProtectedError:
            return HttpResponseRedirect(u'%s?status_message=%s'
                                        % (reverse('groups_delete', args=[self.object.id]), error_text))
        return HttpResponseRedirect(success_url)
