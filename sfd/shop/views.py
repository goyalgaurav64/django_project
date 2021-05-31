# from sfd.shop.models import Product
from django.db.models import query
from django.shortcuts import render
from django.http import HttpResponse
from . models import Product,Contact,Orders,OrderUpdate
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from sfd.Paytm import checksum
import json
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'



# Create your views here.
def index(request):
    products = Product.objects.all()
    # print(products)
    # n=len(products)
    # slides = n//4 + ceil((n/4)-(n//4))
    # params = {'no_of_slides':slides,'range':range(1,slides),'product':products}
    # allProds=[[products,range(1,slides),slides],[products,range(1,slides),slides]]
    allProds=[]
    catprods=Product.objects.values('category','id')
    # print(catprods)
    cats={item['category'] for item in catprods}
    # print(cats)
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        slides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,slides),slides])
    params={'allProds':allProds}
    return render(request,'shop/index.html',params)


def searchMatch(query,item):
    tags=set()
    tags.add(item.tag1.lower()+" "+item.prod_name.lower())
    tags.add(item.tag2.lower()+" "+item.prod_name.lower())
    tags.add(item.tag3.lower()+" "+item.prod_name.lower())
    tags.add(item.tag4.lower()+" "+item.prod_name.lower())
    tags.add(item.tag5.lower()+" "+item.prod_name.lower())
    tags.add(item.tag1.lower())
    tags.add(item.tag2.lower())
    tags.add(item.tag3.lower())
    tags.add(item.tag4.lower())
    tags.add(item.tag5.lower())
    print(tags)
    a=query.split()
    for query in a:
        if query in item.prod_Description.lower() or query in item.prod_name.lower() or query in item.category.lower() or query in item.subcategory.lower() or query in tags:
            return True
    return False


def search(request):
    query = request.GET.get('search')
    allProds=[]
    catprods=Product.objects.values('category','id')
    # print(catprods)
    cats={item['category'] for item in catprods}
    # print(cats)
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        slides = n//4 + ceil((n/4)-(n//4))
        if n!=0:
            allProds.append([prod,range(1,slides),slides])
    params={'allProds':allProds,"msg":""}
    if len(allProds)==0:
        return HttpResponse("<h1 class='text-danger'>No Search Results.Please Enter Relevant Item Name</h1>")
    return render(request,'shop/search.html',params)


def prodView(request,myid):
    cat=Product.objects.values("category","id")
    # Fetch the product using product ID
    product = Product.objects.filter(id=myid)
    # print(product)
    # print(product[0])
    # print(product[0].category)
    prodCat=product[0].category
    # print(prodCat)
    prodWithSameCat=Product.objects.filter(category=prodCat)
    # print(prodWithSameCat)

    return render(request,"shop/products.html",{'product':product[0],'allProdsofSameCat':prodWithSameCat})



def checkout(request):
    thank=False
    if request.method=="POST":
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        amount=request.POST.get('amt','')
        phone=request.POST.get('phone','')
        email=request.POST.get('email','')
        address=request.POST.get('address','') + " " + request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        order=Orders(items_json=items_json,amount=amount,name=name,phone=phone,email=email,address=address,city=city,state=state,zip_code=zip_code)
        order.save()
        

        #used for tracking . here we are pushing the request into the db.
        update = OrderUpdate(order_id=order.order_id,update_desc="Your Order has been placed")
        update.save()
        thank=True
        id=order.order_id
        params = {'thank':thank, 'id': id}
        # return render(request,'shop/checkout.html',params)
        
        # Request paytm to transfer the amount to your account after payment by user
        param_dict={
            'MID': 'WorldP64425807474247',
            'ORDER_ID': 'order.order_id',
            'TXN_AMOUNT': 'amount',
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH']=checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict':param_dict})
    return render(request,"shop/checkout.html")


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})



def track(request):
    if request.method=="POST":
        orderid=request.POST.get('orderid','')
        email=request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id=orderid,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderid)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    # print("---->",item.timestamp)
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"No Item"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,"shop/tracker.html")




def about(request):
    return render(request,'shop/about.html')



def contact(request):
    ct=False
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)  # right hand fields like name,desc are the
                                                                      # above ones and left ones are the database fields
        contact.save()
        ct=True
        params={'ct':ct}
        return render(request,"shop/contactus.html",params)
    return render(request,"shop/contactus.html")





def devop(request):
    return render(request,"shop/meetthedeveloper.html")



def testing(request):
    return render(request,"shop/test.html")