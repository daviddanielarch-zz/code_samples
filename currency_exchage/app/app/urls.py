"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework.documentation import include_docs_urls

from trade.views import home, create_trade, TradeAPI, GetRate

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^trade_create/$', create_trade, name='create-trade'),
    url(r'^trades/', TradeAPI.as_view(), name='trade-api'),
    url(r'^rate/', GetRate.as_view(), name='get-rate'),
    url(r'^docs/', include_docs_urls(title='Exchange API', public=False))
]

