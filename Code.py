import random
import json
import os
import streamlit as st

# 2024 F1 Calendar with Tracks (Updated with all races)
tracks = [
    {"track_name": "Bahrain Grand Prix", "location": "Bahrain", "race_date": "2024-03-03", "laps": 57, "length": 5.412},
    {"track_name": "Saudi Arabian Grand Prix", "location": "Jeddah", "race_date": "2024-03-10", "laps": 50, "length": 6.174},
    {"track_name": "Australian Grand Prix", "location": "Melbourne", "race_date": "2024-03-24", "laps": 58, "length": 5.303},
    {"track_name": "Azerbaijan Grand Prix", "location": "Baku", "race_date": "2024-04-28", "laps": 51, "length": 6.003},
    {"track_name": "Miami Grand Prix", "location": "Miami, USA", "race_date": "2024-05-05", "laps": 57, "length": 5.41},
    {"track_name": "Spanish Grand Prix", "location": "Barcelona", "race_date": "2024-06-02", "laps": 66, "length": 4.675},
    {"track_name": "Monaco Grand Prix", "location": "Monte Carlo", "race_date": "2024-05-26", "laps": 78, "length": 3.337},
    {"track_name": "Austrian Grand Prix", "location": "Spielberg", "race_date": "2024-07-07", "laps": 71, "length": 4.318},
    {"track_name": "British Grand Prix", "location": "Silverstone", "race_date": "2024-07-14", "laps": 52, "length": 5.891},
    {"track_name": "Hungarian Grand Prix", "location": "Budapest", "race_date": "2024-07-21", "laps": 70, "length": 4.381},
    {"track_name": "Belgian Grand Prix", "location": "Spa-Francorchamps", "race_date": "2024-07-28", "laps": 44, "length": 7.004},
    {"track_name": "Dutch Grand Prix", "location": "Zandvoort", "race_date": "2024-08-25", "laps": 72, "length": 4.259},
    {"track_name": "Italian Grand Prix", "location": "Monza", "race_date": "2024-09-01", "laps": 53, "length": 5.793},
    {"track_name": "Singapore Grand Prix", "location": "Singapore", "race_date": "2024-09-15", "laps": 61, "length": 5.063},
    {"track_name": "Japanese Grand Prix", "location": "Suzuka", "race_date": "2024-09-22", "laps": 53, "length": 5.807},
    {"track_name": "Qatar Grand Prix", "location": "Losail", "race_date": "2024-09-29", "laps": 57, "length": 5.380},
    {"track_name": "United States Grand Prix", "location": "Austin, Texas", "race_date": "2024-10-20", "laps": 56, "length": 5.513},
    {"track_name": "Mexican Grand Prix", "location": "Mexico City", "race_date": "2024-10-27", "laps": 71, "length": 4.304},
    {"track_name": "Brazilian Grand Prix", "location": "São Paulo", "race_date": "2024-11-03", "laps": 71, "length": 4.309},
    {"track_name": "Las Vegas Grand Prix", "location": "Las Vegas, USA", "race_date": "2024-11-16", "laps": 50, "length": 6.120},
    {"track_name": "Abu Dhabi Grand Prix", "location": "Yas Marina", "race_date": "2024-11-24", "laps": 58, "length": 5.281},
]

# 2024 F1 Drivers with team assignments
drivers = {
    "Max Verstappen": {"team": "Red Bull Racing", "speed": 98, "strategy": 95, "consistency": 97, "aggression": 98},
    "Sergio Perez": {"team": "Red Bull Racing", "speed": 92, "strategy": 90, "consistency": 88, "aggression": 82},
    "Lewis Hamilton": {"team": "Mercedes", "speed": 95, "strategy": 92, "consistency": 88, "aggression": 80},
    "George Russell": {"team": "Mercedes", "speed": 93, "strategy": 89, "consistency": 85, "aggression": 77},
    "Charles Leclerc": {"team": "Ferrari", "speed": 93, "strategy": 88, "consistency": 85, "aggression": 84},
    "Carlos Sainz": {"team": "Ferrari", "speed": 91, "strategy": 85, "consistency": 84, "aggression": 80},
    "Lando Norris": {"team": "McLaren", "speed": 92, "strategy": 86, "consistency": 83, "aggression": 79},
    "Oscar Piastri": {"team": "McLaren", "speed": 89, "strategy": 83, "consistency": 80, "aggression": 75},
    "Esteban Ocon": {"team": "Alpine", "speed": 88, "strategy": 82, "consistency": 80, "aggression": 70},
    "Pierre Gasly": {"team": "Alpine", "speed": 90, "strategy": 84, "consistency": 81, "aggression": 73},
    "Fernando Alonso": {"team": "Aston Martin", "speed": 90, "strategy": 91, "consistency": 85, "aggression": 78},
    "Lance Stroll": {"team": "Aston Martin", "speed": 85, "strategy": 80, "consistency": 78, "aggression": 72},
    "Valtteri Bottas": {"team": "Alfa Romeo", "speed": 87, "strategy": 82, "consistency": 79, "aggression": 71},
    "Guanyu Zhou": {"team": "Alfa Romeo", "speed": 84, "strategy": 80, "consistency": 77, "aggression": 70},
    "Yuki Tsunoda": {"team": "AlphaTauri", "speed": 85, "strategy": 79, "consistency": 76, "aggression": 83},
    "Liam Lawson": {"team": "AlphaTauri", "speed": 82, "strategy": 76, "consistency": 75, "aggression": 68},
    "Alexander Albon": {"team": "Williams", "speed": 86, "strategy": 81, "consistency": 78, "aggression": 70},
    "Franco Colapinto": {"team": "Williams", "speed": 90, "strategy": 75, "consistency": 74, "aggression": 77}
}

# 2024 F1 Teams with performance and reliability ratings
teams = {
    "Red Bull Racing": {"performance": 98, "reliability": 95},
    "Mercedes": {"performance": 93, "reliability": 90},
    "Ferrari": {"performance": 90, "reliability": 85},
    "McLaren": {"performance": 87, "reliability": 80},
    "Alpine": {"performance": 85, "reliability": 78},
    "Aston Martin": {"performance": 88, "reliability": 82},
    "Alfa Romeo": {"performance": 80, "reliability": 75},
    "RB Visa Cash App": {"performance": 75, "reliability": 70},
    "Williams": {"performance": 70, "reliability": 68}
}

# Function to create a new driver
def create_driver():
    name = st.text_input("Enter your driver's name:")
    speed = st.number_input("Enter driver's speed (0-100):", min_value=0, max_value=100)
    strategy = st.number_input("Enter driver's strategy (0-100):", min_value=0, max_value=100)
    consistency = st.number_input("Enter driver's consistency (0-100):", min_value=0, max_value=100)
    aggression = st.number_input("Enter driver's aggression (0-100):", min_value=0, max_value=100)
    
    if st.button("Create Driver"):
        driver = {name: {"team": "Custom Team", "speed": speed, "strategy": strategy, "consistency": consistency, "aggression": aggression}}
        st.write(f"Your driver {name} has been created!")
        return driver
    return None

# Function to create a new team
def create_team():
    name = st.text_input("Enter your team's name:")
    performance = st.number_input("Enter team's performance (0-100):", min_value=0, max_value=100)
    reliability = st.number_input("Enter team's reliability (0-100):", min_value=0, max_value=100)
    
    if st.button("Create Team"):
        team = {name: {"performance": performance, "reliability": reliability}}
        st.write(f"Your team {name} has been created!")
        return team
    return None

# Function to simulate a race
def race(driver, team, track):
    st.write(f"Starting the race at {track['track_name']} in {track['location']}!")
    
    # Driver and team performance for the race
    driver_skill = driver['speed'] + driver['strategy'] + driver['consistency'] + driver['aggression']
    team_performance = team['performance'] + team['reliability']
    
    race_result = random.randint(driver_skill + team_performance - 20, driver_skill + team_performance + 20)
    st.write(f"Race finished! Your performance score: {race_result}")
    
    return race_result

# Saving the game state to a file
def save_game(driver_name, driver, team_name, team):
    save_data = {
        "driver": driver,
        "team": team,
        "tracks": tracks,
    }
    
    filename = f"{driver_name}_{team_name}_save.json"
    
    with open(filename, "w") as file:
        json.dump(save_data, file)
    st.write(f"Game saved as {filename}!")

# Loading the game state from a file
def load_game(driver_name, team_name):
    filename = f"{driver_name}_{team_name}_save.json"
    
    if os.path.exists(filename):
        with open(filename, "r") as file:
            save_data = json.load(file)
        st.write(f"Game loaded from {filename}!")
        return save_data
    else:
        st.write("No save file found.")
        return None

# Main Game Function
def main():
    st.title("F1 Career Simulator")
    
    # Choose to create a custom driver or use an existing one
    choice = st.radio("Do you want to create your own driver?", ("Yes", "No"))
    if choice == "Yes":
        driver = create_driver()
    else:
        driver = drivers["Max Verstappen"]  # Default to Max Verstappen if no custom driver
    
    # Choose to create a custom team or use an existing one
    choice = st.radio("Do you want to create your own team?", ("Yes", "No"))
    if choice == "Yes":
        team = create_team()
    else:
        team = teams["Red Bull Racing"]  # Default to Red Bull Racing if no custom team
    
    # Simulate a race
    for track in tracks:
        race_result = race(driver[list(driver.keys())[0]], team[list(team.keys())[0]], track)
    
    # Save the game
    save_choice = st.button("Save Game")
    if save_choice:
        driver_name = list(driver.keys())[0]
        team_name = list(team.keys())[0]
        save_game(driver_name, driver[driver_name], team_name, team[team_name])

# Run the game
if __name__ == "__main__":
    main()
