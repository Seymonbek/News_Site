from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .forms import UserRegistrationForm, ProfileEditForm, UserEditForm
from .models import Profile


@login_required
def dashboard_view(request):
    user = request.user
    # get_or_create: agar profil yo'q bo'lsa (admin orqali yaratilgan user) avtomatik yaratadi
    profile, _ = Profile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'pages/user_profile.html', context)


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # commit=False: avval parolni to'g'ri hash qilib, keyin saqlaymiz
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
        return render(request, 'account/register.html', {'user_form': user_form})

    user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


class EditUserView(LoginRequiredMixin, View):

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileEditForm(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/profile_edit.html', context)

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/profile_edit.html', context)
