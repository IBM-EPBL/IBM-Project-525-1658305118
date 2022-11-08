import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(api_key= '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' )
from_email = Email("itaswinic@gmail.com")
to_email = To("aswinichittibabu05@gmail.com")
subject = "Sending with SendGrid is Fun"
content = Content("text/plain", "and easy to do anywhere, even with Python")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
