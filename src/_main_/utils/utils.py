from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from _main_.utils.decorators import run_in_background

@run_in_background
def send_universal_email(recipients, subject, template, template_args, attachments=None):
    try:
        """
        Send an email to a list of recipients with optional attachments.
        """
        from_email = "info@csepf.com"

        # Render the email templates with the provided arguments
        text_content = render_to_string(template, template_args)
        html_content = render_to_string(template, template_args)

        # Create the email
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        msg.attach_alternative(html_content, "text/html")

        # Attach files if provided
        if attachments:
            for attachment in attachments:
                msg.attach(attachment['filename'], attachment['content'], attachment['mimetype'])

        # Send the email
        ok = msg.send()
        if not ok:
            raise Exception("Failed to send email")
        return ok

    except Exception as e:
        raise Exception(f"An error occurred while sending the email: {str(e)}")
