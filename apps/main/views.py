from django.views.generic import TemplateView, DetailView
from .models import Page
from apps.courses.models import Course
from django.shortcuts import get_object_or_404


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_courses'] = Course.objects.filter(state='reg')
        context['page'] = get_object_or_404(Page, slug='home')
        return context


class PageDetailView(DetailView):
    model = Page

    def get_template_names(self):
        return self.object.get_template()
