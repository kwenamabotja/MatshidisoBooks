import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView

from main.models import Contact
from main.utils.email_utils import EmailUtil
from main.utils.payfast_utils import PayFastUtil

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
            u = EmailUtil()
            u.send_contact_email(contact)
        else:
            logger.info("The form is invalid")
        return render(request=request, template_name=self.template_name)


class PaymentView(LoginRequiredMixin, TemplateView):
    """Payment page."""
    template_name = "payfast.html"

    # def get_context_data(self, **kwargs):
    #     context = super(PaymentView, self).get_context_data(**kwargs)
    #
    #     return context

    def get(self, request):
        context = dict()
        action = request.GET.get("action", "")
        if action == "return":
            print("success")
            context['title'] = "Payment successful"
            context['message'] = "Payment successful"
        elif action == "notify":
            print("notify")
        elif action == "cancel":
            print("cancel")
            context['title'] = "Payment cancelled"
            context['message'] = "Payment cancelled"
        else:
            util = PayFastUtil()
            buyer = {
                "first_name": "Toto",
                "last_name": "Tutu",
                "email": "example@gmail.com",
            }
            context['current_url'] = reverse('pay')
            context["payfast_button"] = util.generate_form(
                buyer=buyer,
                order=None,
                url=f"{request.build_absolute_uri(reverse('pay'))}",
                amount=500.00
            )
            context['title'] = "Pay with Payfast"
            print(context)
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )

