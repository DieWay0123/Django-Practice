from django.core.signing import TimestampSigner


class EmailToken(object):
    def __init__(self):
        self.salt = ":poop:"

    def generate_token(self, email):
        signer = TimestampSigner(salt=self.salt).sign_object(email)
        return signer

    def confirm_token(self, token):
        email = TimestampSigner(salt=self.salt).unsign_object(token)
        return email
