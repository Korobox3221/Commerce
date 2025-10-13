from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path('listing/<str:title>', views.listing_page, name = "listing_page"),
    path('error/<str:message>', views.error, name = 'error'),
    path('watchlist/<str:username>/', views.wishlist, name = 'watchlist'),
    path('categories', views.categories, name = 'categories'),
    path('category/<str:category>', views.category, name = 'category')
]
