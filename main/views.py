import logging

from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from main.models import Contact

logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    """Home page."""
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        message = request.POST.get("message")
        print(name)
        if name and email and mobile_number and message:
            contact = Contact.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                message=message
            )
            logger.info(f"{contact} Created!")
        else:
            logger.info("The form is invalid")
        return render(request=request, template_name=self.template_name)