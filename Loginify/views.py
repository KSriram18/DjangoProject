from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from  . models import UserDetails
from django.views.decorators.csrf import csrf_exempt
from  . serializer import UserSerializer
import json
# Create your views here.

def signup(request):
    if request.method=='GET':
        return render(request, 'Loginify/signup.html')
    elif request.method=='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            all_data=UserDetails.objects.all() 
            data1= UserSerializer(all_data,many=True)
            serializer_data=data1.data[:]
            for value in serializer_data:
                if value["email"]==email:
                    return JsonResponse({'error': 'This email is already registered.'}, status=400)
            serialize_data=UserSerializer(data={"Username":username, "Email":email, "Password":password})
            if serialize_data.is_valid(): 
                UserSerializer.save(serialize_data)
                return redirect('confirmation')
            else: 
                return JsonResponse(serialize_data.errors,status=400) 
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
        
def login(request):
    if request.method=='GET':
        return render(request, 'Loginify/login.html')
    elif request.method=='POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_data=UserDetails.objects.get(pk=username)
            serializer_data=UserSerializer(user_data) 
            if (serializer_data["Password"]==password):
                return redirect("success")
            else:
                return JsonResponse({"error":"Wrong Password"},status=404) 
        except UserDetails.DoesNotExist: 
            return JsonResponse({"error":"User not found"},status=404) 
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)


       
def confirmation(request):
    if request.method=='POST':
        return redirect("login")
    return render(request, 'Loginify/confirmation.html')

def success(request):
    return HttpResponse('Form submission successful')

def getalluserdetails(request):
    if request.method == "GET": 
        try: 
            all_data=UserDetails.objects.all()  
            serializer_data= UserSerializer(all_data,many=True) 
            return JsonResponse(serializer_data.data,safe=False) 

        except Exception as e: 
            return JsonResponse({"error":str(e)},status=500)
        
def singleuserusingbyemail(request,pk):
    if request.method == "GET":
        try: 
            user_data=UserDetails.objects.get(pk=pk) 
            serializer_data=UserSerializer(user_data) 
            return JsonResponse({ "data":serializer_data.data },status=200)
        except UserDetails.DoesNotExist: 
            return JsonResponse({"error":"User not found"},status=404) 
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)
@csrf_exempt        
def UpdateUserdetails(request,pk):
    if request.method == "PUT": 
        try: 
            input_data=json.loads(request.body) 
            user=UserDetails.objects.get(pk=pk) 
            serializer_data=UserSerializer(user,data=input_data) 
            if serializer_data.is_valid(): 
                serializer_data.save() 
                return JsonResponse({"message":"Data updated successfully"},status=200) 
            else: 
                return JsonResponse(serializer_data.errors,status=400) 
        except UserDetails.DoesNotExist: 
            return JsonResponse({"error":"User not found"},status=404)
        except Exception as e: 
            return JsonResponse({"error":str(e)},status=500)
        
@csrf_exempt
def deleteUserdetails(request,pk):
    if request.method == "DELETE": 
        try: 
            all_data=UserDetails.objects.all() 
            data1= UserSerializer(all_data,many=True)
            serializer_data=data1.data[:]
            for value in serializer_data:
                if value["Email"]==pk:
                    user=UserDetails.objects.get(pk=value["Username"]) 
                    user.delete() 
                    return JsonResponse({"message":"Data deleted successfully"},status=204) 
            return JsonResponse({"error":"User not found"},status=404)
        except Exception as e: 
            return JsonResponse({"error":str(e)},status=500)






