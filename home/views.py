from django.shortcuts import render
from django.conf import settings
import requests


# Create your views here.
def home(request):
    return render(request, "home.html")

def adda(request):
    return render(request, "adda.html")


def slack(request):
    view_data = {}

    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            token = settings.SLACK_TOKEN
            subdomain = settings.SLACK_SUB_DOMAIN
            api_url = "https://{}.slack.com/api/users.admin.invite".format(subdomain)
            res = requests.post(api_url, {
                'email': email,
                'token': token,
                'set_active': 'true'
            })

            data = res.json()

            if not data['ok']:
                if data['error'] == 'already_invited':
                    view_data['message'] = "You are already invited to this team! Please check your email!"
                else:
                    view_data['message'] = "Error: " + data['error']

            else:
                view_data['message'] = "You have been invited. Please check your email!"

    return render(request, "slack.html", view_data)
