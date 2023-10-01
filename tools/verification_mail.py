import secrets

from flask_mail import Mail, Message

from tools import models


class EmailVerificator:
    def __init__(self, app):
        self.app = app
        self.mail = Mail(app)

    def send_verification_email(self, user: models.User):
        token = self.generate_verification_token(user)
        verification_link = f"http://your-website.com/verify/{token}"

        msg = Message(
            "Verify Your Email",
            sender="noreply@your-website.com",
            recipients=[user.email],
        )
        msg.body = f"Hello {user.full_name},\n\nPlease click the following link to verify your email: {verification_link}"

        try:
            self.mail.send(msg)
            print(msg)
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def generate_verification_token(user):
        # You can generate a unique token for email verification here
        # For simplicity, let's assume you have a method that generates tokens
        # Replace 'generate_token()' with your actual token generation logic
        token = generate_token()
        expiration_date = datetime.datetime.now() + datetime.timedelta(hours=24)
        verification_token = models.VerificationToken(
            token=token,
            user_id=user.id,
            expiration_date=expiration_date,
        )
        models.db.session.add(verification_token)
        models.db.session.commit()
        return token

    @staticmethod
    def generate_token(length=32):
        # Generate a random token with the specified length
        token = secrets.token_hex(
            length // 2
        )  # `token_hex` generates bytes, so we divide by 2 to get the desired length in hex characters

        return token
