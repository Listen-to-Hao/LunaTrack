from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    nickname = forms.CharField(max_length=50, required=False, help_text="Optional nickname")

    class Meta:
        model = UserProfile
        fields = ["username", "nickname", "email", "password1", "password2"]

    def clean_email(self):
        # Ensure that the email is unique by checking if it already exists in the database.
        email = self.cleaned_data.get("email")
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password1(self):
        # Ensure that the password is at least 8 characters long.
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password1

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "nickname", "height", "age_group"]

class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)  # ✅ Allows the avatar to remain unchanged if not provided
    nickname = forms.CharField(required=False)
    height = forms.FloatField(required=False)
    age_group = forms.ChoiceField(choices=UserProfile.AGE_GROUPS, required=False)

    class Meta:
        model = UserProfile
        fields = ["nickname", "avatar", "height", "age_group"]

    def clean_avatar(self):
        """ Ensure that the avatar field isn't cleared if no new avatar is uploaded """
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            return self.instance.avatar  # Keeps the existing avatar if none is uploaded
        return avatar

    def clean_nickname(self):
        """ Ensure that the nickname field keeps the original nickname if no new one is provided """
        nickname = self.cleaned_data.get("nickname")
        if not nickname:
            return self.instance.nickname  # Keeps the existing nickname if none is provided
        return nickname

    def clean_height(self):
        """ Allow height to remain empty, using the existing value if not provided """
        height = self.cleaned_data.get("height")
        if height is None:
            return self.instance.height  # Keeps the existing height if not provided
        return height

    def clean_age_group(self):
        """ Allow age group to remain empty, using the existing value if not provided """
        age_group = self.cleaned_data.get("age_group")
        if not age_group:
            return self.instance.age_group  # Keeps the existing age group if not provided
        return age_group
