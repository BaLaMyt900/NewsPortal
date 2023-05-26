from my_account.forms import UserLoginForm


def get_context_data(request):
    context = {
        'login_ajax': UserLoginForm()
    }
    return context
