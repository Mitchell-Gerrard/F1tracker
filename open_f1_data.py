import requests
import pandas as pd

class OpenF1LiveData:
    BASE_URL = "https://api.openf1.org/v1"

    def __init__(self, event_name="austin", year=2024, session_type="race"):
        self.session_id = self.get_session_id(event_name, year, session_type)
        if not self.session_id:
            raise ValueError(f"Could not find session for {event_name} {year} - {session_type}")

    def get_session_id(self, event_name, year, session_type):
        url = f"{self.BASE_URL}/sessions"
        response = requests.get(url)
        if response.status_code == 200:
            sessions = response.json()
            for session in sessions:
                if (session["circuit_short_name"].lower() == event_name.lower() and
                    session["year"] == year and
                    session["session_type"].lower() == session_type.lower()):
                    self.session_id = session["session_key"]
                    self.session_start_time = pd.to_datetime(session["date_start"])
                   
                    return session['session_key']
        return None

    def get_live_data(self):
        if not self.session_id:
            return None
        url = f"{self.BASE_URL}/live?session_id={self.session_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return self.process_data(response.json())
        return None

    def get_data_in_time_range(self, cental_time_offset):
        start_time =pd.Timedelta(seconds=cental_time_offset) +self.session_start_time-pd.Timedelta(seconds=30) 
        end_time = pd.Timedelta(seconds=cental_time_offset) +self.session_start_time+pd.Timedelta(seconds=30) 

        if not self.session_id:
            return None

        url = (
            f"{self.BASE_URL}/car_data?"
            f"session_key={self.session_id}"
            f"&date%3E{start_time.isoformat()}"  # Start time: date%3E (greater than)
            f"&date%3C{end_time.isoformat()}"    # End time: date%3C (less than)
        )

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            data=pd.DataFrame(data)

            
            return data
        return None

    def get_first_lap_data(self):
        if not self.session_id:
            return None
        url = f"{self.BASE_URL}/session-data?session_key={self.session_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return self.process_data(data, lap_filter=1)
        return None

    def get_lap_data(self, session_name=None):

        url = f"{self.BASE_URL}/laps?session_key={self.session_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        return None

    def get_available_events(self, year):
        url = f"{self.BASE_URL}/sessions"
        response = requests.get(url)

        if response.status_code == 200:
            sessions = response.json()
            # Only include events where the session year matches the provided year
            return list(set([session['circuit_short_name'] for session in sessions if session.get('year') == year]))
        return []

    def get_available_sessions(self, event_name,year):
        url = f"{self.BASE_URL}/sessions"
        response = requests.get(url)
        if response.status_code == 200:
            sessions = response.json()
            return list(set([session['session_type'] for session in sessions if session['circuit_short_name'].lower() == event_name.lower() and session.get('year') == year]))
        return []