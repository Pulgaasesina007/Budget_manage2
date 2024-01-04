from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('Home/', views.Index, name='Home'),
    path('Gastos_Ingreso_modulo/', views.Gastos_Ingreso_modulo, name= 'Ingreso_modulo'),
    path('actualizar_datos/', login_required(views.usuario_act_dat),name='usuario_act_dat'),
    path('cambiar_contraseña/', login_required(views.act_password),name = 'act_password'),
    path('Usuario_r/',views.Usuario_r,name = 'Usuario_r'),
    path('Perfil_usuario/',login_required(views.Perfil_usuario), name='Perfil_usuario'),
    path('logout/', views.logout_view, name='logout'),

    path('',views.login_usuario, name = 'login_usuario'),

    #Ingreso gastos modulo
    path('agregar_ingreso/', views.registrar_ingreso, name= 'reg_ingreso'),

   # path('agregar_gasto/', views.agregar_gasto,name='agg_gasto'),
    path('agregar_gasto/', login_required(views.registrar_gasto),name='reg_gastos'),
    path('Balance/',login_required(views.grafico), name='Balance'),
    path('Historial/',views.historial,name='Historial'),
    path('Busqueda_gastos_ingresos/',login_required(views.obtener_balance),name='Busqueda_gastos_ingresos'),
    path('ListaGastosIngresos/',views.lista_gastos,name='listaGastosIngresos'),
    path('predicion/',views.modelo_prediccion, name='modelo_prediccion')

]