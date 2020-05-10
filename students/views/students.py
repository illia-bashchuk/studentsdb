from django.utils.translation import ugettext as _
from datetime import datetime
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Button, Field, HTML
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DeleteView, ListView, UpdateView

from ..models.groups import Group
from ..models.students import Student
from ..util import get_current_group, paginate


class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'students/students_list.html'
    paginate_by = 10
    page_kwarg = 'page'

    def get_queryset(self):
        current_group = get_current_group(self.request)
        qs = super(StudentList, self).get_queryset()
        if current_group:
            return qs.filter(student_group=current_group.id)
        else:
            # otherwise show all students
            return qs.all()


# Views for Students

@login_required
def students_add(request):

    # If the form was completed:
    if request.method == "POST":

        # If the Add button was clicked:
        if request.POST.get('add_button') is not None:
            # We validate the data and collect errors
            errors = {}

            data = {
                'middle_name': request.POST.get('middle_name'),
                'notes': request.POST.get('notes')
            }
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _(u"First Name field is required")
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = _(u"Last name is required")
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _(u"Date of birth is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = _(
                        u"""Enter the correct date format (e.g. 1984-12-30)""")
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required")
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u"Select a group for the student")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = _(u"Select the correct group")
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo
            # If the data were entered correctly:
            if not errors:
                # We create and store a student in the database
                student = Student(**data)
                student.save()

                # We return the user to the student list
                return HttpResponseRedirect(
                    _(u'%s?status_message=Student %s %s successfully added!')
                    % (reverse('home'), student.first_name, student.last_name))

            else:
                # If the data was entered incorrectly:
                # render form with errors and previous user input
                return render(
                    request, 'students/students_add.html', {
                        'groups': Group.objects.all().order_by('title'),
                        'errors': errors
                    })
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                _(u'%s?status_message=Student addition canceled!')
                % reverse('home'))
        else:
            # initial form render
            return render(request, 'students/students_add.html',
                          {'groups': Group.objects.all().order_by('title')})

        # If the form was completed:
        # return the form's initial state code
    return render(request, 'students/students_add.html',
                  {'groups': Group.objects.all().order_by('title')})


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit',
                                          kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-8'
        # add buttons
        self.helper.layout.append(Field(
            HTML('<div class="form-group">'
                 '<div class="controls col-sm-8 text-left ml-4">'),
            Submit('add_button', _(u"Save"),
                   css_class=""),
            Submit('cancel_button', _(u"Cancel"),
                   css_class=""),
            HTML('</div></div>')))


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return _(u'%s?status_message=Student successfully edited!') % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                _(u'%s?status_message=Editing canceled!') % reverse('home')
            )
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return _(u'%s?status_message=Student successfully deleted!') \
            % reverse('home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)
