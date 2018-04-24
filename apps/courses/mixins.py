from django.http import JsonResponse


class AjaxFormMixin:
    success_message = ''
    form = None

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.get_ajax_response()
        return super().get(request, *args, **kwargs)

    def get_ajax_response(self):
        ajax_context = self.get_ajax_context_data()
        return JsonResponse(ajax_context)

    def get_ajax_context_data(self):
        context = {'is_error': False}
        form = self.form(self.request.POST)
        if form.is_valid():
            form.save()
            context['message'] = self.success_message
        else:
            print(form)
            context['message'] = 'Отправленны не валидные данные'
            context['is_error'] = True
        return context

    def get_form(self):
        return self.form()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
