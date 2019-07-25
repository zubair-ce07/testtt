from django.shortcuts import render, redirect
from django.http import HttpResponse
from reservation.models import Room, Customer, Employee, Reservation
from django.views.generic import TemplateView, ListView
from django.db.models import Q, Count, Sum
from reservation.form import AvailabilityForm, ReservationForm
from django.views.decorators.cache import cache_control
import datetime


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


class ReportView(TemplateView):
    template_name = 'reservation/report.html'

    def get(self, request):
        today = datetime.date.today().strftime('%Y-%m-%d')
        month = datetime.date.today().strftime('%m')
        context = {
            'date': datetime.date.today().strftime('%B %d, %Y'),
            'daily_reservations': Reservation.objects.filter(checkin=today).count(),
            'monthly_reservations': Reservation.objects.filter(checkin__month = month).count(),
            'available_rooms': Room.objects.exclude(Q(reservation__checkin__lte=today) & Q(reservation__checkout__gte=today)).count(),
            'rooms': Room.objects.exclude(Q(reservation__checkin__lte=today) & Q(reservation__checkout__gte=today)),
            'total_employees': Employee.objects.count(),
            'employees': Employee.objects.values('designation').annotate(dcount=Count('designation')),
            'today_income': Reservation.objects.filter(checkin=today).aggregate(Sum('rent'))["rent__sum"],
            'monthly_income': Reservation.objects.filter(checkin__month=month).aggregate(Sum('rent'))["rent__sum"]
        }
        return render(request, self.template_name, context)


class ReserveRoomView(ListView):
    template_name = 'reservation/reserveroom.html'

    def get(self, request, id, checkin, checkout):
        form = ReservationForm(room=Room.objects.filter(id=id)[0], checkin=checkin, checkout=checkout)
        return render(request, self.template_name, {'form': form})


class AddReservation(TemplateView):
    template_name = '/reservations'

    @cache_control(no_cache=True, must_revalidate=True)
    def post(self, request):
        room = Room.objects.filter(room_no=request.POST.get('room'))[0]
        rent = request.POST.get('rent')
        customer = Customer.objects.filter(id=request.POST.get('customer'))[0]
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        Reservation(room=room, rent=rent, customer=customer, checkin=checkin, checkout=checkout).save()
        return redirect(self.template_name)
