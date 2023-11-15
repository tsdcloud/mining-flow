"""mine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include
from common.router import OptionalSlashRouter

from article import views as aviews
from career import views as cviews
from car import views as carviews

router = OptionalSlashRouter()
router.register(r'categorie', aviews.CategorieViewSet, basename='categorie')
router.register(r'article', aviews.ArticleViewSet, basename='article')
router.register(
    r'stockageaera', cviews.StockageAeraViewSet, basename='stockageaera')
router.register(r'career', cviews.CareerViewSet, basename='career')
router.register(
    r'stockageaeralv', cviews.StockageAeraLvViewSet, basename='stockageaeralv')
router.register(r'careerlv', cviews.CareerLvViewSet, basename='careerlv')
router.register(
    r'careerarticle', cviews.CareerArticleViewSet, basename='careerarticle')
router.register(
    r'stockagepartnerarticle',
    cviews.StockagePartnerArticleViewSet,
    basename='stockagepartnerarticle'
)
router.register(r'tractor', carviews.TractorViewSet, basename='tractor')
router.register(r'trailer', carviews.TrailerViewSet, basename='trailer')
router.register(r'depot', cviews.DepotViewSet, basename='depot')
router.register(
    r'stockagepartner',
    cviews.StockagePartnerViewSet,
    basename='stockagepartner'
)
router.register(
    r'transfer',
    cviews.TransferViewSet,
    basename='transfer'
)
router.register(
    r'sale',
    cviews.SaleViewSet,
    basename='sale'
)

urlpatterns = [
    path('', include(router.urls)),
]
