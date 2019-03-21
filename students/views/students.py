# -*- coding: utf-8 -*-


from datetime import datetime

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Button, Field, HTML
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.forms import ModelForm
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


"""


def students_list(request):
    students = Student.objects.all()
    if request.get_full_path() == "/":
        # redirect request.GET on its copy(deep copy) which I will amend
        request.GET = request.GET.copy()
        # assign 'order_by' value 'last_name'
        request.GET.__setitem__('order_by', 'last_name')
    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results.
        students = paginator.page(paginator.num_pages)
    return render(request, 'students/students_list.htmlstudents/students_list.html',
                  {'students': students})


"""

# Views for Students


def students_add(request):

    # Якщо форма була запощена:
    if request.method == "POST":
        # Якщо кнопка Скасувати була натиснута:

        # Повертаємо користувача до списку студентів

        # Якщо кнопка Додати була натиснута:
        if request.POST.get('add_button') is not None:
            # Перевіряємо дані на коректність та збираємо помилки
            errors = {}

            # Якщо дані були введені некоректно:
            # Віддаємо шаблон форми разом із знайденими помилками
            data = {
                'middle_name': request.POST.get('middle_name'),
                'notes': request.POST.get('notes')
            }
            # validate user input
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім’я є обов’язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов’язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов’язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"""Введіть коректний формат дати
                     (напр. 1984-12-30)"""
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов’язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                data['photo'] = photo
            # Якщо дані були введені коректно:
            if not errors:
                # Створюємо та зберігаємо студента в базу
                """
                    student = Student(
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        middle_name=request.POST['middle_name'],
                        birthday=request.POST['birthday'],
                        ticket=request.POST['ticket'],

                        student_group=Group.objects.get(
                            pk=request.POST['student_group']),
                        photo=request.FILES['photo'],
                    )
                """
                # save it to database
                student = Student(**data)
                student.save()

                # Повертаємо користувача до списку студентів
                return HttpResponseRedirect(
                    u'%s?status_message=Студента %s %s успішно додано!'
                    % (reverse('home'), student.first_name, student.last_name))

            else:
                # render form with errors and previous user input
                return render(
                    request, 'students/students_add.html', {
                        'groups': Group.objects.all().order_by('title'),
                        'errors': errors
                    })
        elif request.POST.get('cancel_button') is not None:
            # redirect to home page on cancel button
            return HttpResponseRedirect(
                u'%s?status_message=Додавання студента скасовано!'
                % reverse('home'))
        else:
            # initial form render
            return render(request, 'students/students_add.html',
                          {'groups': Group.objects.all().order_by('title')})

        # Якщо форма не була запощена:
        # повертаємо код початкового стану форми
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
                 '<label class="col-sm-2 control-label" ></label >'
                 '<div class="controls col-sm-8 text-center">'),
            Submit('add_button', u"Зберегти",
                   css_class="btn btn-primary"),
            Submit('cancel_button', u"Скасувати",
                   css_class="btn btn-link"),
            HTML('</div></div>')))


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Cтудента успішно відредаговано!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування відмінено!' % reverse('home')
            )
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' \
            % reverse('home')
