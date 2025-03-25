from apscheduler.schedulers.background import BackgroundScheduler
import time
from watcher import watch_one_time

def my_function():
    print("Function is called!")
    watch_one_time()

# Create a scheduler instance
scheduler = BackgroundScheduler()

# Schedule the function to run every 10 seconds
scheduler.add_job(my_function, 'interval', seconds=120)

# Start the scheduler
scheduler.start()

try:
    # Keep the script running
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler on exit
    scheduler.shutdown()