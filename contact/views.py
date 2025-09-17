from django.shortcuts import render

from .forms import ContactForm

def contact_home(request):
    form = ContactForm()
    return render(request, 'contact/contact_form.html', {'form': form})


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ContactForm

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .forms import ContactForm

def contact_form_view(request):
    show_modal = False
    print("CONTACT FORM VIEW HIT")
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            # Send email
            subject = f"New Contact Form Submission from {submission.name}"
            body = (
                f"Name: {submission.name}\n"
                f"Email: {submission.email}\n"
                f"Phone: {submission.phone}\n"
                f"Reason: {submission.reason}\n"
                f"Source: {submission.source}\n\n"
                f"Message:\n{submission.message}"
            )

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_RECEIVER_EMAIL],
                fail_silently=False,
            )
            print("Form errors:", form.errors)
            show_modal = True
            form = ContactForm()  # clear form after submission
        else:
            print("Form is not valid:", form.errors)

    else:
        form = ContactForm()
        

    return render(request, 'contact/contact_form.html', {
        'form': form,
        'show_modal': show_modal,
    })


