"""demo0414_userauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from account import views as av

urlpatterns = [
    url(r'^$', av.hello),
    url(r'^login/$',av.login, name = 'login'),
    url(r'^register/$',av.register, name = 'register'),
    url(r'^logout/$',av.logout, name = 'logout'),
    url(r'^checkcode/$',av.check_code, name = 'checkcode'),
    url(r'^admin/', admin.site.urls),
    url(r'^servicelist/$', av.goToServicePage, name="servicelist"),
    url(r'^sleepcondition/$', av.testPosting, name="sleepcondition"),
    #url(r'^testPosting/$', av.testPosting, name="tp"),


]
