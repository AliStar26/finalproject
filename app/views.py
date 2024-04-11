from typing import Any
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser, Products, Category,Comment
from .forms import  SignUpForm, CommentForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.views import View



def home(request):
    return render(request, 'home.html')

class SignUpView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name= 'signup.html'
    success_url = reverse_lazy('home')
    success_message = 'Account created successfully'


    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        link = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}/')
        subject = 'Email confirmation'
        body = f'{user.username}, Activate your account by clicking on the link: {link}'
        send_mail(
            subject,body, 'alikhanilyassov@gmail.com',[user.email]
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object  
        user.is_active = False
        user.save()
        self.send_verification_email(self.object)
        return response


class VerifyEmailView(View):
    def get(self, request, user_pk, token):
        user = CustomUser.objects.get(pk=user_pk)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified')
            return redirect('login')
        else:
            messages.error(request, 'The link is invalid')
            return redirect('home')
    

class CustomLoginView(SuccessMessageMixin,LoginView):
    template_name = 'login.html'
    success_message = "You were successfully logged in."
    
    def form_valid(self, form):
        user = form.get_user()
        if  user.is_active:
            super().form_valid(form)
        return redirect(reverse('home'))
        
class Logout(LogoutView):
    next_page = reverse_lazy('home')

class CategoryListView(ListView):
    model = Category
    template_name = 'home.html'
    context_object_name = 'categories'


def home(request):
    categories = Category.objects.all()
  
    paginator = Paginator(categories, 3)
    if 'page' in request.GET:
        page = request.GET['page']
    else:
        page = 1
    page = paginator.get_page(page)

    return render(request, 'home.html', {'page': page})
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Products.objects.filter(category=self.object).order_by('created_at')
        paginator = Paginator(products, 3)
        page_number = self.request.GET.get('page', 1)
        page = paginator.page(page_number)
        context['page'] = page
        print(page.object_list)
        return context

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Category
    template_name = 'category_create.html'
    fields = ['name', 'image']
    success_url = reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

class CategoryUpdateView(LoginRequiredMixin,UpdateView):
    model = Category
    template_name = 'category_update.html'
    fields = ['name']
    success_url = reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    

    

    
    

class CategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('home')


class ProductListView(ListView):
    model = Products
    template_name = 'product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Products
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentForm'] = CommentForm()
        content_type = ContentType.objects.get_for_model(self.object)
        context['comments'] = Comment.objects.filter(content_type=content_type, object_id=self.object.id)
        return context

    
    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        user = request.user  
        self.object = self.get_object()
        Comment.objects.create(content=content, content_object=self.object, user=user)
        return redirect(reverse('product_detail', kwargs={'pk': self.object.pk}))

class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Products
    template_name = 'product_create.html'
    fields = ['name', 'description', 'image', 'price', 'category', 'quantity']
    
    def get_success_url(self):
        category_id = self.object.category_id
        return reverse_lazy('category_detail', kwargs={'pk': category_id})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    template_name = 'product_update.html'
    fields = ['name', 'description', 'image', 'price', 'category', 'quantity']

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Products
    template_name = 'product_delete.html'

    
    def get_success_url(self):
        category_id = self.object.category_id
        return reverse_lazy('category_detail', kwargs={'pk': category_id})

    
