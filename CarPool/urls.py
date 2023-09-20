from django.urls import path
from . import views

urlpatterns = [
    path("", views.carpool, name="carpool"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("loginpass", views.loginpass, name="loginpass"),
    path("logindrive", views.logindrive, name="logindrive"),
    path("registerpass", views.registerpass, name="registerpass"),
    path("registerdrive", views.registerdrive, name="registerdrive"),
    path("driver_page/<int:did>", views.driver_page, name="driver_page"),
    path("driver_page/view_profile/delete_d/<int:did>", views.delete_d, name="delete_d"),
    path("driver_page/view_orders/<int:did>", views.view_orders, name="view_orders"),
    path("driver_page/view_profiled/<int:d>", views.view_profiled, name="view_profiled"),
    path("driver_page/view_orders/cancel_accept/<int:i>,<int:d>", views.cancel_accept, name="cancel_accept"),
    path("driver_page/view_orders/completed/<int:i>,<int:d>", views.completed, name="completed"),
    path("passenger_page/delete_p/<int:pid>", views.delete_p, name="delete_p"),
    path("passenger/<int:pid>", views.passenger_page, name="passenger_page"),
    path("passenger/requestride/<int:p>", views.requestride, name="requestride"),
    path("passenger/view_profile/<int:p>", views.view_profile, name="view_profile"),
    path("passenger/view_profile/delete_p/<int:p>", views.delete_p, name="delete_p"),
    path("passenger/view_requests/<int:pid>", views.view_requests, name="view_requests"),
    path("passenger/view_requests/cancel_orders/<int:i>,<int:p>", views.cancel_orders, name="cancel_orders"),
    path("passenger/view_requests/editreq/<int:i>,<int:p>", views.editreq, name="editreq"),
    path("passenger/view_requests/editreq/saveedit/<int:i>,<int:p>", views.saveedit, name="saveedit"),
    path("driver_page/acceptorder/<int:i>,<int:d>", views.acceptorder, name="acceptorder"),
]