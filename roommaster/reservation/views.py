from django.shortcuts import render
from django.http import HttpResponse
from reservation.models import Room, Customer, Employee, Reservation
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from reservation.availabilityform import AvailableForm


class HomeView(TemplateView):
    template_name = "reservation/home.html"


class RoomsView(ListView):
    model = Room
    template_name = "reservation/rooms.html"
    context_object_name = 'rooms'
    queryset = Room.objects.all()


class CustomersView(ListView):
    model = Customer
    template_name = "reservation/customers.html"
    context_object_name = 'customers'
    queryset = Customer.objects.all()


class ReservationsView(ListView):
    model = Reservation
    template_name = "reservation/reservations.html"
    context_object_name = 'reservations'
    queryset = Reservation.objects.all()


class EmployeesView(ListView):
    model = Employee
    template_name = "reservation/employees.html"
    context_object_name = 'employees'
    queryset = Employee.objects.all()


class AvailabilityView(ListView):
    model = Room
    template_name = "reservation/availability.html"
    context_object_name = 'rooms'
    # queryset = Room.objects.exclude((Q(reservation__checkin__lte='2019-07-05') & Q(reservation__checkout__gte='2019-07-05')) | (Q(reservation__checkin__lte='2019-07-10') & Q(reservation__checkout__gte='2019-07-10')))

    def get(self, request):
        form = AvailableForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AvailableForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data['Checkin']
            checkout = form.cleaned_data['Checkout']
            return render(request, self.template_name, {'form': form, 'rooms': Room.objects.exclude((Q(reservation__checkin__lte=checkin) & Q(reservation__checkout__gte=checkin)) | (Q(reservation__checkin__lte=checkout) & Q(reservation__checkout__gte=checkout)))})
