from django.contrib import admin
from django.urls import path,include
from tickets import views
from rest_framework.routers import DefaultRouter
router =DefaultRouter()
router.register('gusets',views.viewset_guest)
router.register('movie',views.viewset_movie)
router.register('reservations',views.viewset_reservations)
urlpatterns = [
    path('rest/1/',views.no_rest_no_model),
    path('rest/2/',views.no_rest_from_model),
    path('rest/fpv/',views.Fbv_list),
    path('rest/fpv/<int:pk>',views.Fbv_pk),
    path('rest/cbv/',views.CBV_list.as_view()),
    path('rest/cbv/<int:pk>',views.CBV_pk.as_view()),
    path('rest/mixins/',views.mixins_list.as_view()),
    path('rest/mixins/<int:pk>',views.mixins_pk.as_view()),
    path('rest/generics/', views.generics_list.as_view()),
    path('rest/generics/<int:pk>', views.generics_pk.as_view()),
    path('rest/viewsets/',include(router.urls)),
    path('fbv/findmovie/', views.find_movie),
    path('fbv/create_new/', views.new_reservation),
]