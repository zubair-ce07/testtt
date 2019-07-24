from django.shortcuts import render
from django.http import HttpResponse
from reservation.models import Room, Customer, Employee, Reservation
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from reservation.form import AvailabilityForm, ReservationForm


class HomeView(TemplateView):
    template_name = 'reservation/home.html'


class RoomsView(ListView):
    model = Room
    template_name = 'reservation/rooms.html'
    context_object_name = 'rooms'
    queryset = Room.objects.all()


class CustomersView(ListView):
    model = Customer
    template_name = 'reservation/customers.html'
    context_object_name = 'customers'
    queryset = Customer.objects.all()


class ReservationsView(ListView):
    model = Reservation
    template_name = 'reservation/reservations.html'
    context_object_name = 'reservations'
    queryset = Reservation.objects.all()

    def get(self, request):
        return render(request, self.template_name, {'reservations': self.queryset})

    def post(self, request):
        room = Room.objects.filter(room_no=request.POST.get('room'))[0]
        rent = request.POST.get('rent')
        customer = Customer.objects.filter(id=request.POST.get('customer'))[0]
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        Reservation(room=room, rent=rent, customer=customer, checkin=checkin, checkout=checkout).save()
        return render(request, self.template_name, {'reservations': self.queryset})


class EmployeesView(ListView):
    model = Employee
    template_name = 'reservation/employees.html'
    context_object_name = 'employees'
    queryset = Employee.objects.all()


class AvailabilityView(ListView):
    model = Room
    template_name = 'reservation/availability.html'
    context_object_name = 'rooms'

    def get(self, request):
        form = AvailabilityForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            checkin = form.cleaned_data['checkin']
            checkout = form.cleaned_data['checkout']
            context = {
                'form': form,
                'rooms': Room.objects.exclude((Q(reservation__checkin__lte=checkin) &
                                               Q(reservation__checkout__gte=checkin)) | (
                                               Q(reservation__checkin__lte=checkout) &
                                               Q(reservation__checkout__gte=checkout))),
                'checkin': checkin,
                'checkout': checkout
            }
            return render(request, self.template_name, context)


class ReportView(ListView):
    template_name = 'reservation/reserveroom.html'

    def get(self, request, id, checkin, checkout):
        form = ReservationForm(room=Room.objects.filter(id=id)[0], checkin=checkin, checkout=checkout)
        return render(request, self.template_name, {'form': form})
