import tkinter as tk
from tkinter import Canvas
import obd


def car_dashboard(connection):
    root = tk.Tk()
    root.title("Car Dashboard")
    root.geometry("600x400")

    speed_label = tk.Label(root, text="0 km/h", font=("Helvetica", 24))
    speed_label.pack(pady=20)

    rpm_canvas = Canvas(root, width=400, height=100, bg="white")
    rpm_canvas.pack()

    temperature_label = tk.Label(root, text="0°C", font=("Helvetica", 18))
    temperature_label.pack(pady=20)

    temperature_alert_label = tk.Label(root, text="Temperature too high", font=("Helvetica", 18), bg="red", fg="black")
    rpm_alert_label = tk.Label(root, text="RPM too high", font=("Helvetica", 18), bg="red", fg="black")

    speed = 0
    rpm = 0
    temperature = 0

    def update_dashboard():
        nonlocal speed, rpm, temperature

        speed_command = obd.commands.SPEED
        rpm_command = obd.commands.RPM
        temp_command = obd.commands.COOLANT_TEMP

        speed_response = connection.query(speed_command)
        rpm_response = connection.query(rpm_command)
        temp_response = connection.query(temp_command)

        if not speed_response.is_null() and isinstance(speed_response.value.magnitude, (float, int)):
            speed = int(speed_response.value.magnitude)
        if not rpm_response.is_null() and isinstance(rpm_response.value.magnitude, (float, int)):
            rpm = int(rpm_response.value.magnitude)
        if not temp_response.is_null() and isinstance(temp_response.value.magnitude, (float, int)):
            temperature = int(temp_response.value.magnitude)

        speed_label.config(text=f"{speed} km/h")
        draw_rpm_meter()
        check_and_blink_temperature_alert()
        check_and_blink_rpm_alert()
        temperature_label.config(text=f"{temperature}°C")

        root.after(50, update_dashboard)

    def draw_rpm_meter():
        rpm_canvas.delete("all")

        rpm_canvas.create_line(50, 50, 350, 50, width=2)

        label_range = range(0, 6000, 1000)

        for i in range(0, 7):
            x_label = 50 + (i * 50)
            if i < len(label_range):
                rpm_canvas.create_text(x_label, 70, text=f"{label_range[i] // 1000}", font=("Helvetica", 10))
                if i >= 5:
                    rpm_canvas.create_text(x_label, 70, text=f"{label_range[i] // 1000}", font=("Helvetica", 10),
                                           fill="red")

        max_rpm = 6000
        rpm_percent = min(1, rpm / max_rpm)
        x = 50 + rpm_percent * 300

        if rpm >= 5000:
            rpm_canvas.create_line(50, 50, x, 50, width=6, fill="red")
        else:
            rpm_canvas.create_line(50, 50, x, 50, width=6)

    def check_and_blink_temperature_alert():
        if temperature > 100:
            temperature_alert_label.pack()
            root.after(500, lambda: temperature_alert_label.pack_forget())
            root.after(1000, check_and_blink_temperature_alert)
        else:
            temperature_alert_label.pack_forget()

    def check_and_blink_rpm_alert():
        if rpm > 5000:
            rpm_alert_label.pack()
            root.after(500, lambda: rpm_alert_label.pack_forget())
            root.after(1000, check_and_blink_rpm_alert)
        else:
            rpm_alert_label.pack_forget()

    update_dashboard()
    root.mainloop()

    input("Press Enter to continue...")
