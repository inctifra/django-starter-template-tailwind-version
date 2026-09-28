from __future__ import annotations

import typing

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

if typing.TYPE_CHECKING:
    from allauth.socialaccount.models import SocialLogin
    from django.http import HttpRequest

    from makalek.users.models import User


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
    ) -> bool:
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def populate_user(
        self,
        request: HttpRequest,
        sociallogin: SocialLogin,
        data: dict[str, typing.Any],
    ) -> User:
        """
        Populates user information from social provider info.

        See: https://docs.allauth.org/en/latest/socialaccount/advanced.html#creating-and-populating-user-instances
        """
        user = super().populate_user(request, sociallogin, data)
        self._populate_user_name(user, data)
        self._populate_user_avatar(user, sociallogin)
        return user

    def _populate_user_name(self, user: User, data: dict[str, typing.Any]) -> None:
        if user.name:
            return

        if name := data.get("name"):
            user.name = name
            return

        if first_name := data.get("first_name"):
            user.name = first_name
            if last_name := data.get("last_name"):
                user.name += f" {last_name}"

    def _populate_user_avatar(self, user: User, sociallogin: SocialLogin) -> None:
        if getattr(user.profile, "avatar", None):
            return

        if avatar_url := self._get_social_avatar_url(sociallogin):
            user.profile.avatar = avatar_url

    def _get_social_avatar_url(self, sociallogin: SocialLogin) -> str | None:
        provider = sociallogin.account.provider
        extra_data = sociallogin.account.extra_data
        match provider:
            case "google":
                return extra_data.get("picture")
            case "facebook":
                return f"https://graph.facebook.com/{extra_data.get('id')}/picture?type=large"
            case "github":
                return extra_data.get("avatar_url")
            case "twitter":
                return extra_data.get("profile_image_url_https")
        return None
