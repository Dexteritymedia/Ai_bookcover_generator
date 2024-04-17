from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.homepage, name='homepage'),
    path('register/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('payment/', views.payment_page, name='payment-page'),
    path('confirm-payment/<int:pk>/', views.confirm_payment, name='confirm-payment'),
    path('payment-done/', views.payment_confirmation, name='confirmation-page'),
    path('make-payment/<int:pk>/', views.make_payment, name='make-payment'),
    path('page/<str:username>/', views.cover_page, name='cover-page'),
    path('resize/<slug>/<id>', views.cover_detail_page, name='resize-cover-page'),
    path('<username>/resize/<slug>/done/', views.resize_cover_page_done, name='resize-cover-page-done'),
    path('cover-generator/', views.cover_generator, name='cover-generator-page'),
    path('image-edit/<slug>/<id>', views.image_manipulation_page, name='image-manipulation-page'),
]


#handler500 = "mysite.views.my_custom_error_view"
#handler404 = "mysite.views.my_custom_page_not_found_view"
#handler403 = "mysite.views.my_custom_permission_denied_view"
#handler400 = "mysite.views.my_custom_bad_request_view"
