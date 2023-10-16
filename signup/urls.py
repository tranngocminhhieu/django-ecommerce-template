from django.urls import path, include

app_name = 'signup'

urlpatterns = [
    path('api/', include('signup.api.urls'))
]