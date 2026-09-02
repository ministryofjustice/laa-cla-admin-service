from django_entra_auth.backend import  AdfsAuthCodeBackend


class EntraBackend(AdfsAuthCodeBackend):
    def validate_access_token(self, access_token):
        claims = super(EntraBackend, self).validate_access_token(access_token)
        # This should be in the format: First Last [Department]
        names = claims.get("name", "").split(" ")
        if names and len(names) > 2:
            # the last part is the department
            names.pop()

            claims["CLA_FIRST_NAME"] = names.pop(0)
            if names:
                # Todo: Enforce length of last name
                claims["CLA_LAST_NAME"] = " ".join(names)
        return claims

