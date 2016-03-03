# from threading import Thread
from flask import current_app, render_template
# from flask.ext.mail import Message
# from . import mail
#

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)


# def send_email(to, subject, template, **kwargs):


    # app = current_app._get_current_object()
    # msg = Message(app.config['WOTER_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
    #               sender=app.config['WOTER_MAIL_SENDER'], recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html', **kwargs)
    # thr = Thread(target=send_async_email, args=[app, msg])
    # thr.start()
    # return thr
from sae.mail import EmailMessage


def send_email(to, subject, template, **kwargs):
    m = EmailMessage()
    app = current_app._get_current_object()
    m.to = to
    m.subject = app.config['WOTER_MAIL_SUBJECT_PREFIX'] + ' ' + subject
    m.html = render_template(template + '.html', **kwargs)
    m.smtp = (app.config['MAIL_SERVER'], app.config['MAIL_PORT'], app.config['MAIL_USERNAME'],
              app.config['MAIL_PASSWORD'], app.config['MAIL_USE_TLS'])
    m.send()
