import autocomplete_light
from account.forms import SignupForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from geonode.base.forms import ResourceBaseForm
from geonode.layers.models import Layer
from geonode.base.forms import Profile
from geonode.base.models import ResourceBase
import taggit
from geonode.groups.models import GroupProfile
from geonode.groups.forms import GroupForm, GroupUpdateForm

class MapStorySignupForm(SignupForm):
    """
    Extends the accounts SignupForm to include the user's first and last name and subscribtion to monthly digest.
    """

    firstname = forms.CharField(
        label=_("First name"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    lastname = forms.CharField(
        label=_("Last name"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )

    digest = forms.BooleanField(
        label=_("Monthly email digest"),
        required=False
    )


class UploadLayerForm(ResourceBaseForm):

    poc = forms.CharField(
        label=_("poc"),
        widget=forms.HiddenInput(),
        required=False,
    )

    metadata_author = forms.CharField(
        label=_("metadata_author"),
        widget=forms.HiddenInput(),
        required=False,
    )

    supplemental_information = forms.CharField(
        label=_('Data Source'),
        required=False,
        widget=forms.TextInput(),
        initial=''
    )

    data_quality_statement = forms.CharField(
        label=_('Data Quality'),
        widget=forms.TextInput(),
        required=False,
    )


    def __init__(self, *args, **kwargs):
        super(UploadLayerForm, self).__init__(*args, **kwargs)
        for field in 'date temporal_extent_start temporal_extent_end thumbnail_url'.split():
            self.fields.pop(field)

    class Meta(ResourceBaseForm.Meta):
        model = Layer
        exclude = ResourceBaseForm.Meta.exclude + (
            'workspace',
            'store',
            'storeType',
            'typename',
            'default_style',
            'styles',
            'upload_session',
            'service',
            'owner',
            'date',
            'date_type',
            'edition',
            'abstract',
            'purpose',
            'maintenance_frequency',
            'restriction_code_type',
            'constraints_other',
            'license',
            'language',
            'spatial_representation_type',
            'distribution_url',
            'distribution_description',
            'is_published',
            'featured'
        )
        # TODO: Refactor this for the latest version of Autocomplete Light.
        # widgets = autocomplete_light.get_widgets_dict(Layer)

# A form for just keywords
class KeywordsForm(forms.ModelForm):

    class Meta:
        model = ResourceBase
        fields = ['keywords']


# A form for just Metadata
class MetadataForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MetadataForm, self).__init__(*args, **kwargs)
        self.fields['distribution_url'].label = "Data Source"
        self.fields['abstract'].label = "Summary"

    class Meta:
        model = ResourceBase
        fields = [
            'title',
            'category',
            'language',
            'abstract',
            'distribution_url',
            'data_quality_statement',
            'purpose',
            'is_published',
        ]

# A form for just publishing status
class PublishStatusForm(forms.ModelForm):

    class Meta:
        model = ResourceBase
        fields = ['is_published']

# A form for just deactivating profile
class DeactivateProfileForm(forms.ModelForm):
    is_active = forms.BooleanField(help_text=_("Uncheck the field and select confirm to deactivate your profile."), required=False)

    class Meta:
        model = Profile
        fields = ['is_active']

# A form for the fields we want the user to be able to edit
class EditProfileForm(forms.ModelForm):
    Volunteer_Technical_Community = forms.BooleanField(help_text=_("Join the Volunteer Technical Community (What's this? Learn more <a href='http://wiki.mapstory.org/wiki/Volunteer_Technical_Community'>here</a>)"), required=False)
    keywords = taggit.forms.TagField(
        required=False,
        label='Interests',
        help_text=_("A list of personal interests (separate each interest with a comma)"))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'keywords', 'city', 'country', 'profile', 'education', 'expertise', 'social_twitter', 'social_facebook', 'social_linkedin', 'social_github', 'Volunteer_Technical_Community']

# Organization forms
class OrganizationForm(GroupForm):

    class Meta:
        model = GroupProfile
        exclude = ['group', 'profile_type', 'tasks', 'featured']


class OrganizationUpdateForm(GroupUpdateForm):

    class Meta:
        model = GroupProfile
        exclude = ['group', 'profile_type', 'tasks', 'featured']