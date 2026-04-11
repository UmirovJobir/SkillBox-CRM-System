from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm


@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/products-list.html", {"products": products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/products-detail.html", {"object": product})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/products/")
    else:
        form = ProductForm()
    return render(request, "products/products-create.html", {"form": form})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(f"/products/{pk}/")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/products-edit.html", {"form": form, "object": product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("/products/")
    return render(request, "products/products-delete.html", {"object": product})