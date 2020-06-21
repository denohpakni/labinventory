from inventory import views

app_name = ""
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^orders/$', views.OrdersView.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', views.OrderView.as_view(), name='order'),
    url(r'^items/(?P<pk>\d+)/$', views.ItemView.as_view(), name='item')
]
