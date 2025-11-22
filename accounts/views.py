from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import EmailLoginForm, ProfileForm
from .models import UserProfile
from .utils import InvalidToken, generate_login_token, is_allowed_email, verify_login_token


User = get_user_model()


def request_link(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            username = email
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "is_active": True},
            )
            if created:
                UserProfile.objects.create(user=user)

            # Development bypass: log in immediately instead of sending email.
            if settings.DEBUG and getattr(settings, "BYPASS_LOGIN", False):
                login(request, user)
                profile, _ = UserProfile.objects.get_or_create(user=user)
                if profile.require_profile_update or not (
                    user.first_name and user.last_name
                ):
                    return redirect("accounts:profile")

                messages.info(
                    request,
                    "Logged in automatically (BYPASS_LOGIN is enabled).",
                )
                return redirect(settings.LOGIN_REDIRECT_URL)

            # Normal behaviour: send magic-link email.
            token = generate_login_token(email)
            url = request.build_absolute_uri(
                reverse("accounts:magic_login", args=[token])
            )

            subject = "Your sign-in link for Murweh LGA tools"
            body = (
                "Hello,\n\n"
                "Use the link below to sign in. "
                f"It will remain valid for {settings.EMAIL_LOGIN_JWT_EXPIRY_DAYS} days.\n\n"
                f"{url}\n\n"
                "If you did not request this link you can ignore this email."
            )
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])

            messages.success(
                request,
                "We’ve sent a sign-in link to your email. "
                "For development it will also appear in the console.",
            )
            return redirect("accounts:link_sent")
    else:
        form = EmailLoginForm()

    return render(request, "accounts/request_link.html", {"form": form})


def link_sent(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/link_sent.html")


def magic_login(request: HttpRequest, token: str) -> HttpResponse:
    try:
        email = verify_login_token(token)
    except InvalidToken:
        return HttpResponseBadRequest("Invalid or expired login link.")

    if not is_allowed_email(email):
        return HttpResponseBadRequest("Invalid email domain.")

    user = (
        User.objects.filter(username=email).first()
        or User.objects.filter(email=email).first()
    )
    if user is None or not user.is_active:
        return HttpResponseBadRequest("User account is not available.")

    login(request, user)

    profile, _ = UserProfile.objects.get_or_create(user=user)
    if profile.require_profile_update or not (user.first_name and user.last_name):
        return redirect("accounts:profile")

    return redirect(settings.LOGIN_REDIRECT_URL)


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "accounts/profile.html", {"form": form})

