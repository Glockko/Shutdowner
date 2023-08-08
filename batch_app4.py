#Shutdowner by Glockko
import tkinter as tk
import subprocess
import threading
import time

shutdown_thread = None
stop_flag = False
process = False

def execute_shutdown():
    global process
    subprocess.run(["shutdown", "/s", "/f", "/t", "10"], shell=True)
    output_text.insert(tk.END, "SHUTTING DOWN YOUR COMPUTER.\n")
    process = True

def cancel_shutdown():
    global shutdown_thread
    global stop_flag
    global process
    if shutdown_thread and shutdown_thread.is_alive():
        stop_flag = True
        output_text.insert(tk.END, "Timer Stopped. Shutdown Cancelled.\n")
    elif process:
        subprocess.run(["shutdown", "/a"], shell=True)
        output_text.insert(tk.END, "Shutdown Cancelled.\n")
        process = False
    else:
        output_text.insert(tk.END, "No shutdown process detected.\n")

def start_shutdown_timer(minutes):
    global shutdown_thread
    global stop_flag
    try:
        stop_flag = False
        wait_time = int(abs(minutes) * 60)
        cancel_shutdown()  # Cancel any ongoing timer
        shutdown_thread = threading.Thread(target=update_timer, args=(wait_time,))
        shutdown_thread.start()
        output_text.insert(tk.END, "Starting timer...\n")
    except ValueError:
        output_text.insert(tk.END, "Invalid input. Please enter a valid number of minutes.\n")

def update_timer(wait_time):
    global stop_flag
    while wait_time > 0 and not stop_flag:
        hours, remainder = divmod(wait_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_text.set(f"Time Left: {hours:02d}:{minutes:02d}:{seconds:02d}")
        wait_time -= 1
        time.sleep(1)
    timer_text.set("Time Left: 00:00:00")
    if not stop_flag:
        execute_shutdown()

# Create the main application window
app = tk.Tk()
app.title("Shutdown Timer")

# Entry widget to input custom time in minutes
entry = tk.Entry(app, width=50)
entry.pack(pady=10)

# Button to execute the custom shutdown timer
execute_button = tk.Button(app, text="Start Custom Shutdown Timer",
                           command=lambda: start_shutdown_timer(float(entry.get())))
execute_button.pack()

# Frame for the predefined shutdown timers
predefined_frame = tk.Frame(app)
predefined_frame.pack()

# Predefined shutdown timers in minutes
predefined_timers = [5, 10, 15, 20, 30, 40, 50, 60]
for time_in_minutes in predefined_timers:
    button = tk.Button(predefined_frame, text=f"{time_in_minutes} min",
                       command=lambda minutes=time_in_minutes: start_shutdown_timer(minutes))
    button.pack(side='left', padx=5)

# Button to cancel the timer
cancel_button = tk.Button(app, text="Cancel Shutdown", command=cancel_shutdown)
cancel_button.pack()

# Timer display
timer_text = tk.StringVar()
timer_label = tk.Label(app, textvariable=timer_text, font=("Helvetica", 14))
timer_label.pack()

# Text widget to display the output
output_text = tk.Text(app, wrap=tk.WORD, width=60, height=10)
output_text.pack(pady=10)

# Start the application
app.mainloop()
