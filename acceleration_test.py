import obd
import time


def acceleration_test(connection, start_speed=0, end_speed=100):
    try:
        if not (0 <= start_speed < end_speed):
            print("Invalid speed parameters.")
            return

        time.sleep(1)

        start_speed_response = connection.query(obd.commands.SPEED)
        current_speed = start_speed_response.value.magnitude if not start_speed_response.is_null() else 0
        print(f'Waiting for speed to be greater than {start_speed} km/h...')

        while current_speed <= start_speed:
            time.sleep(1)
            start_speed_response = connection.query(obd.commands.SPEED)
            current_speed = start_speed_response.value.magnitude if not start_speed_response.is_null() else 0

        print('Starting acceleration test...')
        start_time = time.time()
        while current_speed < end_speed:
            speed_response = connection.query(obd.commands.SPEED)
            current_speed = speed_response.value.magnitude if not speed_response.is_null() else 0

        end_time = time.time()

        acceleration_time = end_time - start_time
        print(f"Acceleration time from {start_speed} km/h to {end_speed} km/h: {acceleration_time:.2f} seconds")

    except:
        print("Error during acceleration test.")

    input("Press Enter to continue...")
