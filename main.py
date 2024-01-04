import obd
import car_dashboard
import dtc_errors
import acceleration_test


print("Connecting...")
connection = obd.OBD("COM5", 115200, None, False, 15, False, True)

if connection.status() != obd.OBDStatus.CAR_CONNECTED:
    print("Not connected to the car.")
    # exit()
else:
    print("Connected to the car.")
    end = False

    while not end:
        print("Choose an option:")
        print("1. Car Dashboard")
        print("2. Read Errors")
        print("3. Acceleration Test")
        print("4. Exit")

        choice = input("Enter the number of your choice: ")

        if choice == "1":
            car_dashboard.car_dashboard(connection)
        elif choice == "2":
            dtc_errors.dtc_errors(connection)
        elif choice == "3":
            start_speed = int(input("Enter start speed: "))
            end_speed = int(input("Enter end speed: "))
            acceleration_test.acceleration_test(connection, start_speed, end_speed)
        elif choice == "4":
            end = True
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
