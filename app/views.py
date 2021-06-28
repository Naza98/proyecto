


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy
from app.forms import CambiarContraseñaForm
from bases.views import SinPrivilegios
from django.contrib.auth.views import PasswordChangeView


class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    form_class = CambiarContraseñaForm
    template_name = 'base/cambiar_contraseña.html'
    success_url = reverse_lazy('bases:home.html')
    success_message = 'La contraseña fue actualizada con éxito'