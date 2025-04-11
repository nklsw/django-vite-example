from django.urls import path
from django.views.decorators.cache import cache_page
from django.views.i18n import JavaScriptCatalog

from .views import (
    TeamMemberDetailView,
    TeamMemberEditFormView,
    TeamMemberFormView,
    TeamMembersListView,
)

urlpatterns = [
    path("team/list", TeamMembersListView.as_view(), name="team_members_list"),
    path("team/add", TeamMemberFormView.as_view(), name="team_member_add"),
    path("team/<int:pk>/edit", TeamMemberEditFormView.as_view(), name="team_member_edit"),
    path("team/<int:pk>", TeamMemberDetailView.as_view(), name="team_member_detail"),
    path(
        "jsi18n/",
        cache_page(3600)(JavaScriptCatalog.as_view(packages=["formset"])),
        name="javascript-catalog"
    ),

]
