from django.urls import path

from .views import (
    HomePageView,
    LocalNewsView, WorldNewsView, SubjectNewsView, SportNewsView, IqtisodiyotNewsView,
    ContactPageView,
    NewsCreateView, NewsUpdtaeView, NewsDeleteView,
    news_detail, admin_page, search_view,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('adminpage/', admin_page, name='admin_page'),

    # MUHIM: create/, edit/, delete/ — slug pattern DAN OLDIN turishi shart
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:slug>/edit/', NewsUpdtaeView.as_view(), name='news_update'),
    path('news/<slug:slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),

    path('contact/', ContactPageView.as_view(), name='contact-us'),
    path('Uzbekistan/', LocalNewsView.as_view(), name='Uzbekistan'),
    path('Jahon/', WorldNewsView.as_view(), name='Jahon'),
    path('Fan_texnika/', SubjectNewsView.as_view(), name='Fan_texnika'),
    path('Sport/', SportNewsView.as_view(), name='Sport'),
    path('Iqtisodiyot/', IqtisodiyotNewsView.as_view(), name='Iqtisodiyot'),
    path('searchresult/', search_view, name='search_results'),
]
