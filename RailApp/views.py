from telnetlib import LOGOUT
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import TrainForms,StationAddForms,TicketAddForm
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from .helpers import *
from django.conf import settings
from django.core.mail import send_mail













# Create your views here.

def index(request):
    return render(request,'index.html')


def contact(request):
    return render(request,'contact.html')

def signup(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        addr = request.POST.get('address')
        name = request.POST.get('name')
        uname = request.POST.get('username')
        age = request.POST.get('age')
        pwd = request.POST.get('password')
        phone=request.POST.get('phone')
        email = request.POST.get('email')
        
        user= userregister.objects.filter(uname=uname,email=email)
        if user.exists():
            messages.warning(request, 'username already exists')
            return redirect(signup)
        elif userregister.objects.filter(email=email).exists():
            messages.warning(request, 'email already exists')
            return redirect(signup)

        
        else:
            user=userregister( 
            file=file,
            addr=addr,
            name=name,
            uname=uname,
            age=age,
            pwd=pwd,
            email=email,

            phone=phone,)
            user.save()
        return redirect(login_view)     
    return render(request, 'signup.html')

           
        
def login_view(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        pwd = request.POST.get('pwd')
        check_user=userregister.objects.filter(uname=uname, pwd=pwd)

        if check_user:
            request.session['user']=uname
            return redirect(userhome)
        else:
            messages.warning(request,'Please Enter a Valid Username or Password...')
            return redirect(login_view)
    return render(request,'userlogin.html')


from django.core.mail import send_mail
import random
def forgot_password(request):
    if 'submit' in request.POST:
        uname=request.POST['username']
        mail=request.POST['email']
        g=login.objects.get(username=uname)
        if g is not None:
            a=random.randint(0000,9999)
            g.password=(str(a))
            g.save()
            send_mail('CREDITCARD FRAUD DETECTION', "YOUR NEW PASSWORD IS  -" +str(a), 'email@gmail.com',[mail], fail_silently=False)
            messages.info(request,"Password sent to your registered email address !!!")
            return redirect(login_view)
        else:
            print('error==========')
            messages.info(request,"Invalid Username or Email Adress!!!")
            return redirect(forgot_password)

    return render(request,'forgot_password.html')


# def ForgotPassword(request):
#     if request.method == "POST":
#         em = request.POST.get("email")
#         subject = "Password Reset"
#         msg = "Here is your reset link : http://127.0.0.1:8000/PasswordReset/ "
#         to = em
#         print(msg)
#         res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
#         if res == 1:
#             return HttpResponse("Mail sent")
#         else:
#             msg = "Mail could not sent"
#             return HttpResponse(msg)
#     return render(request, "ForgotPassword.html")

# def PasswordReset(request,id):
#     user = userregister.objects.get(id=id)
#     if request.method == 'POST':
#             new_password = request.POST.get('pwd')
#             conform_password=request.POST.get('con')
#             if new_password==conform_password:
#                 user.set_password(new_password)
#                 user.save()
#                 return HttpResponse("Updated")
#             return redirect(login_view)


passcode = random.randrange(100000, 1000000, 1)
def ForgotPassword(request):
    if request.method=="POST":
        em = str(request.POST.get("email"))
        global passcode
        subject = "Password Reset"
        msg = "Here is your passcode :" + str(passcode)
        to = em
        print(msg)
        res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
        if (res == 1):
            return render(request,"passcode.html")
        else:
            msg = "Mail could not sent"
            return HttpResponse(msg)
    return render(request,'ForgotPassword.html')

def PasscodeEnter(request):
    return render(request, "passcode.html")

def PasscodeConfirmation(request):
    if request.method == "POST":
        code = int(request.POST.get("code"))
        print("Code Entered:",code,"and type ->",type(code))
        print("Passcode:",passcode,"and type ->",type(passcode))
        if code == passcode:
            return render(request,'password_reset.html')
        else:
            return HttpResponse("Wrong Code")
    

def PasswordReset(request,uname):
    
    if request.method=='POST':
        uname=request.POST.get('uname')
        new_password=request.POST.get('pwd')
        confirm_password=request.POST.get('conform_password')
        # user = userregister.objects.get(uname=request.session['user'])
        
        user= userregister.objects.filter(uname=uname)
        if new_password != confirm_password:
            messages.warning(request, "your new password not match the confirm password !")
        else:
            user.pwd=new_password
            user.save()
            messages.success(request, "your password has been changed successfuly.!")
            return redirect('login_view')
    return render(request,'password_reset.html')

                    
            


   


def Email_Send(request):
    print("IN SEND MAIL")
    if request.method=="POST":
        em = str(request.POST.get("email"))
        global passcode
        subject = ""
        msg = "Hii, Thankyou for subscribing newletter from now on you will receive important informations and updates we will promise that we will never spam !  :"
        to = em
        print("ROJIN B4 RES")
        res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
        print("ROJIN:",res)
        if (res == 1):
            print('------------')
            return redirect(index)
        else:
            msg = "Mail could not sent"
            return HttpResponse(msg)




        # Authenticate user``
def userhome(request):    
    trains = Ticket.objects.all()
    messages=Complaint.objects.filter(user__name=request.session['user'])

    search_in = request.GET.get('q')
    search = request.GET.get('h')

    if search_in:
        trains = Ticket.objects.filter(destination_station__name__icontains=search_in,starting_station__name__icontains=search)
   
    context = {
        'trains':trains,
        'messages':messages,

        
    }
    return render(request,'userpage.html',context)





def edit_for_user(request):
    usr=userregister.objects.get(uname=request.session['user'])

      # Replace User with your user model
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        addr = request.POST['addr']
        age = request.POST['age']
        new_password = request.POST['pwd1']
        confirm_new_password = request.POST['pwd2']

        if new_password == confirm_new_password:
            usr.name = name
            usr.email = email
            usr.phone = phone
            usr.addr = addr
            usr.age = age
            usr.pwd = new_password
            usr.save()
            messages.success(request,'Sucsellfully updated')

            return redirect(userhome) 
        else: 
            new_password != confirm_new_password
            messages.error(request,'Passwords do not match. Please try again.')

       
        
    return render(request,'edit_profile_for_user.html',{'usr':usr})

# #def change_password(request,token):
#     context={}

#     user=userregister.objects.filter(forgot_pwd_token =token).first()
#     context={'user_id':user.user.id}

#     print(user)
#     new_password=request.POST.get('new_password')
#     confirm_password=request.POST.get('confirm_password')
#     user_id=request.POST.get('user_id')
#     return render(request,'user_changepassword.html',{context})
#     if user_id is None:
#         messages.success(request,'no user found')
#         return redirect(f'/change_password/{token}/')
    
#     if new_password!=confirm_password:
#         messages.success(request,'both should be equal')
#         return redirect(f'change_password/{token}/')
    
#     user=userregister.objects.get(id=user_id)
#     user.set_password(new_password)
#     user.save()
#     return redirect('login')


# #def forgot_password(request):
#     if request.method=='post':
#         uname=request.POST.get('uname')
#         if not userregister.objects.filter(uname=uname).first():
#             messages.success(request,'no user found with this username.')
#             print('++++++++++++++++++++++')
#             return redirect('/forgot-password/')
#         return render(request,'forgotPass.html')
#     user_obj=userregister.objects.get(uname=uname)
#     token=str(uuid.uuid4())
#     user=userregister.objects.get(user=user)
#     user.forgot_pwd_token=token
#     user.save()
#     send_forgot_password_mail(user_obj,token)
#     messages.success(request,'An email is sent.')
#     return redirect('/forgot-password/')
    


def faq(request):
    return render(request,'helpcenter-faqs.html')

def terms_and_conditions(request):
    return render(request,'terms_and_conditions.html')

def contact(request):
    return render(request,'contact.html')

def adminLogin(request):
    if request.method=="POST":
        uname=request.POST.get('uname')
        pwd=request.POST.get('pwd')
        if uname=='admin' or uname=='ADMIN' or uname=='Admin' and pwd=='1234':
            request.session['user']=uname
            return redirect(adminHome)
        else:
            return HttpResponse('PLEASE ENTER A VALID USERNAME AND PASSWORD')
    else:
        return render(request,'adminsignin.html')
        print('333')
    
        
def adminHome(request):
    obj=userregister.objects.all()
    train=Train.objects.all()
    customer =Customer.objects.all()
    book=Booking.objects.all()
    customer_replay=ComplaintAdmin.objects.all()
    ticket = Booking.objects.all()



    context = {
        'obj': obj,
        'train':train,
        'customer':customer,
        'book':book,
        'customer_replay':customer_replay,
        'ticket':ticket
        
    }
    return render(request,'adminhome.html',context)



def add_train(request):
    if request.method == 'POST':
        form = TrainForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect(adminHome)
    else:
        form = TrainForms()    
    return render(request, 'train.html',{'form':form})
    
def delete_train(request,id):
    # Retrieve the train object from the database
    train = Train.objects.get(id=id)

    train.delete()
    messages.success(request,'deleted')
    return redirect(adminHome)   

def edit_train(request, id):
    train = Train.objects.get(id=id)

    if request.method == 'POST':
        form = TrainForms(request.POST, instance=train)
        if form.is_valid():
            form.save()
            return redirect(adminHome)  
    else:
        form = TrainForms(instance=train)
    return render(request, 'edittrain.html', {'train': train})

def train_search(request):
    if request.method == 'GET':
        train_number = request.GET.get('train_number')
        if train_number:
            train = Train.objects.filter(train_number=train_number).first()
            return render(request, 'train_details.html', {'train': train})
    return render(request, 'search_train.html')

def add_cust(request):
    if request.method=='POST':
        cust_id=request.POST.get('id')
        name=request.POST.get('name')
        password=request.POST.get('password')
        customer=Customer(cust_id=cust_id,name=name,password=password)
        customer.save()
        return redirect(adminHome)
    return render (request,'add_customer.html')

def delete_customer(request,id):
    # Retrieve the train object from the database
    customer = Customer.objects.get(id=id)

    customer.delete()
    messages.success(request,'deleted')
    return redirect(adminHome)

def edit_user(request,id):
    user=userregister.objects.get(id=id)

    if request.method=='POST':
        user.name=request.POST['name']
        user.age = request.POST['age']
        user.email = request.POST['email']
        user.phone = request.POST['phone']
        user.addr = request.POST['addr']
        user.birth=request.POST['birth']

        user.save()
        return redirect(adminHome)
    return render(request, 'edit_user.html', {'user': user})

def delete_user(request,id):
    user= userregister.objects.get(id=id)
    user.delete()
    messages.success(request,'deleted')
    return redirect(adminHome)  


# ticket_booking/views.py


  



    
# def book_train(request,id):
#     ticket= Ticket.objects.get(id=id)

#     if request.method=='POST':
#         userid = userregister.objects.get(uname=request.session['user'])
#         booking=Booking(ticket=ticket,user=userid)
#         ticket_price_usd=100
#         conversion_rate=75
#         ticket_price_inr=ticket_price_usd * conversion_rate

#         ticket={
#             'ticket_price_inr':ticket_price_inr

#         }
       
#         print(booking)
#         booking.save()
#         return HttpResponse('<script>alert(" successfully sended we will reach you soon ");window.location="/userhome"</script>')
#     #return render(request, 'book.html',{'ticket':ticket})
#     return render(request, 'book.html',{'ticket':ticket})
# return render(request, 'book.html', context=context)


#payment testing

# client=razorpay.Client (auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))



#integrated Razorpay payment
# def payment_success(request):
#     return render (request, 'success.html')

def book_train(request,id,):
    ticket= Ticket.objects.get(id=id)
    if request.method=='POST':
        ticket= Ticket.objects.get(id=id)
        userid = userregister.objects.get(uname=request.session['user'])
        book= Booking(user=userid,ticket=ticket)
        book.save()
        print(ticket)
    return render(request, 'book.html',{'ticket':ticket})


#payment testing from github
import razorpay
client=razorpay.Client (auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

def initiate_payment(amount,currency='INR'):
    data={
    'amount':int(amount)* 100,
    'currency':currency,
    'payment_capture':'1'
    }
    response=client.order.create(data=data)
    return response['id']


def payment_view(request,ticket_id):
   ticket = Ticket.objects.get(pk=ticket_id)
   amount = ticket.amount  # Set the amount dynamically or based on your requirements
   order_id = initiate_payment(amount)
   context = {
       'order_id': order_id,
       'amount': amount,
       'ticket_id':ticket_id
       
   }
   return render(request, 'payment.html', context)

def payment_success_view(request):
   order_id = request.POST.get('order_id')
   payment_id = request.POST.get('razorpay_payment_id')
   signature = request.POST.get('razorpay_signature')
   params_dict = {
       'razorpay_order_id': order_id,
       'razorpay_payment_id': payment_id,
       'razorpay_signature': signature
   }
   try:
       client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
       
       return render(request, 'payment_success.html')
   except razorpay.errors.SignatureVerificationError as e:
       
    
       # Payment signature verification failed
       # Handle the error accordingly
    
         return HttpResponse('<script>alert(" your ticket is successfully booked hppy journey");window.location="/userhome"</script>')
   





# def initiate_payment(ticket_id,amount,currency='INR'):
#     ticket = Ticket.objects.get(pk=ticket_id)
#     amount = ticket.amount
#     data={
#     'amount':int(amount) * 100,
#     'currency':currency,
#     'payment_capture':'1'
#     }
#     response=client.order.create(data=data)
#     return response['id']
#  #testing 
# def payment_view(request,ticket_id):
#     ticket = Ticket.objects.get(pk=ticket_id)
#     amount = ticket.amount  # Set the amount dynamically or based on your requirements
#     order_id = initiate_payment(ticket_id, amount)  # Pass the amount to initiate_payment
#     context = {
#         'order_id': order_id,
#         'amount': amount,  # Pass the amount to the template
#         'ticket_id': ticket_id
#     }
#     return render(request, 'payment.html', context,)
    


# def payment_view(request,ticket_id):
#    ticket = Ticket.objects.get(pk=ticket_id)
#    print(ticket_id)
#    amount = ticket.amount  # Set the amount dynamically or based on your requirements
#    order_id = initiate_payment(ticket_id)
#    context = {
#        'order_id': order_id,
#        'amount': amount,
#        'ticket_id':ticket_id
#    }
#    return render(request, 'payment.html', context)

#testing
# def ticket_id(request, ticket_id):
#     return payment_view(request, ticket_id, amount=Ticket.objects.get(pk=ticket_id).amount)

# def ticket_id(request, ticket_id):
#     ticket = Ticket.objects.get(pk=ticket_id)
#     return payment_view(request, ticket_id)  # Pass the ticket_id instead of the ticket object


# def ticket_id(request,ticket_id):
#     # Retrieve the ticket_id, either from the request or any other source
#     ticket_id = Ticket.objects.get(pk=ticket_id)
#     return payment_view(request, ticket_id)


# def payment_success_view(request):
#    order_id = request.POST.get('order_id')
#    payment_id = request.POST.get('razorpay_payment_id')
#    signature = request.POST.get('razorpay_signature')
#    params_dict = {
#        'razorpay_order_id': order_id,
#        'razorpay_payment_id': payment_id,
#        'razorpay_signature': signature
#    }
#    try:
#        client.utility.verify_payment_signature(params_dict)
#        # Payment signature verification successful
#        # Perform any required actions (e.g., update the order status)
       
#        return render(request, 'payment_success.html')
#    except razorpay.errors.SignatureVerificationError as e:
       
    
#        # Payment signature verification failed
#        # Handle the error accordingly
    
#          return HttpResponse('<script>alert(" your ticket is successfully booked hppy journey");window.location="/userhome"</script>')



def tickets(request):
    booking= Booking.objects.filter(user__uname=request.session['user'])   
    
    context = {
      'booking':booking
   }
    return render(request,'tickets.html',context) 
       
    



def booking_details(request):
    booking= Booking.objects.filter(user__uname=request.session['user'])   
    
    context = {
      'booking':booking
   }
    return render(request,'booking_details.html',context) 




def senduser_complaint(request):
     if request.method=='POST':
        complaint=request.POST.get('complaint')
        status= 'pending'
        userid = userregister.objects.get(uname=request.session['user'])
        complaints=Complaint(complaint=complaint,status=status,user=userid)
        complaints.save()
        return HttpResponse('<script>alert(" successfully sended we will reach you soon ");window.location="/userhome"</script>')
     return render(request,'contact.html')

def senduser_complaint(request):
    if request.method=='POST':
        complaint=request.POST.get('complaint')
        status= 'pending'
        userid = userregister.objects.get(uname=request.session['user'])

        complaints=Complaint(complaint=complaint,status=status,user=userid)
        complaints.save()
        return HttpResponse('<script>alert(" successfully sended we will reach you soon ");window.location="/userhome"</script>')

    return render(request,'contact.html')

def customer_replay(request):
    return render (request,'customer_support_replay.html')


def admin_complaint(request):
    if request.method=='POST':
        complaint=request.POST.get('complaint')
        status= 'pending'
        complaints=ComplaintAdmin(complaint=complaint,status=status)
        complaints.save()
        return HttpResponse('<script>alert(" successfully sended we will reach you soon ");window.location="/adminhome"</script>')

    return render(request,'admin_complaint.html')


def customer_replay(request):
    return render (request,'customer_support_replay.html')

def customer_home(request):
    messages = Complaint.objects.all()
    complaint = ComplaintAdmin.objects.all()
    context ={
        'messages':messages,
        'complaint':complaint

    }

    return render(request,'customer_page.html',context)




#customer section


def customer_login(request):
    if request.method=='POST':
        uname=request.POST.get('id')
        pwd = request.POST.get('password')
        customer=Customer.objects.filter(cust_id=uname, password=pwd)

        if customer:
            request.session['customer']=uname
            return redirect(customer_home)
        else:
            return HttpResponse('Please Enter a Valid Username or Password...')
    return render(request,'customer_login.html')


def usercomplaint_replay(request, id):
    message= Complaint.objects.get(id=id)

    if request.method == 'POST':
        message.complaint = request.POST['text']
        message.status = "replied"       
        message.save()
        return HttpResponse('<script>alert(" successfully sended we will reach you soon ");window.location="/customer_home"</script>')
    return render(request, 'customer_replay.html', {'message': message})


# def admin_complaint(request):
#     if request.method=='POST':
#         complaint=request.POST.get('complaint')
#         status= 'pending'
#         customer = Customer.objects.get(cust_id=request.session['customer'])

#         complaints=ComplaintAdmin(complaint=complaint,status=status,customer=customer)
#         complaints.save()
#         return HttpResponse('<script>alert(" successfully sended we will reach you soon ");window.location="/adminhome"</script>')
#     return render(request,'admin_complaint.html')

def admin_complaint(request):
    if request.method=='POST':
        complaint=request.POST.get('complaint')
        status= 'pending'
        complaints=ComplaintAdmin(complaint=complaint,status=status)
        complaints.save()
        return HttpResponse('<script>alert(" successfully sended we will reach you soon ");window.location="/adminhome"</script>')

    return render(request,'admin_complaint.html')

def admin_replay(request, id):
    message= ComplaintAdmin.objects.get(id=id)
    if request.method == 'POST':
        message.complaint = request.POST['text']
        message.status = "replied"       
        message.save()

        return redirect(customer_home)
    return render(request, 'admin_replay.html', {'message': message})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')

def add_station(request):
    if request.method == 'POST':
        form = StationAddForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect(adminHome)  # Redirect to a success page or another view
    else:
        form = StationAddForms()
    return render(request, 'add_station.html', {'form': form})

def addtickets(request):
    if request.method == 'POST':
        form = TicketAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(adminHome)  # Redirect to a success page or another view
    else:
        form = TicketAddForm()
    return render(request, 'addtickets.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Verify if the new password and confirm_new_password match
        if new_password == confirm_new_password:
            user = userregister.objects.get(uname=request.session['user'])
            if not user.check_password(current_password):
                messages.warning(request, "your old password is not correct!")
            else:
                if new_password != confirm_new_password:
                    messages.warning(request, "your new password not match the confirm password !")

                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "your password has been changed successfuly.!")
                    return redirect('/')
    return render(request, 'change_password.html')