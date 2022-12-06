from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from .models import SMTPSetting, MailTemplate
from django.core.mail.backends.smtp import EmailBackend


def send_reset_password(subject,body,receiver):
    smtpsetting = SMTPSetting.objects.last()
    backend = EmailBackend(
                            port=smtpsetting.email_port,
                            username=smtpsetting.email_host_user,
                            password=smtpsetting.email_host_password
                            )
    return send_mail(subject = subject,message = body,from_email = 'no-reply@gmail.com', recipient_list = [receiver] , fail_silently=False, connection=backend)


def send_mail_notification(subject,body,receiver):
    smtpsetting = SMTPSetting.objects.last()
    backend = EmailBackend(
                            port=smtpsetting.email_port,
                            username=smtpsetting.email_host_user,
                            password=smtpsetting.email_host_password
                            )
    return send_mail(subject=subject,message = body,from_email = 'no-reply@gmail.com', recipient_list = [receiver] , fail_silently=False, connection=backend)


def send_email(data):
    smtpsetting = SMTPSetting.objects.last()
    backend = EmailBackend(
                            port=smtpsetting.email_port,
                            username=smtpsetting.email_host_user,
                            password=smtpsetting.email_host_password
                            )
    print('hi')
    return send_mail(subject= data['subject'], message="Dear "+ data['username'] + ", Your Credintials For SMS is Email is "+ data['email'] +" and Password is "+ data['password'] + " .Please Use this Credintials to Login.", from_email= 'no-reply@gmail.com',recipient_list=[data['email']], fail_silently=False, connection=backend)
    #email.send()
    # body1 = MailTemplate.objects.first().send_mail.replace('[PASSWORD]',data['password'])
    # body = body1.replace('[EMAIL]',data['email'])
    # return send_mail("Your Credientials", body.replace('[USERNAME]',data['username']), 'noreply@gmail.com', fail_silently=False, connection=backend)


# class Util:

#     @staticmethod
#     def send_mail(data):
#         smtpsetting = SMTPSetting.objects.last()
#         backend = EmailBackend(port=smtpsetting.email_port,
#                                username=smtpsetting.email_host_user,
#                                password=smtpsetting.email_host_password
#                                )
#         SENDER = smtpsetting.email_host_user
#         # text_content = 'This is an important message.'
#         text_content = """
#                     <div
#                         style="
#                             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                             background-color: #e6e6e6;
#                             width: 100%;
#                             max-width: 400px;
#                             margin: 0 auto;
#                         "
#                         >
#                         <div
#                             style="text-align: center; background-color: #cc8125; padding: 15px 30px"
#                         >
#                             <img
#                             src="#"
#                             alt=""
#                             style="border-radius: 50%; width: 100px; height: 100px; object-fit: cover"
#                             />
#                             <div style="color: white; margin-top: 5px; font-size: 24px">
#                             School Management System
#                             </div>
#                         </div>
#                         <div style="margin: 20px auto 20px; padding: 15px 30px">
#                             <div style="font-size: 18px">Hi there <b>{}</b>,</div>
#                             <div style="padding: 10px 0; font-size: 16px">
#                             We received a request for {} for your account
#                             <b> {} </b>
#                             </div>
#                             <div>For the {}, use email and password given below:</div>
#                             <div style="text-align: center; padding: 10px 0">
#                             </div>
#                             <div style="padding: 10px 0; font-size: 16px">
#                             </div>
#                              <div style="padding: 10px 0; font-size: 16px">
#                             Copy and paste this username or email and password in the website to  log into your account
#                             <b><u>{}</u></b>
#                             </div>
#                             <div style="padding: 10px 0; font-size: 16px">
#                             If you did not request for the {} just ignore this message.
#                             </div>
#                             <div style="text-align: center; margin-top: 10px; font-weight: 500">
#                             !!! Thank You !!!<br>
#                             </div>
#                         </div>
#                         </div>
#         """.format(data['email_user'], data['email_subject'],data['email_receiver'], data['email_subject'],data['password'],data['email_subject'])
#         msg = EmailMultiAlternatives(data['email_subject'], text_content,SENDER, [data['email_receiver']], connection=backend)
#         msg.attach_alternative(text_content, "text/html")
#         msg.send()

