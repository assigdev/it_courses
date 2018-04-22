class SecondHeaderMixin:
    url_name = None
    menu_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = self.url_name
        context['menu_title'] = self.menu_title
        context['menu_courses'] = self.get_queryset()
        return context
