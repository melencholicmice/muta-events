import jwt
import requests
import google_auth_oauthlib.flow
from muta_event.settings import (
    GOOGLE_OAUTH2_CLIENT_ID,
    GOOGLE_OAUTH2_CLIENT_SECRET,
    GOOGLE_OAUTH2_PROJECT_ID,
    BASE_BACKEND_URL
)
from django.core.exceptions import ImproperlyConfigured
from dataclasses import dataclass
from utils.api_exception import ApiException

@dataclass
class GoogleRawLoginCredentials:
    client_id: str
    client_secret: str
    project_id: str

@dataclass
class GoogleAccessTokens:
    id_token: str
    access_token: str

def google_raw_login_get_credentials() -> GoogleRawLoginCredentials:
    # print("GOOGLE_OAUTH2_CLIENT_ID", GOOGLE_OAUTH2_CLIENT_ID)   
    client_id = GOOGLE_OAUTH2_CLIENT_ID
    client_secret = GOOGLE_OAUTH2_CLIENT_SECRET
    project_id = GOOGLE_OAUTH2_PROJECT_ID

    if not client_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_ID missing in env.")

    if not client_secret:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_CLIENT_SECRET missing in env.")

    if not project_id:
        raise ImproperlyConfigured("GOOGLE_OAUTH2_PROJECT_ID missing in env.")

    credentials = GoogleRawLoginCredentials(
        client_id=client_id,
        client_secret=client_secret,
        project_id=project_id
    )

    return credentials


class GoogleSdkLoginFlowService:
    # Two options are available: 'web', 'installed'
    GOOGLE_CLIENT_TYPE = "web"

    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

    # Add auth_provider_x509_cert_url if you want verification on JWTS such as ID tokens
    GOOGLE_AUTH_PROVIDER_CERT_URL = ""

    SCOPES = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    def __init__(self):
        self._credentials = google_raw_login_get_credentials()

    def _get_redirect_uri(self):
        domain = BASE_BACKEND_URL
        redirect_uri = f"{domain}/user/google-auth-callback"
        return redirect_uri

    def _generate_client_config(self):
        # This follows the structure of the official "client_secret.json" file
        client_config = {
            self.GOOGLE_CLIENT_TYPE: {
                "client_id": self._credentials.client_id,
                "project_id": self._credentials.project_id,
                "auth_uri": self.GOOGLE_AUTH_URL,
                "token_uri": self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
                "auth_provider_x509_cert_url": self.GOOGLE_AUTH_PROVIDER_CERT_URL,
                "client_secret": self._credentials.client_secret,
                "redirect_uris": [self._get_redirect_uri()],
                "javascript_origins": [],
            }
        }
        return client_config

    # Reference:
    # https://developers.google.com/identity/protocols/oauth2/web-server#creatingclient
    def get_authorization_url(self):
        redirect_uri = self._get_redirect_uri()
        client_config = self._generate_client_config()

        google_oauth_flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=client_config, scopes=self.SCOPES
        )
        google_oauth_flow.redirect_uri = redirect_uri

        authorization_url, state = google_oauth_flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="select_account",
        )
        return authorization_url, state
    
    def get_tokens(self, *, code: str, state: str) -> GoogleAccessTokens:
        redirect_uri = self._get_redirect_uri()
        client_config = self._generate_client_config()

        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config=client_config, scopes=self.SCOPES, state=state
        )
        flow.redirect_uri = redirect_uri
        access_credentials_payload = flow.fetch_token(code=code)

        if not access_credentials_payload:
            raise ApiException("Failed to obtain tokens from Google.",400)

        google_tokens = GoogleAccessTokens(
            id_token=access_credentials_payload["id_token"], 
            access_token=access_credentials_payload["access_token"]
        )

        return google_tokens
    
    def decode_id_token(self, id_token: str):
        decoded_token = None
        try:
            decoded_token = jwt.decode(jwt=id_token, options={"verify_signature": False})
        except ValueError:
            raise ApiException("Failed to decode ID token.",400)
        return decoded_token
    
    def get_user_info(self, *, google_tokens: GoogleAccessTokens):
        access_token = google_tokens.access_token

        response = requests.get(
            self.GOOGLE_USER_INFO_URL,
            params={"access_token": access_token}
        )

        if not response.ok:
            raise ApiException("Failed to obtain user info from Google.",400)

        return response.json()
