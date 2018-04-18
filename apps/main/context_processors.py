def main_context(request):
    return {
        'active_url': request.path
    }
