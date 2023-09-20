from django.shortcuts import render, redirect
from CarPool.models import Passenger, Driver, Vehicle, Routes, RideRequest
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import json

# Create your views here.

def acceptorder(request,i, d):
    data = RideRequest.objects.get(id = i)
    drive = Driver.objects.get(dID = d)
    data.dID = drive
    vd = Driver.objects.filter(dID = d).values('vID')
    data.vID = Vehicle.objects.get(vID = vd[0]['vID'])
    data.status = 'Accepted'
    data.save()

    return redirect("/driver_page/{0}".format(d))
        


#New

def carpool(request):
    return render(request, "landing.html")

def register(request):
    all = Vehicle.objects.all().order_by('brand').values()
    dict = {
        'message':'',
        'all':all,
    }
    return render(request, 'register.html',dict)


def registerpass(request):
    all = Vehicle.objects.all().order_by('brand').values()
    dict = {}
    dict['all'] = all
    if request.method == 'POST':
        sID = request.POST['studentID']
        pname = request.POST['pName']
        pphone = request.POST['pPhone']
        ppass = request.POST['pPass']
        if Passenger.objects.filter(studentID=sID).exists() == True:
            dict['exist']='Account with student ID {0} already exists'.format(sID)
            return render(request, 'register.html', dict)
        else:
            if str(pphone).isnumeric() == False:
                dict['numeric'] = "Phone number must be numeric"
                return render(request, 'register.html', dict)
            else:
                data = Passenger(studentID = sID, pName = pname, pPhone=pphone,pPass = ppass)
                data.save()
                dict = {
                    'message':'Account Successfully Added'
                }
                return render(request, 'registered.html', dict)

def registerdrive(request):
    all = Vehicle.objects.all().order_by('brand').values()
    dict = {}
    dict['all'] = all
    if request.method == 'POST':
        sID = request.POST['studentID']
        dname = request.POST['dName']
        dphone = request.POST['dPhone']
        dpass = request.POST['dPass']
        Vid = request.POST['brand']
        plt = request.POST['plate']
        color = request.POST['carcolor']
        if Driver.objects.filter(studentID=sID).exists() == True:
            dict['exist']='Account with student ID {0} already exists'.format(sID)
            return render(request, 'register.html', dict)
        else:
            if str(dphone).isnumeric() == False:
                dict['numeric'] = "Phone number must be numeric"
                return render(request, 'register.html', dict)
            
            else:
                data = Driver(studentID=sID,dName=dname, dPhone=dphone,plate=plt,carcolor=color, vID=Vehicle.objects.get(vID=Vid),dPass=dpass)
                data.save()

                dict = {
                    'message':'Account Successfully Added'
                }
                return render(request, 'registered.html', dict)
        
        
def login(request):
    return render(request, 'login.html')


def loginpass(request):
    dict = {}
    if request.method == 'POST':
        sID = request.POST['studentID']
        ppass = request.POST['pPass']
        if Passenger.objects.filter(studentID=sID).exists() == True:
            pw = Passenger.objects.filter(studentID=sID).values('pPass')
            if pw[0]['pPass']==ppass:
                p = Passenger.objects.filter(studentID=sID).values('pID') 

                return redirect("/passenger/{0}".format(p[0]['pID']))
            else:
                dict['pw']='Wrong password'
                return render(request, 'login.html',dict)
        else:
            dict['exist'] = 'Account Does Not Exist'
            return render(request, 'login.html',dict)
        

def logindrive(request):
    dict = {}
    if request.method == 'POST':
        sID = request.POST['studentID']
        dpass = request.POST['dPass']
        if Driver.objects.filter(studentID=sID).exists() == True:
            pw = Driver.objects.filter(studentID=sID).values('dPass')
            if pw[0]['dPass']==dpass:
                d = Driver.objects.filter(studentID=sID).values('dID')
                return redirect("/driver_page/{0}".format(d[0]['dID']))
            else:
                dict['pw']='Wrong password'
                return render(request, 'login.html', dict)
        else:
            dict['exist'] = 'Account Does Not Exist'
            return render(request, 'login.html',dict)
        

def driver_page(request, did):
    data = Driver.objects.filter(dID = did).values('vID__capacity','dID', 'studentID', 'dName', 'dPhone', 'vID__brand', 'vID__CarModel', 'carcolor', 'plate')
    max = Driver.objects.filter(dID = did).values('vID__capacity')
    routes = Routes.objects.all().distinct()
    orders = RideRequest.objects.filter(Q(status='Pending') & Q(passengers__lte=max)).values('payment','passengers','pID__studentID','pID__pName','rID__rPrice','rID__rFrom','rID__rTo','status','time','date','id')
    temp = []
    for x in data:
        temp.append(x)
    dict = {'message':'Successful Log In','data':temp[0],'routes':routes,'orders':orders}    
    return render(request, 'driver.html',dict)

def passenger_page(request, pid):
    data = Passenger.objects.filter(pID = pid).values('pID', 'studentID', 'pName', 'pPhone')
    routes = Routes.objects.all().distinct()
    temp = []
    for x in data:
        temp.append(x)
    dict = {'message':'Successful Log In','data':temp[0],'routes':routes} 
    return render(request, 'passenger.html',dict)


def requestride(request,p):
    data = Passenger.objects.filter(pID = p).values('pID', 'studentID', 'pName', 'pPhone')
    routes = Routes.objects.all().distinct()
    temp = []
    for x in data:
        temp.append(x)
    dict = {}
    dict['data']=temp[0]
    dict['routes']=routes
    if request.method == 'POST':
        d = request.POST['date']
        t = request.POST['time']
        to = request.POST['rTo']
        fr = request.POST['rFrom']
        n = request.POST['passengers']
        e = ""
        c = ""
        if 'E-wallet' in request.POST:
            e = request.POST['E-wallet']
        if 'Cash' in request.POST:
            c = request.POST['Cash']
        r = Routes.objects.filter(Q(rTo=to ) & Q(rFrom=fr)).values('rID')
        if(e!="") and (c!=""):
            c = " or Cash"
        pay = e+c

        if(to==fr or int(n)<1):
            if(to==fr):
                dict['loc'] = 'Pick up location and Drop off location cannot be the same'
            
            if(int(n)<1):
                dict['num']='Number of passengers must be more than one'
            return render(request, 'passenger.html', dict)
        else:
            data =RideRequest(pID=Passenger.objects.get(pID=p),passengers = n, date=d,time=t,rID=Routes.objects.get(rID=r[0]['rID']), payment = pay)
            data.save()
            dict ={
                'message':'Request has been made','rID':r, 'p':p,
            }     
            return render(request, "order.html", dict)
        

def view_requests(request, pid):
    data = Passenger.objects.filter(pID =pid)
    req = RideRequest.objects.filter(pID = pid, status = 'Pending').values('payment','passengers', 'id','rID', 'rID__rFrom', 'rID__rTo', 'date', 'time', 'status', 'rID__rPrice')
    acpt = RideRequest.objects.filter(pID = pid, status = 'Accepted').values('payment','passengers','dID__dPhone', 'id','rID', 'rID__rFrom', 'rID__rTo', 'date', 'time', 'dID__dName','dID__plate', 'dID__carcolor', 'vID__brand', 'vID__CarModel', 'status', 'rID__rPrice')
    dict = {
        'req':req,'p':pid, 'acpt':acpt, 'data':data[0]
    }
    return render(request, "myorderp.html", dict)

def editreq(request, i, p):
    r = Routes.objects.all().values('rFrom', 'rID')
    have = []
    count = 0
    for x in r:
        if x['rFrom'] not in have:
            have.append(x['rFrom'])
    v = RideRequest.objects.filter(id = i).values('passengers', 'id','rID', 'rID__rFrom', 'rID__rTo', 'date', 'time', 'status', 'rID__rPrice')
    return render(request, "editOrder.html", {"data":v[0], "r":have , 'p':p})

def saveedit(request,i, p):
    r = Routes.objects.all().values('rFrom', 'rID')
    have = []
    for x in r:
        if x['rFrom'] not in have:
            have.append(x['rFrom'])
    v = RideRequest.objects.filter(id = i).values('passengers', 'id','rID', 'rID__rFrom', 'rID__rTo', 'date', 'time', 'status', 'rID__rPrice')
    routes = Routes.objects.all().distinct()
    dict = {}
    dict['routes']=routes
    if request.method == 'POST':
        d = request.POST['date']
        t = request.POST['time']
        to = request.POST['rTo']
        fr = request.POST['rFrom']
        n = request.POST['passengers']
        e = ""
        c = ""
        if 'E-wallet' in request.POST:
            e = request.POST['E-wallet']
        if 'Cash' in request.POST:
            c = request.POST['Cash']
        r = Routes.objects.filter(Q(rTo=to ) & Q(rFrom=fr)).values('rID')
        if(e!="") and (c!=""):
            c = " or Cash"
        pay = e+c
        if(to==fr or int(n)<1):
            if(to==fr):
                dict['loc'] = 'Pick up location and Drop off location cannot be the same'
            
            if(int(n)<1):
                dict['num']='Number of passengers must be more than one'
            return render(request, 'editOrder.html', dict)
        else:
            data = RideRequest.objects.filter(id = i)
            data.update(date = d, time  = t, rID = r, passengers =n, payment = pay)

            return redirect("/passenger/view_requests/{0}".format(p))

def cancel_orders(request, i, p):
    to_be_canceled = RideRequest.objects.get(id = i)
    to_be_canceled.delete()

    return redirect("/passenger/view_requests/{0}".format(p))



def view_profile(request, p):
    if request.method == 'POST':
        s = request.POST.get('studentID')
        n = request.POST.get('pName')
        pd = request.POST.get('pPhone')
        pw = request.POST.get('pPass')
        find =Passenger.objects.filter(pID = p)
        find.update(studentID =s, pName = n, pPhone = pd, pPass = pw)
        return redirect("/passenger/{0}".format(p))
    else:
        data = Passenger.objects.get(pID = p)
        name = data.pName.split(' ')[0]
        return render(request, "profilep.html", {"data":data, 'name':name})

def delete_p(request, p):
    data = Passenger.objects.get(pID = p)
    data.delete()

    return redirect("/login")

def view_orders(request, did):
    orders = RideRequest.objects.filter(dID = did, status = "Accepted").values('payment','id','passengers', 'pID__pPhone','pID__pName', 'pID__studentID', 'rID__rTo', 'rID__rFrom', 'date', 'time', 'rID__rPrice')
    dict = {
        'orders': orders, 'd':did, 
    }
    return render(request, "myorderd.html", dict)


def cancel_accept(request,i,d):
    orders = RideRequest.objects.filter(dID = d).values('id','passengers', 'pID__pPhone','pID__pName', 'pID__studentID', 'rID__rTo', 'rID__rFrom', 'date', 'time', 'rID__rPrice')
    data = RideRequest.objects.filter(id = i)
    data.update(status = "Pending", dID = "" )
    return redirect("/driver_page/view_orders/{0}".format(d))


def view_profiled(request, d):
    if request.method == 'POST':
        s = request.POST.get('studentID')
        n = request.POST.get('dName')
        p = request.POST.get('dPhone')
        c = request.POST.get('carcolor')
        pl = request.POST.get('plate')
        vi = request.POST.get('brand')
        find = Driver.objects.filter(dID = d)
        find.update(studentID =s, dName = n, dPhone = p, carcolor = c, plate = pl, vID=Vehicle.objects.get(vID=vi))
        return redirect("/driver_page/{0}".format(d))
    else:
        v = Vehicle.objects.all().values()
        data = Driver.objects.filter(dID = d).values('dPass','dName','vID','plate','studentID','dID', 'dName', 'dPhone', 'carcolor', 'vID__brand', 'vID__CarModel')
        name = data[0]['dName'].split(' ')[0]
        return render(request, "profiled.html", {"data":data[0], 'name':name , 'v':v})
    


def update_details_d(request,did):
    if request.method == 'POST':
        s = request.POST.get('studentID')
        n = request.POST.get('dName')
        p = request.POST.get('dPhone')
        c = request.POST.get('carcolor')
        pl = request.POST.get('plate')
        vi = request.POST.get('brand')
        find = Driver.objects.filter(dID = did)
        find.update(studentID =s, dName = n, dPhone = p, carcolor = c, plate = pl, vID = vi)
        return redirect("/driver_page/{0}".format(did))
    else:
        v = Vehicle.objects.all().values()
        data = Driver.objects.filter(dID = did).values('vID','plate','studentID','dID', 'dName', 'dPhone', 'carcolor', 'vID__brand', 'vID__CarModel')
        dict = {
            "data":data[0], 'v':v
        }
        return render(request, "updated.html", dict)
    


def delete_d(request, did):
    data = Driver.objects.get(dID = did)
    data.delete()

    return redirect("/login")


def completed(request, i, d):
    orders = RideRequest.objects.filter(dID = d).values('id','passengers', 'pID__pPhone','pID__pName', 'pID__studentID', 'rID__rTo', 'rID__rFrom', 'date', 'time', 'rID__rPrice')
    data = RideRequest.objects.filter(id = i)
    data.update(status = "Completed")
    return redirect("/driver_page/view_orders/{0}".format(d))