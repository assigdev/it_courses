from django.views.generic import TemplateView, DetailView
from .models import Page
from apps.courses.models import Course
from django.shortcuts import get_object_or_404
from .mixins import HeaderMixin


class HomeView(HeaderMixin, TemplateView):
    template_name = 'main/home.html'
    header_path = 'main'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_courses'] = Course.objects.filter(state='reg')
        context['page'] = get_object_or_404(Page, slug='home')
        return context


class PageDetailView(HeaderMixin, DetailView):
    model = Page
    header_path = 'main'

    def get_template_names(self):
        return self.object.get_template()
