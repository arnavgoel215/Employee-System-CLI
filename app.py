import zmq

context = zmq.Context()

# Addresses for microservices
services = {
    "db_service": "tcp://localhost:5556",
    "paycheck_service": "tcp://localhost:5557",
    "time_service": "tcp://localhost:5558",
    "email_service": "tcp://localhost:5559"
}

sockets = {name: context.socket(zmq.REQ) for name in services}
for name, address in services.items():
    sockets[name].connect(address)

def send_request(command, data={}):
    """Sends request to database service"""
    socket = sockets["db_service"]
    socket.send_json({"command": command, **data})
    return socket.recv_json()

def calculate_paycheck(hours, rate):
    socket = sockets["paycheck_service"]
    socket.send_json({"hours": hours, "pay_rate": rate})
    response = socket.recv_json()
    return response

def send_pdf(filename, email):
    socket = sockets["email_service"]
    email_data = {"name": "Arnav Goel",
                  "email": "goelar@oregonstate.edu",
                  "type": "paystub"}
    socket.send_json(email_data)
    message = socket.recv()
    print(message)
    with open(filename, "rb") as file:
        data = file.read()
        socket.send(data)

def add_employee():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email address: ")
    phone = input("Enter phone number: ")
    response = send_request("add_employee",
                            {"first_name": first_name, "last_name": last_name, "phone": phone, "email": email})
    print(response["message"])

def view_employees():
    response = send_request("view_employees")
    if "data" in response:
        print("\nEmployees:")
        print("Employee ID | First Name | Last Name | Phone Number | Email Address")
        for employee in response["data"]:
            print(f"{employee[0]} | {employee[1]} | {employee[2]} | {employee[3]} | {employee[4]}")
    else:
        print(response["message"])

def delete_employee():
    view_employees()
    employee_id = input("Enter id of employee you want to delete: ")
    confirmation = input("Are you sure you want to delete this employee? This action is irreversible. Enter y to proceed otherwise enter any key to go back: ")
    if confirmation.lower() == 'y':
        response = send_request("delete_employee", {"id": employee_id})
        print(response["message"])

def update_employee():
    view_employees()
    employee_id = input("Enter id of employee you want to update: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email address: ")
    response = send_request(
        "update_employee",
        {"first_name": first_name, "last_name": last_name, "phone": phone, "email": email, "id": employee_id})
    print(response["message"])

def add_paycheck():
    hours = int(input("Enter hours worked: "))
    rate = float(input("Enter hourly rate of pay: "))
    total_pay = calculate_paycheck(hours, rate)
    view_employees()
    employee_id = input("Enter id number of employee for this paycheck: ")
    response = send_request("add_paycheck",
                            {"hours": hours, "rate": rate, "employee_id": employee_id, "pay": total_pay})
    print(response["message"])

def view_paychecks():
    response = send_request("view_paychecks")
    if "data" in response:
        print("\nPaychecks:")
        for paycheck in response["data"]:
            print("Paycheck ID | Employee ID | Hours Worked | Total Pay")
            print(f"{paycheck[0]} | {paycheck[1]} | {paycheck[2]} | {paycheck[3]} | ${round(float(paycheck[4]), 2)}")
    else:
        print(response["message"])

def delete_paycheck():
    view_paychecks()
    paycheck_id = int(input("Enter id of employee you want to delete: "))
    confirmation = input("Are you sure you want to delete this paycheck? This action is irreversible. Enter y to proceed otherwise enter any key to go back: ")
    if confirmation.lower() == 'y':
        response = send_request("delete_paycheck", {"id": paycheck_id})
        print(response["message"])

def update_paycheck():
    view_paychecks()
    paycheck_id = input("Enter id number of paycheck you want to update: ")
    hours = input("Enter hours worked: ")
    rate = input("Enter hourly rate of pay: ")
    employee_id = ("Enter id number of employee for this paycheck: ")
    response = send_request("update_paycheck",
                            {"id": paycheck_id, "hours": hours, "rate": rate, "pay": total_pay, "employee_id": employee_id})
    print(response["message"])

if __name__ == "__main__":
    socket = sockets["time_service"]  # Connects to date microservice
    socket.send_string("GET_DATE")
    curr_date = socket.recv_string()
    print(f"The date today is {curr_date}")
    while True:
        print("\nEmployee Management System Menu:")
        print("1. Add Employee (You will have to enter each employee manually)")
        print("2. View Employees")
        print("3. Delete Employee")
        print("4. Update Employee")
        print("5. Add Paycheck (You will have to enter each paycheck manually)")
        print("6. View Paychecks")
        print("7. Delete Paycheck")
        print("8. Update Paycheck")
        print("9. Send PDF to Employee")
        print("10. Exit")

        selection = int(input("Enter selection: "))

        if selection == 1:
            add_employee()
        elif selection == 2:
            view_employees()
        elif selection == 3:
            delete_employee()
        elif selection == 4:
            update_employee()
        elif selection == 5:
            add_paycheck()
        elif selection == 6:
            view_paychecks()
        elif selection == 7:
            delete_paycheck()
        elif selection == 8:
            update_paycheck()
        elif selection == 10:
            print("Exiting...")
            break
        else:
            print("Invalid selection. Please try again")