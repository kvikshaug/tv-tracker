from django import forms

from captcha.fields import ReCaptchaField

class CaptchaForm(forms.Form):
    captcha = ReCaptchaField()
