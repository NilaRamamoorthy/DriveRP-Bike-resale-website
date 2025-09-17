from .models import SiteSettings, LoginImage

def site_settings(request): 
    try:
        settings = SiteSettings.objects.first()
        login_image = LoginImage.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    return {'site_settings': settings,
            'login_image': login_image,
            }


