from django.shortcuts import render
from temoignage.models import Abonnee

from django.core.mail import send_mail
from django.http import JsonResponse

def admin_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipients = [subscriber.email for subscriber in Abonnee.objects.all()]
        
        for recipient in recipients:
            send_mail(subject, message, "montemoignage.christ@gmail.com", [recipient])
            
        return JsonResponse({'success': True, 'message': 'Email sent successfully'})
    return render(request, 'email_form.html')
