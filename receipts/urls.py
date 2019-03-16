from django.urls import path

from . import views

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'receipts'

urlpatterns = [

    # ex: /
    path('receipt', views.IndexView2.as_view(), name='index2'),

    # ex: /post/create/
    path('receipt/create/', views.CreateView2.as_view(), name='create2'),

    # ex: /post/1/
    path('receipt/<int:pk>/', views.DetailView2.as_view(), name='detail2'),

    # ex: /post/1/update/
    path('receipt/<int:pk>/update/', views.UpdateView2.as_view(), name='update2'),

    # ex: /post/1/delete
    path('receipt/<int:pk>/delete/', views.DeleteView2.as_view(), name='delete2'),

    # ex: /post/help/
    # path('post/help/', views.help, name='help'),

]
