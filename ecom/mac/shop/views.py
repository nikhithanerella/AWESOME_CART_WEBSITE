from django.shortcuts import render,HttpResponse,redirect
from shop.models import Product,Contact,Orders,UpdateOrders,categories
from math import ceil
import json
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth import authenticate, login as logins,logout
from django.contrib.auth.models import User
#from django.views.decorators.csrf import csrf_exempt
#from shop.paytm import checksum
#MERCHANT_KEY=""
# Create your views here.
@login_required(login_url='login')
def shop(request):
    print(f"User is logged in: {request.user.username}")
    category=categories.objects.all()
    allpods=[]
    catprods=Product.objects.values('category','product_id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        product_chunk = [prod[i:i + 4] for i in range(0, n, 4)]
    # Create chunks of 3 products for each slide
        allpods.append({
            'category': cat,
            'product_chunk': product_chunk,
        })
    params = {
    'allpods': allpods,
      # Send the chunks to the template
    'category':category,
    'user' :request.user.username,
    }
    return render(request, 'index/shops.html', params)

def about(request):
    return render(request,'index/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address','')
        state=request.POST.get('state','')
        city=request.POST.get('city','')
        zip=request.POST.get('zip','')
        email=request.POST.get('email','')
        contact=Contact(name=name,phone=phone,address=address,state=state,city=city,zip=zip,email=email)
        contact.save()
    return render(request,'index/contact.html')

def searchMatch(query,item):
    if query in item.product_name or query in item.category or query in item.desc:
       return True
    else:
        return False
def search(request):
    msg=False
    query=request.GET.get('search')
    allpods=[]
    catprods=Product.objects.values('category','product_id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        product_chunk = [prod[i:i + 4] for i in range(0, n, 4)]
    # Create chunks of 3 products for each slide
        if len(prod)>0:
            allpods.append({
                'category': cat,
                'product_chunk': product_chunk,
            })
    if allpods != []:
        msg=False
    else:
        msg=True
    params = {
    'allpods': allpods,
    'msg':msg,
    'user':request.user.username,
    }
    print(params)
    return render(request, 'index/search.html', params)


def productview(request,id):
    product=Product.objects.filter(product_id=id)
    print(product)
    return render(request,'index/productview.html',{'pro':product[0]})


def tracker(request):
        # If not a GET request, return an error
        if request.method=='POST':
            email=request.POST.get('email','')
            orderId=request.POST.get('orderid','')
            try:
                order=Orders.objects.filter(order_id=orderId,email=email)
                if len(order)>0:
                    update=UpdateOrders.objects.filter(order_id=orderId)
                    updates=[]
                    for item in update:
                        updates.append({'text':item.update_desc,'time':item.timestamp})
                        response=json.dumps([updates,order[0].items_json],default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{}')
        
            except Exception as e:
                return HttpResponse('{}')
            

        return render(request,'index/tracker.html')

def orderTracker(request):
    if request.method == 'GET':
        # Extract order_id and email from the URL parameters
        order_id = request.GET.get('orderid')
        email = request.GET.get('email')
        
    return render(request,'index/orderTracker.html',{'email': email, 'orderid': order_id})

def checkout(request):
    product=Product.objects.all()
    if request.method=='POST':
        items_json=request.POST.get('items_json','')
        amount=request.POST.get('amount')
        name=request.POST.get('name','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address','')
        state=request.POST.get('state','')
        city=request.POST.get('city','')
        zip=request.POST.get('zip','')
        email=request.POST.get('email','')
        order=Orders(items_json=items_json,amount=amount,name=name,phone=phone,address=address,state=state,city=city,zip=zip,email=email)
        order.save()
        update=UpdateOrders(order_id=order.order_id,update_desc="the order has been placed")
        update.save()
        thank=True
        id=order.order_id
        #request paytm to transfer the amount to your account after payment by user
        # params_dict={
            
        #     "MID": "VMLsp333374331769871",          # Your Paytm Merchant ID
        #     "ORDER_ID": str(order.order_id),        # Unique order ID
        #     "CUST_ID": email,      # Unique customer ID
        #     "TXN_AMOUNT": str(amount),                # The amount to be charged
        #     "WEBSITE": "WEBSTAGING",      # Your Paytm website URL
        #     "CHANNEL_ID": "WEB",                # Payment channel type (WEB for website)
        #     "INDUSTRY_TYPE_ID": "Retail",       # Industry type, example: Retail
        #     "CALLBACK_URL": "https://127.0.0.1:8000/shop/handlerequest",  # URL to handle the response
        # }
        #print(params_dict)
        #params_dict['CHECKSUMHASH']=checksum.generate_checksum(params_dict,MERCHANT_KEY)
        return render(request,'index/checkout.html',{'thank':thank,'id':id,'user':request.user.username})

        
    return render(request,'index/checkout.html',{'product':product})


# @csrf_exempt
# def handlerequest(request):
#     #paytm will send post request here
#     form=request.POST
#     response_dict={}
#     for i in form.keys():
#         response_dict[i]=form[i]
#         if i=="CHECKSUMHASH":
#             checksum=form[i]
#     verify=checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
#     if verify:
#         if response_dict['RESPONSE']=='01':
#             print('order successful')
#         else:
#             print("order was not succesful because"+response_dict['RESPONSE'])
#     return render(request,'shop/paymentstatus.html',{'response':response_dict})


def myorders(request):
    orders=Orders.objects.all()
    lyst=[]
    for order in orders:
        # Check if the items_json is a string and not empty
        if order.items_json:
            try:
                # Clean the string (remove spaces) and parse it into a dictionary
                cleaned_string = order.items_json.replace(" ", "")
                order.items_json = json.loads(cleaned_string)  # This will throw an error if it's invalid
            except json.JSONDecodeError:
                # If there's a decoding error, set items_json to an empty dictionary or handle appropriately
                order.items_json = {}
        else:
            # If items_json is empty or None, set it to an empty dictionary
            order.items_json = {}
    # for one in orders:
    #     # Ensure order.items_json is a dictionary before using .items()
    #     if isinstance(one.items_json, dict):
    #         for item_key, item_value in one.items_json.items():
    #             lyst.append(item_value[4])  # Convert the item_value (which is a list) to a list
    #     else:
    #         print(f"Order ID {one.order_id} has invalid items_json: {one.items_json}")
    # print(lyst)
    required=[]
    for order in orders:
        for id in order.items_json:
            flag=0
            person=order.items_json[id][4]
            if request.user.username==person:
               flag=1
        if flag:
            required.append(order)
    return render(request,'index/myorders.html',{'user':request.user.username,'mine':required,})

def wishlist(request):
    user=request.user.username
    return render(request,'index/wishlist.html',{'user':user})


def signup(request):
    success=False
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the user but don't save to the database yet
            user = form.save(commit=False)
            # Hash the password
            user.set_password(form.cleaned_data['password'])
            # Save the user to the database
            user.save()
            success=True
            logout(request)
            # Log the user in immediately after signup
            logins(request, user)
            return redirect('/')  # Redirect to home page after successful signup
        else:
              error=SignupForm()
              return render(request,'index/signup.html',{'error':"Something wrong"})
    else:
        form=SignupForm()
    return render(request, 'index/signup.html', {'form': form})
    
def login(request):
    success=True
    print("login")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            logins(request, user)
            return redirect('/')  # Redirect to the homepage or dashboard
        else:
            return render(request,'index/login.html',{'error':"Invalid credentials",'success':False})
    return render(request, 'index/login.html')  # Render the login form for GET requests

def logouts(request):
    logout(request)
    return redirect('login')   