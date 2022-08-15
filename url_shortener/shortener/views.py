from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from shortener.models import ShortenedUrl
from shortener.forms import ShortenedUrlForm
from shortener.viewmixins import keyAsSlugMixin
from shortener.utils.shortener import short_url


class ShortenedUrlCreateView(LoginRequiredMixin, CreateView):
    form_class = ShortenedUrlForm
    template_name = "shortener/shortened_url_create_view.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user

        form.instance.key = short_url()
        while ShortenedUrl.objects.filter(key=form.instance.key).exists():
            form.instance.key = short_url()

        return super().form_valid(form)


class ShortenedUrlDetailView(LoginRequiredMixin, keyAsSlugMixin, DetailView):
    template_name = "shortener/shortened_url_detail_view.html"


class ShortenedUrlUpdateView(LoginRequiredMixin, keyAsSlugMixin, UpdateView):
    template_name = "shortener/shortened_url_update_view.html"
    fields = ("active_from", "active_until")


class ShortenedUrlDeleteView(LoginRequiredMixin, keyAsSlugMixin, DeleteView):
    template_name = "shortener/shortened_url_delete_view.html"
    success_url = reverse_lazy("shortener:create")
