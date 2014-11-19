from django.core import serializers
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
import models
import forms


def render_static(request, page):
    return render(request, 'pages/{}.html'.format(page))

{%% for model_name in all_models %%}{%% set model_name = model_name|capitalize %%}
def {{{ model_name|lower }}}(request):
    if request.method == 'POST':
        form = forms.{{{ model_name }}}Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added new {{{ model_name }}}')
    else:
        form = forms.{{{ model_name }}}Form()
    context = {
        'form_mode': 'add',
        'view_url': '{{{ app_name }}}.views.{{{ model_name|lower }}}_detail',
        'model_name': '{{{ model_name }}}',
        'collection': serializers.serialize('python', models.{{{ model_name }}}.objects.all()),
        'form': form
    }
    return render(request, 'layouts/collection.html', context)


def {{{ model_name|lower }}}_detail(request, pk):
    {{{ model_name|lower }}}_instance = get_object_or_404(models.{{{ model_name }}}, pk=pk)
    if request.method == 'POST':
        form = forms.{{{ model_name }}}Form(
            request.POST, request.FILES, instance={{{ model_name|lower }}}_instance)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully edited {{{ model_name }}} details')
            return HttpResponseRedirect(request.path)
    else:
        form = forms.{{{ model_name }}}Form(instance={{{ model_name|lower }}}_instance)
    context = {
        'form_mode': 'edit',
        'model': {{{ model_name|lower }}}_instance,
        'model_name': '{{{ model_name }}}',
        'form': form
    }
    return render(request, 'layouts/model.html', context)


def {{{ model_name|lower }}}_add(request, pk):
    if request.method == 'POST':
        form = forms.{{{ model_name }}}Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully added new {{{ model_name }}}')
    else:
        return HttpResponseRedirect('/')
    messages.add_message(request, messages.SUCCESS, 'Successfully added new {{{ model_name }}}')
    return HttpResponseRedirect('/')


def {{{ model_name|lower }}}_delete(request, pk):
    {{{ model_name|lower }}}_instance = get_object_or_404(models.{{{ model_name }}}, pk=pk)
    {{{ model_name|lower }}}_instance.delete()
    messages.add_message(request, messages.SUCCESS, 'Successfully deleted {{{ model_name }}} #{}'.format(pk))
    return HttpResponseRedirect('/')

{%% endfor %%}