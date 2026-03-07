import urllib.parse
from django.shortcuts import render, redirect
from .models import Appointment


def home(request):
    return render(request, "home.html")


def book(request):

    slots = [
        "09:00","09:30","10:00","10:30","11:00","11:30","12:00",
        "17:00","17:30","18:00","18:30","19:00","19:30","20:00"
    ]

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        time = request.POST.get("time")

        # phone validation
        if not phone.isdigit() or len(phone) != 10:
            return render(request,"book.html",{
                "slots":slots,
                "error":"Please enter a valid 10 digit phone number."
            })

        # name validation
        if not name.replace(" ","").isalpha():
            return render(request,"book.html",{
                "slots":slots,
                "error":"Name should contain only letters."
            })

        if not time:
            return render(request,"book.html",{
                "slots":slots,
                "error":"Please select a time slot."
            })

        # prevent double booking
        if Appointment.objects.filter(date=date,time=time).exists():
            return render(request,"book.html",{
                "slots":slots,
                "error":"This slot is already booked. Please choose another time."
            })

        # generate token
        token = Appointment.objects.filter(date=date).count() + 1

        Appointment.objects.create(
            name=name,
            phone=phone,
            date=date,
            time=time,
            token=token
        )

        message = f"""
New Appointment Booked

Name: {name}
Phone: {phone}
Date: {date}
Time: {time}
Token: {token}
"""

        encoded_message = urllib.parse.quote(message)

        # Replace with your dad's WhatsApp number
        whatsapp_url = f"https://wa.me/919392881524?text={encoded_message}"

        return redirect(whatsapp_url)

    return render(request,"book.html",{"slots":slots})


def success(request):

    name = request.GET.get("name")
    date = request.GET.get("date")
    time = request.GET.get("time")
    token = request.GET.get("token")

    return render(request,"success.html",{
        "name":name,
        "date":date,
        "time":time,
        "token":token
    })