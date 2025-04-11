from django.forms import ModelForm

from .models import TeamMember


class TeamMemberForm(ModelForm):
    class Meta:
        model = TeamMember
        fields = "__all__"

class TeamMemberUpdateForm(TeamMemberForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True
