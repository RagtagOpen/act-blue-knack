from django.conf.urls import url

from sync import views

urlpatterns = [url(r"^sync/", views.sync, name="sync")]
