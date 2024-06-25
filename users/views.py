from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from .models import CustomUser, PortfolioItem, Order, Discussion, Comment
from .forms import SignUpForm, SignInForm, UserUpdateForm, DiscussionForm, CommentForm
import requests

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Include request.FILES to handle profile pictures
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/sign_up.html', {'form': form})
def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'registration/sign_in.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('home')

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'settings.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('settings')
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {
        'password_change_form': password_change_form,
    })

def custom_password_reset(request):
    return PasswordResetView.as_view(
        request,
        template_name='forgot_password.html',
        email_template_name='forgot_password_email.html',
        subject_template_name='forgot_password_subject.txt',
        post_reset_redirect='/sign_in/',
    )

def portfolio_page(request):
    portfolio_items = PortfolioItem.objects.all()
    return render(request, 'portfolio/portfolio_page.html', {'portfolio_items': portfolio_items})

def portfolio_item_detail(request, item_id):
    portfolio_item = get_object_or_404(PortfolioItem, pk=item_id)
    return render(request, 'portfolio/portfolio_item_detail.html', {'portfolio_item': portfolio_item})

def about_us(request):
    return render(request, 'about_us.html')

@login_required
def order_list(request):
    if request.user.role != 'client':
        return redirect('home')
    orders = Order.objects.filter(client=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    if request.user.role != 'client':
        return redirect('home')
    order = get_object_or_404(Order, pk=order_id, client=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def start_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            new_discussion = form.save(commit=False)
            new_discussion.author = request.user
            new_discussion.save()
            return redirect('discussion_detail', discussion_id=new_discussion.id)
    else:
        form = DiscussionForm()

    discussions = Discussion.objects.all()
    return render(request, 'discussions/start_discussion.html', {'discussions': discussions, 'form': form})

@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    comments = discussion.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.discussion = discussion
            new_comment.author = request.user
            new_comment.save()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = CommentForm()

    return render(request, 'discussions/discussion_detail.html', {'discussion': discussion, 'comments': comments, 'form': form})

@login_required
def add_comment(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = CommentForm()

    return render(request, 'discussions/add_comment.html', {'form': form, 'discussion': discussion})

# New Views for Designer and Client Dashboards
@login_required
def designer_dashboard(request):
    if request.user.role != 'designer':
        return redirect('home')
    # Add specific designer logic here
    return render(request, 'designer_dashboard.html')

@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('home')
    # Add specific client logic here
    return render(request, 'client_dashboard.html')

# Decorators for Role-Based Access
def user_is_designer(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'designer':
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

def user_is_client(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == 'client':
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

@user_is_designer
@login_required
def designer_specific_view(request):
    # Designer-specific view logic
    return render(request, 'designer_specific_view.html')

@user_is_client
@login_required
def client_specific_view(request):
    # Client-specific view logic
    return render(request, 'client_specific_view.html')
