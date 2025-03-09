from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=50, required=False, help_text="Optional nickname")

    class Meta:
        model = UserProfile
        fields = ["username", "nickname", "email", "password1", "password2"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar", "nickname", "height", "weight", "age_group"]

class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)  # ✅ 允许头像不更改
    nickname = forms.CharField(required=False)
    height = forms.FloatField(required=False)
    weight = forms.FloatField(required=False)
    age_group = forms.ChoiceField(choices=UserProfile.AGE_GROUPS, required=False)

    class Meta:
        model = UserProfile
        fields = ["nickname", "avatar", "height", "weight", "age_group"]

    def clean_avatar(self):
        """ 确保用户不上传头像时不会清空字段 """
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            return self.instance.avatar  # ✅ 返回已有的头像，而不是 `None`
        return avatar

    def clean_nickname(self):
        """ 确保用户不修改昵称时，保留原昵称 """
        nickname = self.cleaned_data.get("nickname")
        if not nickname:
            return self.instance.nickname
        return nickname

    def clean_height(self):
        """ 允许 height 为空 """
        height = self.cleaned_data.get("height")
        if height is None:
            return self.instance.height
        return height

    def clean_weight(self):
        """ 允许 weight 为空 """
        weight = self.cleaned_data.get("weight")
        if weight is None:
            return self.instance.weight
        return weight

    def clean_age_group(self):
        """ 允许 age_group 为空 """
        age_group = self.cleaned_data.get("age_group")
        if not age_group:
            return self.instance.age_group
        return age_group
