from django.urls import path, include
from product import views
from rest_framework import routers
from . import views

# from django.conf.urls import include, url

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'customuser', views.CustomUserViewSet)

urlpatterns = [

    # path("",views.home),
    # path("",views.homeIndex,name="homeIndex"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('customuser/', views.index, name='customuser'),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    # path('home/',views.home ),
    path('indexpage/', views.indexpage),

    path('userreg/', views.ruser, name="userreg"),
    path('productreg/', views.rproduct, name="productreg"),

    path('showUser/', views.showUser),
    path('showProduct/', views.showProduct),

    path('userProduct/<int:id>', views.userProduct),

    path("userProfile/<int:id>", views.userProfile),

    path('updateUser/<int:id>', views.updateUser, name="updateUser"),
    path('updateProduct/<int:id>', views.updateProduct, name="updateProduct"),

    path('deleteUser/<int:id>', views.destroyUser, name="deleteUser"),
    path('deleteProduct/<int:id>', views.destroyProduct, name="deleteProduct"),


]
