from django.conf import settings

def site_config(request):
    """
    Context processor to make site configuration available in all templates.
    This allows the app to be dynamically configured for different use cases.
    """
    return {
        'site_config': getattr(settings, 'SITE_CONFIG', {
            'SITE_NAME': 'FlexOpt Selection System',
            'SITE_DESCRIPTION': 'Dynamic selection system for quizzes and subject assignments',
            'SITE_LOGO_TEXT': 'FlexOpt',
            'DEFAULT_QUIZ_TYPE': 'Selection Quiz',
            'DEFAULT_SUBJECT_TYPE': 'Subject',
        })
    }
