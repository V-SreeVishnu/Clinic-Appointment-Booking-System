from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os



def home(request):
    return render(request, "home.html")


def book(request):

    slots = [
        "09:00","09:30","10:00","10:30","11:00","11:30","12:00",
        "17:00","17:30","18:00","18:30","19:00","19:30","20:00"
    ]

    date = request.POST.get("date") or request.GET.get("date")

    booked_slots = []

    if date:
        booked_slots = list(
            Appointment.objects.filter(date=date).values_list("time", flat=True)
        )

    if request.method == "POST" and request.POST.get("time"):

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        time = request.POST.get("time")

        # prevent double booking
        if Appointment.objects.filter(date=date, time=time).exists():
            return render(request, "book.html", {
                "slots": slots,
                "booked_slots": booked_slots,
                "date": date,
                "error": "This slot is already booked. Please choose another time."
            })

        token = Appointment.objects.filter(date=date).count() + 1

        # save appointment
        Appointment.objects.create(
            name=name,
            phone=phone,
            date=date,
            time=time,
            token=token
        )

        # send email
        try:
            message = Mail(
                from_email='sreevishnu0101@gmail.com',
                from_email='sreevishnu0101@gmail.com',
                subject='New Clinic Appointment',
                  html_content=f"""
                <strong>New Appointment Booked</strong><br>
                Name: {name}<br>
                Phone: {phone}<br>
                Date: {date}<br>
                Time: {time}<br>
                Token: {token}
                """
            )
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
        except Exception as e:
            print(e)     

        return redirect(f"/success?name={name}&date={date}&time={time}&token={token}")

    return render(request, "book.html", {
        "slots": slots,
        "booked_slots": booked_slots,
        "date": date
    })


def success(request):

    name = request.GET.get("name")
    date = request.GET.get("date")
    time = request.GET.get("time")
    token = request.GET.get("token")

    return render(request, "success.html", {
        "name": name,
        "date": date,
        "time": time,
        "token": token
    })