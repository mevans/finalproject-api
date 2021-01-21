import requests

from tracker import settings


class DynamicLinks:
    def __init__(self, api_key):
        self.api_key = api_key

    def endpoint(self):
        return f"https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={self.api_key}"

    def short_url(self, url):
        data = {
            "dynamicLinkInfo": {
                "domainUriPrefix": "https://evans99.page.link",
                "link": url,
                "androidInfo": {
                    "androidPackageName": settings.ANDROID_PACKAGE_NAME,
                }
            }
        }
        response = requests.post(url=self.endpoint(), json=data).json()
        return response

    def generate_invite_link(self, token):
        url = f"https://www.canoe.io/accept-invite?token={token}"
        response = self.short_url(url)
        return response.get("shortLink")


dynamic_links = DynamicLinks(settings.FIREBASE_API_KEY)
