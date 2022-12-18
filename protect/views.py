from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from pytz import common_timezones
from django.http import HttpResponseRedirect


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request):

        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'default.html', {'timezones': common_timezones})
