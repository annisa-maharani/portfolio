from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def staff_required(view_func=None, redirect_=REDIRECT_FIELD_NAME, login_='/accounts/logout/'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff and u.is_superuser,
        login_url=login_,
        redirect_field_name=redirect_
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def slug_generator(link):
    link: str = link
    link.replace(" ", "-")
    return link
