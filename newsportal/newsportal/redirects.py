from django.shortcuts import redirect


def redirect_to_profile(request):
    return redirect(f'/account/profile/{request.user.pk}')
