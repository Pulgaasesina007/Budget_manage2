from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate,login
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .forms import Register_User,Login_user,CambiarContraseñaForm,Act_User,GastosForm,IngresosForm
from .models import user_perfil,Gastos,Tipo_Gasto,Ingresos,Tipo_Ingreso
from django.contrib.auth import authenticate, login,logout
import math
import matplotlib.pyplot as plt
import  io



def Index(request):
    return  render(request,'inicio.html')
# Create your views here.

def Usuario_r(request):
    if request.method == 'POST':
        print("POST a")
        form = Register_User(request.POST)
        if form.is_valid():
            if user_perfil.objects.filter(username=form.cleaned_data['username']).exists():
                print("usuario ya existe")
                form.add_error('username', 'Este usuario ya existe')
            else:
                print("login")
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                login(request, user)
                return redirect('/Home')
        else:
            print(form.errors)
            print("error form no valido ")
    else:
        form = Register_User()  # Mover la inicialización del formulario fuera del bloque 'if'
    return render(request, 'Usuario/usuario_r.html', {'form': form})
def Gastos_Ingreso_modulo(request):
    return render(request,'Gastos_Ingresos_modulo.html')


def login_usuario(request):
    mensaje_error = ''

    print("Entrando a la vista de login")

    if request.method == 'POST':
        print("Método POST recibido")
        print(request.POST)  # Imprime el contenido del formulario

        form = Login_user(request, request.POST)

        if form.is_valid():
            print("Formulario válido")

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(f"Username: {username}")
            print(f"Password: {password}")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                print(f"Usuario autenticado: {user.username}")

                login(request, user)

                next_url = request.POST.get('next') or 'Home/'
                return redirect(next_url)

            else:
                print("Error autenticando usuario")
                mensaje_error = "Credenciales inválidas"

        else:
            print("Formulario no válido")
            print(form.errors)

    else:
        print("Petición GET recibida")
        form = Login_user()

    return render(request, 'Usuario/Login_usuario.html', {'form': form, 'mensaje_error': mensaje_error, 'next': request.GET.get('next', '')})


def Perfil_usuario(request):
    perfil = get_object_or_404(user_perfil, username=request.user.username)
    print(perfil)
    return render(request, 'Usuario/Perfil_user.html', {'datos': perfil})
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('login_usuario')

def usuario_act_dat(request):
    perfil = get_object_or_404(user_perfil, username=request.user.username)

    if request.method == 'POST':
        print("entro al post")
        form_perfil = Act_User(request.POST, instance=perfil)

        if form_perfil.is_valid():
            print("entro al form")
            datos_perfil = form_perfil.save(commit=False)
            datos_perfil.usuario = request.user
            datos_perfil.save()

            return redirect('Perfil_usuario')  # Cambia 'perfil' con la URL a la que deseas redirigir después de guardar
        else:
            print(form_perfil.errors)
    else:


        form_perfil = Act_User(instance=perfil)

    return render(request, 'Usuario/actualizar_datos.html', {
        'perfil': perfil,
        'form_perfil': form_perfil,
    })

def act_password(request):
    perfil = get_object_or_404(user_perfil, username=request.user.username)

    if request.method == 'POST':
        form = CambiarContraseñaForm(request.POST)

        if form.is_valid():
            password1 = form.cleaned_data['password1']

            # Actualizar la contraseña del usuario
            request.user.set_password(password1)
            request.user.save()
            next_url = request.POST.get('next') or 'logout'
            return redirect(next_url)

    else:
        form = CambiarContraseñaForm()

    return render(request, './Usuario/cambiar_contraseña.html', {'form': form, 'perfil': perfil})


def agregar_ingreso(request):
   # opciones = Tipo_Ingreso.objects.all(Gastos, )
    ingreso_individual = Ingresos.objects.all()
    sumatoria_ingresos = 0
    for i in ingreso_individual:
        sumatoria_ingresos += i.valor
        print(f"{i.descripcion} --- Valor: ${i.valor}")

    print(sumatoria_ingresos)
    return render(request, 'Ingresos/add_ingreso.html', {
      #  '#opciones': opciones,
        'suma_ingresos': sumatoria_ingresos
    })


def registrar_ingreso(request):
    descripcion = request.POST['descripcion']
    tipo_ingreso = request.POST['categoria']
    valorDinero = request.POST['valorDinero']
    fecha = request.POST['fechaDesde']
    usuario = get_object_or_404(user_perfil, username=request.user.username)
    print(descripcion)
    print(tipo_ingreso)
    print(valorDinero)
    print(fecha)
    print(type(usuario.id))
    Ingresos.objects.create(descripcion=descripcion, fecha_registro=fecha, valor=valorDinero,
                            tipoIngreso_id=tipo_ingreso, Usuario_id=usuario.id)
    return redirect('/Home/Perfil_usuario')




from django.db.models import Sum
def registrar_gasto(request):
    perfil = get_object_or_404(user_perfil, username=request.user.username)
    if request.method == 'POST':

        form = GastosForm(request.POST)
        if form.is_valid():
            print("aaaaaaaa",form.cleaned_data)  # Verificar que traiga tipoGasto
            gasto = form.save(commit=False)
            gasto.Usuario = perfil


            gasto.save()
            return redirect('/Home/')
        else:
            print(form.errors)
            print(request.POST)
    else:
        form = GastosForm()

    opciones_tipo_gasto = Tipo_Gasto.objects.all()
    total_gastos = Gastos.objects.filter(Usuario=perfil).aggregate(Sum('valor'))['valor__sum'] or 0.0



    return render(request, 'Gastos/add_gasto.html', {'form': form, 'total_gastos': total_gastos, 'opciones_tipo_gasto': opciones_tipo_gasto})


def registrar_ingreso(request):
    perfil = get_object_or_404(user_perfil, username=request.user.username)

    if request.method == 'POST':
        form = IngresosForm(request.POST)

        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.Usuario = perfil
            ingreso.save()

            return redirect('/Home/')
        else:
            print(form.errors)
            print(request.POST)
    else:
        form = IngresosForm()

    opciones_tipo_ingreso = Tipo_Ingreso.objects.all()
    total_ingreso = Ingresos.objects.filter(Usuario=perfil).aggregate(Sum('valor'))['valor__sum'] or 0.0

    return render(request, 'Ingresos/add_ingreso.html',
                  {'form': form, 'total_ingreso': total_ingreso, 'opciones_tipo_ingreso': opciones_tipo_ingreso})
def lista_gastos(request):
    gastos = Gastos.objects.all()
    return render(request, 'lista_gastos.html', {'gastos': gastos})
#_________________________________




@require_GET
@login_required
def obtener_balance(request):
    perfil = get_object_or_404(user_perfil, username=request.user.username)
    categoria = request.GET.get('categoria')
    fechadesde = request.GET.get('fechadesde')
    fechahasta = request.GET.get('fechahasta')

    resultados = []

    if categoria == 'gastos':
        # Calcular el total de gastos
        total_gastos = Gastos.objects.filter(Usuario=perfil, fecha_registro__range=(fechadesde, fechahasta)).aggregate(Sum('valor'))['valor__sum'] or 0.0

        gastos = Gastos.objects.filter(
            fecha_registro__range=(fechadesde, fechahasta), Usuario=perfil
        ).values('descripcion', 'fecha_registro', 'valor', 'tipoGasto', 'Usuario__username', 'Usuario')

        resultados = list(gastos)

        if resultados:
            # Agregar el total de gastos al primer elemento del resultado
            resultados[0]['total_gastos'] = total_gastos

    elif categoria == 'ingresos':
        # Calcular el total de ingresos
        total_ingresos = Ingresos.objects.filter(Usuario=perfil, fecha_registro__range=(fechadesde, fechahasta)).aggregate(Sum('valor'))['valor__sum'] or 0.0

        ingresos = Ingresos.objects.filter(
            fecha_registro__range=(fechadesde, fechahasta), Usuario=perfil
        ).values('descripcion', 'fecha_registro', 'valor', 'tipoIngreso', 'Usuario__username', 'Usuario')

        resultados = list(ingresos)

        if resultados:
            # Agregar el total de ingresos al primer elemento del resultado
            resultados[0]['total_ingresos'] = total_ingresos

    return JsonResponse(resultados, safe=False)



def historial(request):
    return render(request,'Historial/Historial_gastos_ingresos.html')








import base64
import matplotlib
matplotlib.use('Agg')

def grafico(request):
    # Obtener el perfil del usuario logeado
    user_profile = get_object_or_404(user_perfil, username=request.user.username)

    # Obtener todas las categorías de gastos e ingresos
    categorias_gastos = Tipo_Gasto.objects.all()
    categorias_ingresos = Tipo_Ingreso.objects.all()

    # Verificar si el usuario tiene valores ingresados
    if not (Gastos.objects.filter(Usuario=user_profile).exists() and Ingresos.objects.filter(Usuario=user_profile).exists()):
        return render(request, 'grafico.html', {'mensaje': 'No existen valores ingresados para este usuario/Falta de ingresar ingresos u gastos.'})

    # Crear listas para etiquetas y valores de gráficos de pastel
    labels_gastos = []
    values_gastos = []

    for categoria in categorias_gastos:
        total_gastos_categoria = Gastos.objects.filter(tipoGasto=categoria, Usuario=user_profile).aggregate(Sum('valor'))['valor__sum'] or 0.0
        labels_gastos.append(categoria.nombre)
        values_gastos.append(total_gastos_categoria)

    labels_ingresos = []
    values_ingresos = []

    for categoria in categorias_ingresos:
        total_ingresos_categoria = Ingresos.objects.filter(tipoIngreso=categoria, Usuario=user_profile).aggregate(Sum('valor'))['valor__sum'] or 0.0
        labels_ingresos.append(categoria.nombre)
        values_ingresos.append(total_ingresos_categoria)

    # Crear un gráfico de pastel para el total de gastos e ingresos
    total_gastos = Gastos.objects.filter(Usuario=user_profile).aggregate(Sum('valor'))['valor__sum'] or 0.0
    total_ingresos = Ingresos.objects.filter(Usuario=user_profile).aggregate(Sum('valor'))['valor__sum'] or 0.0

    labels_total = ['Gastos', 'Ingresos']
    values_total = [total_gastos, total_ingresos]

    # Tamaño personalizado para el gráfico
    figsize = (5, 6)  # Ajusta el tamaño según tus preferencias

    # Convertir gráficos a cadenas base64
    grafica_gastos_base64 = plot_to_base64(labels_gastos, values_gastos, figsize)
    grafica_ingresos_base64 = plot_to_base64(labels_ingresos, values_ingresos, figsize)
    grafica_total_base64 = plot_to_base64(labels_total, values_total, figsize)

    # Calcular el resultado total (ingresos - gastos)
    total_resultado = total_ingresos - total_gastos

    # Pasar la información a la plantilla
    return render(request, 'grafico.html', {
        'grafica_gastos_base64': grafica_gastos_base64,
        'grafica_ingresos_base64': grafica_ingresos_base64,
        'grafica_total_base64': grafica_total_base64,
        'total_resultado': total_resultado,
    })

def plot_to_base64(labels, values, figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    colores = plt.cm.Set1.colors
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90,colors=colores)
    ax.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
###Prediccion de precios

from django.shortcuts import render
from io import BytesIO
import base64
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def modelo_prediccion(request):
    if request.method == 'POST':
        selected_company = request.POST.get('empresa', '')
        fechaDesde = request.POST.get('fechaDesde')
        fechaHasta = request.POST.get('fechaHasta')

        # Verificar si alguna de las fechas es None
        if fechaDesde is None or fechaHasta is None:
            return render(request, 'Prediccion/prediccion.html', {'image_base64': None, 'resultados_prediccion': None, 'mensaje_error': 'Las fechas son requeridas'})

        # descargar datos históricos
        base = selected_company
        data = yf.download(base, start=fechaDesde, end=fechaHasta)

        # Verificar si hay suficientes datos para la división
        if len(data) <= 1:
            return render(request, 'Prediccion/prediccion.html', {'image_base64': None, 'resultados_prediccion': None, 'mensaje_error': 'No hay suficientes datos para la división'})

        # Obtener el nombre de la empresa
        company_name = yf.Ticker(base).info['longName']

        # crear variables predictorias.
        data['SMA_10'] = data['Close'].rolling(window=10).mean()
        data['SMA_30'] = data['Close'].rolling(window=30).mean()
        data['SMA_60'] = data['Close'].rolling(window=60).mean()
        data['SMA_100'] = data['Close'].rolling(window=100).mean()

        data = data.dropna()

        X = data[['SMA_10', 'SMA_30', 'SMA_60', 'SMA_100']].values
        y = data['Close'].values

        # Verificar si hay suficientes datos para la división después de la limpieza
        if len(data) <= 1:
            return render(request, 'Prediccion/prediccion.html', {'image_base64': None, 'resultados_prediccion': None, 'mensaje_error': 'No hay suficientes datos para la división después de la limpieza'})

        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Modelo de árbol de decisión
        tree_regressor = DecisionTreeRegressor(random_state=0)
        tree_regressor.fit(X_train, y_train)
        y_pred_tree = tree_regressor.predict(X_test)
        mse_tree = mean_squared_error(y_test, y_pred_tree)
        print("Error cuadrático árbol de decisión:", mse_tree)

        # Hacer predicciones en datos futuros
        # En este ejemplo, asumimos que el periodo futuro es una continuación del conjunto de datos existente.
        future_data = data[['SMA_10', 'SMA_30', 'SMA_60', 'SMA_100']].tail(10).values
        future_predictions = tree_regressor.predict(future_data)

        # Imprime las predicciones futuras
        print("Predicciones futuras:", future_predictions)

        # Crear el gráfico con fechas reales en el eje x
        fig, ax = plt.subplots(figsize=(14, 9))
        ax.plot(data.index[-len(y_test):], y_test, label='Precio Real', marker='o')

        # Añade las predicciones futuras al gráfico
        future_dates = pd.date_range(start=data.index[-1], periods=len(future_predictions) + 1, freq='B')[1:]
        ax.plot(future_dates, future_predictions, label='Precio Predicho (futuro)', marker='o')

        # Añadir el nombre de la empresa al título del gráfico
        plt.title(f'Precio de Cierre de {company_name}')

        ax.set_xlabel('Fechas')
        ax.set_ylabel('Precio de Cierre')
        ax.legend()
        plt.xticks(rotation=45)

        # Establecer la frecuencia de las fechas a 'M' para que se muestren de mes en mes
        ax.xaxis.set_major_locator(plt.MaxNLocator(3))

        # Guardar el gráfico en un BytesIO para mostrarlo en la plantilla HTML
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        plt.close()

        # Codificar la imagen en base64
        image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

        # Crear una lista de resultados para mostrar en la plantilla
        resultados_prediccion = list(zip(future_dates, future_predictions))

        # Enviar la imagen y los resultados a la plantilla HTML
        return render(request, 'Prediccion/prediccion.html', {'image_base64': image_base64, 'resultados_prediccion': resultados_prediccion, 'mensaje_error': None})

    return render(request, 'Prediccion/prediccion.html', {'image_base64': None, 'resultados_prediccion': None, 'mensaje_error': None})
