from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Advertisement
from .forms import AdvertisementForm
from leads.models import Lead
from customers.models import Customer
from contracts.models import Contract


@login_required
def advertisement_list(request):
    ads = Advertisement.objects.all()
    return render(request, "ads/ads-list.html", {"ads": ads})


@login_required
def advertisement_detail(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    return render(request, "ads/ads-detail.html", {"object": ad})


@login_required
def advertisement_create(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/ads/")
    else:
        form = AdvertisementForm()
    return render(request, "ads/ads-create.html", {"form": form})


@login_required
def advertisement_edit(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect(f"/ads/{pk}/")
    else:
        form = AdvertisementForm(instance=ad)
    return render(request, "ads/ads-edit.html", {"form": form, "object": ad})


@login_required
def advertisement_delete(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    if request.method == "POST":
        ad.delete()
        return redirect("/ads/")
    return render(request, "ads/ads-delete.html", {"object": ad})


@login_required
def advertisement_statistic(request):
    ads = Advertisement.objects.all()
    for ad in ads:
        # Количество лидов по этой рекламе
        ad.leads_count = Lead.objects.filter(advertisement=ad).count()
        # Количество клиентов (лид стал клиентом)
        ad.customers_count = Customer.objects.filter(lead__advertisement=ad).count()
        # Прибыль: сумма контрактов / бюджет рекламы
        contracts_sum = Contract.objects.filter(
            customer__lead__advertisement=ad
        ).aggregate(total=Sum("cost"))["total"]
        if contracts_sum and ad.budget:
            ad.profit = round(contracts_sum / ad.budget, 2)
        else:
            ad.profit = None
    return render(request, "ads/ads-statistic.html", {"ads": ads})