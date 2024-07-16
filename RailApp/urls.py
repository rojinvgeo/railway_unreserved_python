"""
URL configuration for RailProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from .import views
# from .views import create_payment
from .views import payment_view, payment_success_view 



urlpatterns = [
path('',views.index,name='index'),
path('contact',views.contact,name='contact'),
path('signup',views.signup,name='signup'),
path('accounts/login/',views.login_view,name='login'),
 path('ForgotPassword', views.ForgotPassword, name="ForgotPassword"),
 path('PasscodeEnter', views.PasscodeEnter, name="PasscodeEnter"),
 path('PasscodeConfirmation', views.PasscodeConfirmation, name="PasscodeConfirmation"),
 path('PasswordReset/<str:uname>', views.PasswordReset, name="PasswordReset"),
#ath('PasswordReset/<int:id>', views.PasswordReset, name="PasswordReset"),
#path('change_password',views.change_password,name='change_password'),
path('send_email/', views.Email_Send, name='send_email'),
path('userhome',views.userhome,name='userhome'),
path('booking_details/',views.booking_details,name='booking_details'),
path('faq',views.faq,name='faq'),
path('terms_and_conditions',views.terms_and_conditions,name='terms_and_conditions'),
path('adminlogin',views.adminLogin,name='adminlogin'),
path('adminhome',views.adminHome,name='adminhome'),
path('add_train',views.add_train,name='add_train'),
path('delete_train/<int:id>',views.delete_train,name='delete_train'),
path('delete_customer/<int:id>',views.delete_customer,name='delete_customer'),
path('edit_train/<int:id>',views.edit_train,name='edit_train'),
path('train_search',views.train_search,name='train_search'),
path('add_cust',views.add_cust,name='add_cust'),
path('edit_user/<int:id>',views.edit_user,name='edit_user'),
path('edit_for_user/',views.edit_for_user,name='edit_for_user'),
path('delete_user/<int:id>',views.delete_user,name='delete_user'),


# path('register_success',views.registration_success,name='register_success'),
 path('tickets/<int:id>',views.tickets, name='tickets'),
  path('forgot_password/',views.forgot_password, name='forgot_password'),


path('book_train/<int:id>',views.book_train,name='book_train'),
path('payment/<int:ticket_id>',views.payment_view, name='payment'),
# path('payment', views.payment_view, name='payment'),
# path('payment/',views.payment_view, name='payment/'),
# path('ticketid/<int:ticket_id>/', views.ticket_id, name='ticket_id'),

# path('ticketid/',views.ticket_id,name='ticket_id'),
path('payment/success/', payment_success_view, name='payment_success'),

 
# path('createpayment/', create_payment, name='create_payment'),
# path('paymenthandler/',views.paymenthandler, name='paymenthandler'),
# path('payment/success/', process_payment, name='payment_success'),

#path('cnf',views.cnf,name='cnf'),

#path('initiate_payment/',initiate_payment, name='initiate_payment'),

path('customer_replay',views.customer_replay,name='customer_replay'),
path('Email_Send',views.Email_Send,name='Email_Send'),
path('senduser_complaint',views.senduser_complaint,name='senduser_complaint'),
path('customer_home',views.customer_home,name='customer_home'),


path('customer_login',views.customer_login,name='customer_login'),
path('usercomplaint_replay/<int:id>',views.usercomplaint_replay,name='usercomplaint_replay'),

path('admin_complaint',views.admin_complaint,name='admin_complaint'),
path('admin_replay/<int:id>',views.admin_replay,name='admin_replay'),

    path('logout_view', views.logout_view, name='logout_view'),
  path('add_station',views.add_station,name='add_station'),
path('addtickets',views.addtickets,name='addtickets'),
path('change_password/',views.change_password,name='change_password'),




]
 