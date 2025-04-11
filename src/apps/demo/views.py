from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from .forms import TeamMemberForm, TeamMemberUpdateForm
from .models import TeamMember


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html", {"message": "Hello World!"})


class TeamMembersListView(ListView):
    model = TeamMember
    template_name = "team_members.html"


class TeamMemberFormView(FormView, CreateView):
    template_name = "form.html"
    form_class = TeamMemberForm

    def get_success_url(self) -> str:
        return reverse("team_member_detail", args=[self.object.pk])

    def form_valid(self, form: TeamMemberForm) -> HttpResponse:
        self.request.up.layer.emit("member:created", {})
        return super().form_valid(form)


class TeamMemberEditFormView(UpdateView):
    model = TeamMember
    template_name = "form.html"
    form_class = TeamMemberUpdateForm

    def get_success_url(self) -> str:
        return reverse("team_member_detail", args=[self.object.pk])


class TeamMemberDetailView(DetailView):
    model = TeamMember
    template_name = "team_detail.html"
