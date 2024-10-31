import requests
import threading
import time
from datetime import datetime, timedelta

QUERY_FREQUENCY = 1  # Query data every 3 seconds
DELAY = 3  # Delay between the event on track and the speedometer (10 seconds)

# Shared buffer for holding the latest speed data
buffer = []
buffer_lock = threading.Lock()

def fetch_speed_data():
    last_query_time = datetime.now() - timedelta(seconds=DELAY)
    while True:
        try:
            # Format the timestamp for the API call
            formatted_time = last_query_time.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
            url = f"https://api.openf1.org/v1/car_data?driver_number=1&session_key=latest&date>{formatted_time}"
            response = requests.get(url)
            data = response.json()
            
            with buffer_lock:
                buffer.extend(data)  # Add new data to the buffer
                
            # Update last_query_time to the time of the last data point received
            if data:
                last_query_time = datetime.strptime(data[-1]['date'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
            
            time.sleep(QUERY_FREQUENCY)  # Wait for a few seconds before next API call
        except Exception as e:
            print(f"Error fetching speed data: {e}")
            time.sleep(QUERY_FREQUENCY)  # In case of an error, wait before trying again

def display_speed_data():
    while True:
        with buffer_lock:
            if buffer:
                # Take the most recent value and remove it from the buffer
                current = buffer.pop(0)
                date = datetime.strptime(current['date'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
                waiting_time = max(0, DELAY - (datetime.now() - date).total_seconds())
                time.sleep(waiting_time)
                print(f"Current Speed: {current['speed']} km/h")
            else:
                pass
                #print("Waiting for new speed data...")

# Start the data fetching thread
fetching_thread = threading.Thread(target=fetch_speed_data)
fetching_thread.start()

# Start the display thread
display_thread = threading.Thread(target=display_speed_data)
display_thread.start()
