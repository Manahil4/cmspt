from django.urls import path
from .views import (
    home, sign_up, sign_in, sign_out, settings, change_password, custom_password_reset,
    portfolio_page, portfolio_item_detail, about_us, order_list, order_detail,
    start_discussion, discussion_detail, add_comment,
    designer_dashboard, client_dashboard, designer_specific_view, client_specific_view
)

urlpatterns = [
    path('', home, name='home'),
    path('sign_up/', sign_up, name='sign_up'),
    path('sign_in/', sign_in, name='sign_in'),
    path('sign_out/', sign_out, name='sign_out'),
    path('settings/', settings, name='settings'),
    path('change_password/', change_password, name='change_password'),
    path('custom_password_reset/', custom_password_reset, name='custom_password_reset'),
    path('portfolio/', portfolio_page, name='portfolio_page'),
    path('portfolio/<int:item_id>/', portfolio_item_detail, name='portfolio_item_detail'),
    path('about_us/', about_us, name='about_us'),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('discussions/', start_discussion, name='start_discussion'),
    path('discussions/<int:discussion_id>/', discussion_detail, name='discussion_detail'),
    path('add_comment/<int:discussion_id>/', add_comment, name='add_comment'),
    path('designer_dashboard/', designer_dashboard, name='designer_dashboard'),
    path('client_dashboard/', client_dashboard, name='client_dashboard'),
    path('designer_specific_view/', designer_specific_view, name='designer_specific_view'),
    path('client_specific_view/', client_specific_view, name='client_specific_view'),
]