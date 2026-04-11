from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Contract
from .forms import ContractForm


@login_required
def contract_list(request):
    contracts = Contract.objects.all()
    return render(request, "contracts/contracts-list.html", {"contracts": contracts})


@login_required
def contract_detail(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    return render(request, "contracts/contracts-detail.html", {"object": contract})


@login_required
def contract_create(request):
    if request.method == "POST":
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/contracts/")
    else:
        form = ContractForm()
    return render(request, "contracts/contracts-create.html", {"form": form})


@login_required
def contract_edit(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    if request.method == "POST":
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            return redirect(f"/contracts/{pk}/")
    else:
        form = ContractForm(instance=contract)
    return render(request, "contracts/contracts-edit.html", {"form": form, "object": contract})


@login_required
def contract_delete(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    if request.method == "POST":
        contract.delete()
        return redirect("/contracts/")
    return render(request, "contracts/contracts-delete.html", {"object": contract})