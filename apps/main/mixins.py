class HeaderMixin:
    header_path = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_path'] = self.header_path
        return context


class SecondHeaderMixin(HeaderMixin):
    url_name = None
    menu_title = ''

    def get_menu_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_name'] = self.url_name
        context['menu_title'] = self.menu_title
        context['menu_courses'] = self.get_menu_queryset() or self.get_queryset()
        return context
