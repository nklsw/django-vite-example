from django.forms import ModelForm

from .models import TeamMember


class TeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = "__all__"  # noqa: DJ007


class TeamMemberUpdateForm(TeamMemberForm):
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True
