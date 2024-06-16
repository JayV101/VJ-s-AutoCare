from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

class Employee:
    def __init__(self, name, hourly_wage):
        self.name = name
        self.hourly_wage = hourly_wage
        self.total_hours_worked = 0
        self.clock_in_time = None

    def clock_in(self, clock_in_time):
        self.clock_in_time = datetime.strptime(clock_in_time, '%H:%M')
        return f"{self.name} has successfully clocked in at {self.clock_in_time.strftime('%H:%M')}."

    def clock_out(self, clock_out_time):
        if not self.clock_in_time:
            return "Error: You must clock in before clocking out."

        clock_out_time = datetime.strptime(clock_out_time, '%H:%M')
        if clock_out_time <= self.clock_in_time:
            return "Error: Clock out time must be later than clock in time."
        
        hours_worked = (clock_out_time - self.clock_in_time).seconds / 3600
        self.total_hours_worked += hours_worked
        self.clock_in_time = None
        return f"{self.name} has successfully clocked out at {clock_out_time.strftime('%H:%M')}. Total hours worked today: {hours_worked:.2f}"

    def print_paycheck(self):
        base_hours = min(self.total_hours_worked, 20)
        overtime_hours = max(self.total_hours_worked - 20, 0)
        base_pay = base_hours * self.hourly_wage
        overtime_pay = overtime_hours * self.hourly_wage * 1.15
        total_pay = base_pay + overtime_pay

        paycheck_details = {
            "name": self.name,
            "total_hours_worked": self.total_hours_worked,
            "base_pay": base_pay,
            "overtime_pay": overtime_pay,
            "total_pay": total_pay
        }
        return paycheck_details

employees = {}

@app.route('/')
def home():
    return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    hourly_wage = float(request.form['hourly_wage'])
    employees[name] = Employee(name, hourly_wage)
    return redirect(url_for('home'))

@app.route('/clock_in/<name>', methods=['POST'])
def clock_in(name):
    clock_in_time = request.form['clock_in_time']
    message = employees[name].clock_in(clock_in_time)
    return redirect(url_for('home', message=message))

@app.route('/clock_out/<name>', methods=['POST'])
def clock_out(name):
    clock_out_time = request.form['clock_out_time']
    message = employees[name].clock_out(clock_out_time)
    return redirect(url_for('home', message=message))

@app.route('/print_paycheck/<name>')
def print_paycheck(name):
    paycheck_details = employees[name].print_paycheck()
    return render_template('paycheck.html', paycheck=paycheck_details)

@app.route('/remove_employee/<name>')
def remove_employee(name):
    del employees[name]
    return redirect(url_for('home'))

@app.route('/print_all_paychecks')
def print_all_paychecks():
    paycheck_list = [employee.print_paycheck() for employee in employees.values()]
    return render_template('all_paychecks.html', paychecks=paycheck_list)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
