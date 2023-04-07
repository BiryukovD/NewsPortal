def is_not_author(request):
    is_not_author = request.user.groups.filter(name='authors').exists()
    is_not_author = not is_not_author
    return {
        'is_not_author': is_not_author
        }