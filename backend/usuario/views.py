from django.contrib.auth.models import Permission, User
from rest_framework.views import APIView
from rest_framework import permissions, serializers
from .models import CustomUser, Employee, Role
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import auth
from .serializers import UserSerializer, EmployeeSerializer, CustomUserSerializer

class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })

@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        #username = data['username']
        email = data['email']
        password = data['password']
        re_password  = data['re_password']
        employee = data['employee']
        role = data['role']

        """Validamos que las contraseñas sean iguales"""
        if password == re_password:
                """Validamos que el usuario no exista"""
                if User.objects.filter(username=email).exists():
                    return Response({ 'error': 'El correo ya existe' })
                else:
                    if len(password) < 6:
                        return Response({ 'error': 'La contraseña debe tener al menos 6 caracteres' })
                    else:
                        user = User.objects.create_user(username=email, password=password)
                        
                        user = User.objects.get(id=user.id)
                        emp= Employee.objects.get(id=employee)
                        rol=Role.objects.get(id=role)

                        customUser= CustomUser.objects.create(
                            user=user,
                            email=email, 
                            Employee=emp, 
                            Role=rol
                            )
                    
                        return Response({ 'success': 'Usuario creado con exito' })
        else:
                return Response({ 'error': 'Las contraseñas no coinciden' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF cookie set' })

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({ 'success': 'Usuario autenticado' })
            else:
                return Response({ 'error': 'Error de autenticación' })
        except:
            return Response({ 'error': 'Something went wrong when logging in' })

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Cerrar sesión' })
        except:
            return Response({ 'error': 'Algo salió mal al cerrar la sesión' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': 'CSRF cookie set' })

class DeleteAccountView(APIView):
    def delete(self, request, format=None):
        user = self.request.user

        try:
            User.objects.filter(id=user.id).delete()

            return Response({ 'success': 'Usuario eliminado exitosamente' })
        except:
            return Response({ 'error': 'Se produjo un error al intentar eliminar al usuario' })

class GetUserView(APIView):
    def get(self, request, format=None):
        
        try:
            user = self.request.user
            username = user.username
            user=User.objects.get(id=user.id)
            
            customUser = CustomUser.objects.get(user=user)
            customUser = CustomUserSerializer(customUser)

            return Response({ 'CustomUser': customUser.data, 'username': str(username) })
        except:
            return Response({ 'error': 'Algo salió mal al recuperar el perfil' })


class UpdateUserView(APIView):
    def put(self, request, format=None):

        try:
            user = self.request.user
            username = user.username
            user=User.objects.get(id=user.id)
            data = self.request.data

            email = data['email']
            CustomUser.objects.filter(user=user).update(email=email)

            customUser = CustomUser.objects.get(user=user)
            customUser = CustomUserSerializer(customUser)

            return Response({ 'CustomUser': customUser.data, 'username': str(username) })

        except:
            return Response({ 'error': 'Algo salió mal al actualizar el perfil' })