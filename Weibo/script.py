from __future__ import division
from weibo import APIClient
import unirest

API_KEY = "959242827"
API_SECRET = "fee01d102c48b3c5f361c6d629856614"
REDIRECT_URI = "https://github.com/nd7141"

if __name__ == "__main__":
    # client = APIClient(app_key=API_KEY, app_secret=API_SECRET, redirect_uri=REDIRECT_URI)
    # url = client.get_authorize_url()
    #
    # print url

    response = unirest.post("https://shadow-weibo.p.mashape.com/oauth2/authorize",
  headers={
    "X-Mashape-Key": "e73VTWNYKMmsh0xTI7MtSwTzReeyp1N1FfxjsnrZPJamej6xKL",
    "Content-Type": "application/x-www-form-urlencoded"
  },
  params={
    "client_id": "959242827",
    "redirect_uri": "https://github.com/nd7141"
  }
)

    print response

    console = []

    # code = your.web.framework.request.get('code')
    # r = client.request_access_token(code)
    # access_token = r.access_token
    # expires_in = r.expires_in

    # print expires_in
    # token = c.token
    # print token
    #
    # c2 = Client(API_KEY, API_SECRET, REDIRECT_URI, token)
    # c2.get('users/show', uid=2703275934)