import obd


def dtc_errors(connection):
    try:
        response = connection.query(obd.commands.GET_CURRENT_DTC)

        if response.value:
            print("DTC Errors:")
            if isinstance(response.value, list):
                for dtc_code in response.value:
                    print(dtc_code)
            elif isinstance(response.value, tuple):
                print(response.value)
            else:
                print(response.value)

            clear_errors = input("Do you want to clear DTC errors? (yes/no): ").lower() == 'yes'

            if clear_errors:
                connection.query(obd.commands.CLEAR_DTC)
                print("DTC errors cleared.")
        else:
            print("No DTC errors found.")
    except:
        print("No connection with the OBD-II interface.")

    input("Press Enter to continue...")
