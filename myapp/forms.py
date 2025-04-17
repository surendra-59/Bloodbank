from django import forms
from .models import CustomUser  # Import CustomUser model
from django.core.exceptions import ValidationError


# forms.py
from django import forms

class Login_form(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com',
            'aria-label': 'Email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'aria-label': 'Password'
        }),
        required=True
    )

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password',
            'id': 'password'
        }),
        label="New Password",
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password',
            'id': 'confirm_password'
        }),
        label="Confirm Password",
        required=True
    )




class RegisterForm(forms.ModelForm):
    contact_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Contact Number"}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}), required=True)
    # identity = forms.FileField(required=True)
    identity = forms.FileField(
        required=True,
        label="Identity Proof",
        label_suffix="",  # Removes the colon
    )


    dob = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Enter your address"}), required=True)
    organization_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Organization Name"}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Last Name"}))


    class Meta:
        model = CustomUser
        fields = ["email", "user_type", "gender", "profile_pic", "address", "identity",
                  "contact_number", "dob", "blood_group", "organization_name", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields["user_type"].choices = [choice for choice in self.fields["user_type"].choices if choice[0] in ["2", "3"]]

        # Get user_type from data (handle both GET and POST requests)
        user_type = self.data.get("user_type") or self.initial.get("user_type")

        if user_type == "2":  # Hospital
            self.fields["dob"].required = False
            self.fields["gender"].required = False
            self.fields["blood_group"].required = False
            self.fields["first_name"].required = False
            self.fields["last_name"].required = False
            # self.fields["organization_name"].required = True
            self.fields["organization_name"].required = False  # We handle the requirement dynamically

        if user_type == "3":  # Regular user
            self.fields["dob"].required = True
            self.fields["gender"].required = False
            self.fields["blood_group"].required = False
            self.fields["first_name"].required = False
            self.fields["last_name"].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        user_type = cleaned_data.get("user_type")

        # Password validation
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        # Hospital-specific validation
        if user_type == "2":
            # if not cleaned_data.get("organization_name"):
            organization_name = cleaned_data.get("organization_name")
            if not organization_name:
                # Raising a ValidationError for custom error message
                self.add_error('organization_name',"Organization name is required.")
            if not cleaned_data.get("identity"):
                self.add_error("identity", "Hospital must upload an identity document.")

        # Regular user-specific validation
        elif user_type == "3":
            if not cleaned_data.get("first_name") or not cleaned_data.get("last_name"):
                self.add_error("first_name", "First name is required for regular users.")
                self.add_error("last_name", "Last name is required for regular users.")
                if not cleaned_data.get("blood_group"):
                    self.add_error("blood_group", "Blood group is required for regular users.")
                if not cleaned_data.get("gender"):
                    self.add_error("gender", "Gender is required for regular users.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get("user_type")

        if user_type == "2":  # If hospital

            user.organization_name = self.cleaned_data.get("organization_name")
            user.is_staff = True  # Mark hospitals as staff
            user.identity = self.cleaned_data.get("identity")
            # Encrypt the password before saving
        user.set_password(self.cleaned_data.get("password"))

        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label='Old Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label='Confirm New Password'
    )

class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_pic', 'first_name', 'last_name', 'email', 'contact_number', 'address', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HospitalProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['organization_name', 'email', 'contact_number', 'address','profile_pic', 'identity']
        widgets = {
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }







        

