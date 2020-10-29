# from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from .forms import ProductForm
from .models import *
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
# from .forms import SignUpForm
from .forms import UserForm
# from sekizai.context import SekizaiContext
#from django.template import RequestContext
# from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, ProductSerializer, CustomUserSerializer
import django_filters.rest_framework
from rest_framework import generics
from rest_framework import filters
# Create your views here.


class UserViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('firstname')
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['=firstname', '=email']

    # class CustomSearchFilter(filters.SearchFilter):
        # def get_search_fields(self, view, request):
        #     if request.query_params.get('firstname'):
        #         return ['firstname']
        #     return super(CustomSearchFilter, self).get_search_fields(view, request)
    ordering_fields = ['firstname', 'lastname', 'city', 'email']
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('product_name')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['=product_name', '=product_type']
    ordering_fields = ['product_name', 'product_type']
    permission_classes = [permissions.IsAuthenticated]


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('firstname')
    serializer_class = CustomUserSerializer


def index(request):
    return render(request, 'product/customTable.html')


def indexpage(request):
     return render(request, "base.html")


def homeIndex(request):
    return render(request, "product/homeIndex.html")


def home(request):
    return render(request, "product/home.html")


def logout_view(request):
    logout(request)
    return redirect('/')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("==============================")
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'product/signup.html', {'form': form})

    # form = SignUpForm(request.POST)
    # if form.is_valid():
    #     user = form.save()
    #     user.refresh_from_db()
    #     user.profile.first_name = form.cleaned_data.get('first_name')
    #     user.profile.last_name = form.cleaned_data.get('last_name')
    #     user.profile.email = form.cleaned_data.get('email')
    #     user.save()
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password1')
    #     user = authenticate(username=username, password=password)
    #     login(request, user)
    #     return redirect('homeIndex')
    # else:
    #     form = SignUpForm()
    # return render(request, 'product/signup.html', {'form': form})


################ login forms###################################################
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'product/login.html', {'form': form})


def ruser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/showUser')

            except:
                pass
    else:
        form = UserForm()
        return render(request, 'product/userIndex.html', {'form': form})


def rproduct(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('/showProduct')
            except:
                pass
    else:
        form = ProductForm()
    return render(request, 'product/productIndex.html', {'form': form})

from django.shortcuts import render as render_to_response
from django.template import RequestContext

#@login_required(login_url='/login/')
def showUser(request):
    if request.user.is_authenticated:

        products = Product.objects.all()
        # pk = request.GET.get('order_by')
        sort = request.GET.get('sort', '')
        desc = request.GET.get('desc', False)
        cuser = User.objects.all()

        ctx = {}
        url_parameter = request.GET.get("q")

        if url_parameter:
            users = cuser.filter(firstname__istartswith=url_parameter)
        else:
            users = cuser

        if sort:
            if desc:
                users = users.order_by("-"+sort)
            else:
                users = users.order_by(sort)

        # user_list = User.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(users, 2)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)


        ctx["users"] = users
        ctx["desc"] = desc
        ctx["q"] = url_parameter
        ctx['sorts'] = sort
        if request.is_ajax():
            html = render_to_string(
                template_name="product/showUserSearch.html", context={"users": users, 'sorts': sort, 'desc' : desc, 'q': url_parameter}
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, "product/showUser.html", context=ctx)

    else:
        return redirect('/')


def userProfile(request, id):
    if request.user.is_authenticated:
        userp = User.objects.get(id=id)
        return render(request, 'product/user_profile.html', {"user": userp})
    else:
        return redirect('/')

def showProduct(request):
    if request.user.is_authenticated:

        products = Product.objects.all()
        if request.GET.get('user_id', ''):
            user = User.objects.get(id=request.GET.get('user_id'))
            products = user.products.all()
            # products = products.filter(user_id=y)

        page = request.GET.get('page', 1)

        paginator = Paginator(products, 5)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request, "product/showProduct.html", {'products': products})
    else:
        return redirect('/')


def showUserProduct(request, id):
    prod = Product.objects.filter(user_id=id)
    return render(request, "product/showProduct.html", {'key2': prod})


def editUser(request, id):
    euser = User.objects.get(id=id)
    return render(request, 'product/editUser.html', {'user': euser})


def editProduct(request, id):
    eproduct = Product.objects.get(id=id)
    return render(request, 'product/editProduct.html', {'prod': eproduct})


# @login_required(login_url='/login/')
def updateUser(request, id):
    if request.user.is_authenticated:

        uuser = User.objects.get(id=id)
        if request.method == "POST":
            form = UserForm(request.POST, instance=uuser)
            if form.is_valid():
                form.save()
                return redirect('/showUser')
        form = UserForm(instance=uuser)

        return render(request, 'product/editUser.html', {'users': form, "id": id})
    else:
        return redirect('/')


def updateProduct(request, id):
    if request.user.is_authenticated:

        uproduct = Product.objects.get(id=id)
        if request.method == "POST":
            form = ProductForm(request.POST, instance=uproduct)
            print("=============================")
            print(form)
            if form.is_valid():
                form.save()
                return redirect('/showProduct')
        form = ProductForm(instance=uproduct)

        return render(request, 'product/editProduct.html', {'prod': form, 'id': id})
    else:
        return redirect('/')


def destroyUser(request, id):
    User.objects.get(id=id).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

def destroyProduct(request, id):
    dproduct = Product.objects.get(id=id)
    dproduct.delete()
    return redirect("/showProduct")

def userProduct(request, id):
    usproduct = Product.objects.filter(user_id=id)
    uname=User.objects.get(id=id)
    return render(request, 'product/userProduct.html', {'prod': usproduct, 'id': uname})


