from . import __version__


def display_version(request):
    return {'app_version': __version__}
