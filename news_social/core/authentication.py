from rest_framework.authentication import TokenAuthentication

from rest_auth.models import TokenModel


class CustomTokenAuthentication(TokenAuthentication):
    """
        Exempts CSRF token.
    """
    model = TokenModel

    def authenticate_credentials(self, key):
        data = super().authenticate_credentials(key)
        # Have scope to add more check on token validity later with maturity.
        return data
