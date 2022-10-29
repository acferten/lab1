from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'polls'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('<int:pk>/', views.DetailView.as_view(), name='detail'),
                  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
                  path('<int:question_id>/vote/', views.vote, name='vote'),
                  path('signup', views.SignUpView.as_view(), name='signup'),
                  path('user/<int:pk>/', views.UserDetailView.as_view(), name='profile'),
                  path('user/<int:pk>/delete', views.UserDeleteView.as_view(), name='user-delete'),
                  path('user/<int:pk>/update', views.UserUpdateView.as_view(), name='user-update'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
