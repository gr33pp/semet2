from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appliance, EnergyUsage
from .forms import ApplianceForm
from .utils import get_appliance_wattage

@login_required
def add_appliance(request):
    if request.method == 'POST':
        form = ApplianceForm(request.POST)
        if form.is_valid():
            appliance = form.save(commit=False)
            appliance.user = request.user
            appliance.wattage = get_appliance_wattage(appliance.name)
            # Alternatively, if using the AI service:
            # appliance.wattage = get_appliance_wattage_from_ai(appliance.name)
            appliance.save()
            return redirect('monitoring:appliance_list')
    else:
        form = ApplianceForm()
    return render(request, 'add_appliance.html', {'form': form})

@login_required
def appliance_list(request):
    appliances = Appliance.objects.filter(user=request.user)
    return render(request, 'appliance_list.html', {'appliances': appliances})

@login_required
def energy_dashboard(request):
    appliances = Appliance.objects.filter(user=request.user)
    total_kwh = sum(appliance.daily_kwh() for appliance in appliances)
    EnergyUsage.objects.create(user=request.user, total_kwh=total_kwh)
    usage_history = EnergyUsage.objects.filter(user=request.user).order_by('-date')
    return render(request, 'energy_dashboard.html', {
        'appliances': appliances,
        'total_kwh': total_kwh,
        'usage_history': usage_history
    })
