# Optional: add contact me email functionality (Day 60)
# import smtplib
from dotenv import load_dotenv
from flask import render_template
from flask_bootstrap import Bootstrap5
from flask_gravatar import Gravatar
from flask_login import current_user

from app import create_app
from app.config import DevConfig
from app.extensions import db

"""
Make sure the required packages are installed: 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
"""

load_dotenv()

app = create_app(DevConfig)
Bootstrap5(app)

# For adding profile images to the comment section
gravatar = Gravatar(
    app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)

with app.app_context():
    db.create_all()



@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html", current_user=current_user)


# Optional: You can include the email sending code from Day 60:
# DON'T put your email and password here directly! The code will be visible when you upload to Github.
# Use environment variables instead (Day 35)

# MAIL_ADDRESS = os.environ.get("EMAIL_KEY")
# MAIL_APP_PW = os.environ.get("PASSWORD_KEY")

# @app.route("/contact", methods=["GET", "POST"])
# def contact():
#     if request.method == "POST":
#         data = request.form
#         send_email(data["name"], data["email"], data["phone"], data["message"])
#         return render_template("contact.html", msg_sent=True)
#     return render_template("contact.html", msg_sent=False)
#
#
# def send_email(name, email, phone, message):
#     email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(MAIL_ADDRESS, MAIL_APP_PW)
#         connection.sendmail(MAIL_ADDRESS, MAIL_APP_PW, email_message)


if __name__ == "__main__":
    app.run(debug=False, port=5001)
