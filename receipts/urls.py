from django.urls import path, include

from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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

    # path('images/', include('receipts.urls'))

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
