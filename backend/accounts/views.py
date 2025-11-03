#from django.shortcuts import render, redirect
#from .forms import CustomUserCreationForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()



#def register_view(request):
 #   if request.method == 'POST':
 #       form = CustomUserCreationForm(request.POST)
  #      if form.is_valid():
   #         user = form.save()
    #        login(request, user)
     #       return redirect('product_list')
   # else:
    #    form = CustomUserCreationForm()
    #return render(request, 'accounts/register.html', {'form': form})
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User created successfully!'}, status=201)
