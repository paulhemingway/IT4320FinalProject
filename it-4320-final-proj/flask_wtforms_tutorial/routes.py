from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *
from .admin import *
from .chart import *
from .reservation import *


#@app.route("/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():

    form = AdminLoginForm()
    form.chart = []

    if(form.is_submitted()):
      
      if(authenticate(form.username.data, form.password.data)):
        form.message = 'authenticated'
        form.chart = display_chart()
        form.totalSales = calculate_sales()
      else:
        form.message = 'invalid username and/or password'
      # this code triggers when user hits submit
      # this is where username and password should be authenticated.

    return render_template("admin.html", form=form, template="form-template")

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()
    form.chart = display_chart()
    form.message = ""
    form.error = ""
    form.code = ""
    if(form.is_submitted()):
      form.code = generate_reservation_code(form.first_name.data)
      if(add_reservation(form.first_name.data, int(form.row.data), int(form.seat.data), form.code)):
        form.message = "Congratulations {}! Row: {} Seat: {} is now reserved for you. Enjoy the trip!".format(form.first_name.data, form.row.data, form.seat.data)
        form.chart = display_chart()

        form.first_name.data = ""
        form.last_name.data = ""
        form.row.data = ""
        form.seat.data = ""
      else:
        form.error = "ERROR! Row {} Seat {} is already assigned. Try again.".format(form.row.data, form.seat.data)
      
        

    return render_template("reservations.html", form=form, template="form-template")

