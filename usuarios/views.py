from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Usuario
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def home(request):
    return render(request, "usuarios/home.html")


def cadastrar_usuario(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")
        telefone = request.POST.get("telefone")
        cargo = request.POST.get("cargo")

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "usuarios/cadastrar_usuario.html")

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "Usuário já cadastrado.")
            return render(request, "usuarios/cadastrar_usuario.html")

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "E-mail já cadastrado.")
            return render(request, "usuarios/cadastrar_usuario.html")

        try:
            validate_password(password1)
        except ValidationError as e:
            for erro in e.messages:
                messages.error(request, erro)

            return render(
                request,
                "usuarios/cadastrar_usuario.html"
            )

        Usuario.objects.create_user(
            username=username,
            email=email,
            password=password1,
            telefone=telefone,
            cargo=cargo,
        )

        messages.success(
            request,
            "Cadastro realizado. Aguarde aprovação do administrador."
        )

        return redirect("login")

    return render(request, "usuarios/cadastrar_usuario.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciais inválidas ou conta inativa.')
    return render(request, 'usuarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
    # return render(request, 'usuarios/login.html')



@login_required(login_url='/login/')
def gerenciar_contas(request):
    if request.user.perfil not in ['CHEFE', 'ASSESSOR']:
        messages.error(request, "Apenas usuários com perfil de Chefe de Gabinete ou Assessor podem acessar esta página.")
        return redirect("home")

    usuarios = Usuario.objects.filter(is_superuser=False).exclude(id=request.user.id)

    # Filtro "mostrar"
    if request.GET.get("mostrar") != "todos":
        usuarios = usuarios.filter(is_active=False)

    # Paginação
    paginator = Paginator(usuarios, 100)  # 100 usuários por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "usuarios/gerenciar_contas.html", {
        "page_obj": page_obj,

    })


@login_required(login_url='/login/')
def definir_perfil(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    # Impede que o usuário altere a própria conta
    if usuario == request.user:
        messages.error(request, "Você não pode alterar o status da própria conta.")
        return redirect('home')
    if request.method == 'POST':
        perfil = request.POST.get('perfil')
        if perfil == "inativo":
            usuario.perfil = None
        else:
            usuario.perfil = perfil

        usuario.save()  # ativa automaticamente se tiver tipo definido
        messages.success(request, f"Usuário {usuario.username} atualizado com sucesso.")
    return redirect('gerenciar_contas')


def sucesso(request):
    return render(request, 'usuarios/sucesso.html')