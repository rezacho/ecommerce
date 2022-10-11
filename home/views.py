from django.shortcuts import render
from django.views import View
from .models import Product


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(is_available=True)
        return render(request, 'home.html', {'products': products})
