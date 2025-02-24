from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Paciente, Avaliacao
from .serializers import PacienteSerializer, AvaliacaoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from triagem.models import Avaliacao, Paciente
from .services import TriagemService

def is_admin(user):
    return user.groups.filter(name="Administrador").exists() or user.is_superuser

@login_required
@user_passes_test(is_admin)
def remover_avaliacao(request, avaliacao_id):
    avaliacao = Avaliacao.objects.get(id=avaliacao_id)
    avaliacao.delete()
    messages.success(request, "Avaliação removida com sucesso!")
    return redirect("home")
    
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("home")  # Redireciona para a home ou outra página
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "triagem/login.html")

# Logout
def logout_user(request):
    logout(request)
    messages.success(request, "Logout realizado com sucesso.")
    return redirect("login")

@login_required
def calcular_score(freq_cardiaca, freq_respiratoria, estado_crianca):
    score = 0
    
    # Avaliação da frequência cardíaca
    if freq_cardiaca < 60 or freq_cardiaca > 160:
        score += 2
    elif 60 <= freq_cardiaca <= 90 or 140 <= freq_cardiaca <= 160:
        score += 1
    
    # Avaliação da frequência respiratória
    if freq_respiratoria < 20 or freq_respiratoria > 60:
        score += 2
    elif 20 <= freq_respiratoria <= 30 or 50 <= freq_respiratoria <= 60:
        score += 1

    # Estado neurológico
    if estado_crianca == "Dormindo":
        score += 1

    return score


class PacienteViewSet(viewsets.ModelViewSet):
    """CRUD para Pacientes"""
    queryset = Paciente.objects.all().order_by('-created_at')
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated]

class AvaliacaoViewSet(viewsets.ModelViewSet):
    """CRUD para Avaliações"""
    queryset = Avaliacao.objects.all().order_by('-data')
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsAuthenticated]
