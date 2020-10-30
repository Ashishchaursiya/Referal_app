from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
import random ,string
from .models import extenduser
from django.contrib.auth.decorators import login_required
import razorpay
from .models import Order
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def Signin(request):
    return render(request,'login.html')

def Register(request):
    return render(request,'signup.html')    

def get_random(size):
    letters=string.ascii_letters
    result=''.join(random.choice(letters) for i in range(size))
    return result


@login_required(login_url='/login/')
def showdata(request):
    datas=extenduser.objects.filter(user=request.user)
    return render(request,'profile.html',{'data':datas})


def Signup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['pass']
        password1=request.POST['pass1']
         
        if password==password1:
            #now we check user exist or not
            try:
                user=User.objects.get(username=username)
                return render(request,'signup.html',{"error":"username already taken",'check':'edr5'}) 
            except User.DoesNotExist:
                myuser=User.objects.create_user(username,email,password)
                referal=get_random(8)+str(username)
                newextenduser=extenduser(referal=referal,user=myuser)
                newextenduser.save()
                myuser.first_name=fname
                myuser.last_name=lname
                myuser.save()
                messages.success(request,"account successful created")
                auth.login(request,myuser,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/accounts/Sign_page') 

            

        else:
            return render(request,'signup.html',{"error":"password not match",'check':'ert'})   
         
         
    else:
        return HttpResponse("404 not found")  


def Login(request):
    if request.method=='POST':
        uname=request.POST['username']
        pswd=request.POST['pass']  
        user=auth.authenticate(username=uname,password=pswd) 
        if user is not None:
            auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            
            return redirect('profile/')
        else:
            
            return render(request,"login.html",{'error':'invalid username or password','check':'23er'}) 
    else:
        return HttpResponse("404 not found")   

 
def Logout(request):
    auth.logout(request) 
    return redirect("/")  

 
             

 
@login_required(login_url='/login/')
def Buy(request):
   
    return render(request,'payment.html')



@login_required()
def checkout(request):
     if request.method=='POST':
        upi=request.POST['upi']
        referal=request.POST['referal']
        amount=int(request.POST['amount'])
        phone=request.POST['phone']
        client=razorpay.Client(auth=("rzp_test_fLkLtmNTfcNSbw","ADeYiLVJ8V1W9BR7blXffRkI"))
        payment=client.order.create({'amount':amount*100,'currency':'INR','payment_capture':'1'})
    
        order=Order(phone=phone,UPI_ID=upi,plan=str(amount),Refer_by=referal,payment_id=payment['id'])
        order.save()
        return render(request,'payment.html',{'payment':payment,'again':'yuhj','referal':referal})

       
@csrf_exempt
def success(request,referal):
    if request.method=="POST":
        data=request.POST
        order_id=''
        for key,val in data.items():
            if key == 'razorpay_order_id':
                order_id=val
                break
        user=Order.objects.filter(payment_id=order_id).first() 
        user.paid=True
        user.save()
        try:
            profit_user=extenduser.objects.filter(referal=referal).first()
            profit_user.no_referal=profit_user.no_referal+1
            profit_user.save()
        except:
            return HttpResponse("<h1>sorry referal id is wrong <h1>")    
        
        
        

    return render(request,'success.html')      