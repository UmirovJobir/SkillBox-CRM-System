from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .forms import CustomerForm


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "customers/customers-list.html", {"customers": customers})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customers/customers-detail.html", {"object": customer})


@login_required
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/customers/")
    else:
        form = CustomerForm()
    return render(request, "customers/customers-create.html", {"form": form})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect(f"/customers/{pk}/")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "customers/customers-edit.html", {"form": form, "object": customer})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect("/customers/")
    return render(request, "customers/customers-delete.html", {"object": customer})