# CommandGOLF
# by Adam Wickwire
# 2.3.2024
#
# CommandGOLF is a command-line interface (CLI) golf game built in Python, offering a 
# simplified yet captivating golfing experience directly from your terminal. Engage in a 
# game of golf where strategy, club selection, and dealing with the whims of the wind 
# come together to challenge your path to the least number of swings to get the ball in 
# the hole. The game is designed to be played in a single-player mode, with the option to
# play 1, 9, or 18 holes. The game also includes a wind mechanic that can affect the
# distance of your shots, adding an extra layer of complexity to your golfing strategy.
# 



import random

def generate_wind():
    directions = ['headwind', 'tailwind', 'crosswind']
    strength = random.randint(1, 5)  # Wind strength on a scale from 1 to 5
    wind_direction = random.choice(directions)
    print(f"Wind condition: {wind_direction} with a strength of {strength}")
    return wind_direction, strength

def adjust_distance_for_wind(swing_distance, wind_direction, wind_strength):
    if wind_direction == 'headwind':
        return max(swing_distance - wind_strength, 0)  # Reduce distance, don't go negative
    elif wind_direction == 'tailwind':
        return swing_distance + wind_strength  # Increase distance
    else:  # For simplicity, we won't adjust distance for crosswind in this example
        return swing_distance

def choose_club(clubs, on_green, current_distance=None, hole_distance=None):
    if on_green:
        print("\nYou're on the green. Use the putter.")
        return "putter"
    else:
        if current_distance is not None and hole_distance is not None:
            print(f"\nDistance to hole: {hole_distance - current_distance} yards. Choose wisely!")
        print("\nAvailable clubs and their average stock yardages:")
        for club, info in clubs.items():
            if club != "putter":  # Exclude putter from regular play options
                print(f"- {club.capitalize()}: {info['stock']} yards")
        
        while True:
            club_choice = input("Choose your club: ").lower()
            if club_choice in clubs and club_choice != "putter":
                return club_choice
            else:
                print("Invalid choice. Please select a valid club from the list above.")

def swing(club, clubs, current_distance, hole_distance, on_green, wind_direction, wind_strength):
    if on_green:
        remaining_distance = round(abs(hole_distance - current_distance) * 3)  # Convert yards to feet and round
        print(f"You're on the green, {remaining_distance} feet from the hole.")
        tolerance = 2  # Tolerance in feet for a successful putt
        
        power_factor = int(input("Choose your putting strength (1-10): "))
        putt_distance = power_factor * 3  # Simplified putt distance calculation
        
        # Calculate new remaining distance after the putt, ensuring it's rounded for realistic gameplay
        new_remaining_distance = round(abs(remaining_distance - putt_distance))
        
        if new_remaining_distance <= tolerance:
            print("Great putt! You've made it into the hole!")
            return hole_distance, True
        else:
            print(f"Your ball is now {new_remaining_distance} feet from the hole.")
            # Convert the remaining distance back to yards for consistency if not in the hole yet, rounding as necessary
            return (hole_distance - round(new_remaining_distance / 3)), False
    else:
        print("\nSwinging with the", club)
        power_factor = int(input("Choose your swing strength (1-10): "))
        random_factor = random.randint(clubs[club]["random_factor"][1], clubs[club]["random_factor"][0])
        swing_distance = clubs[club]["stock"] + random_factor + (power_factor * 2)
        adjusted_distance = adjust_distance_for_wind(swing_distance, wind_direction, wind_strength)
        new_distance = current_distance + adjusted_distance
        if abs(hole_distance - new_distance) <= 5:
            print("What a shot! You've landed in the hole!")
            return hole_distance, True
        else:
            print(f"After your swing, the ball is now {abs(hole_distance - new_distance)} yards from the hole.")
            return new_distance, False

def golf_game():
    print("Welcome to the Backyard Loop Golf Game!")
    print("Rules: Try to get the ball in the hole in the fewest swings.")
    
    clubs = {
        "driver": {"stock": 250, "random_factor": (5, -2)},
        "fairway wood": {"stock": 220, "random_factor": (4, -2)},
        "long iron": {"stock": 180, "random_factor": (3, -2)},
        "short iron": {"stock": 140, "random_factor": (3, -2)},
        "long wedge": {"stock": 95, "random_factor": (2, -1)},
        "short wedge": {"stock": 55, "random_factor": (2, -1)},
        "chip": {"stock": 12, "random_factor": (1, -1)},
        "putter": {"stock": 5, "random_factor": (0, 0)}
    }

    # Ask player for the number of holes
    while True:
        try:
            num_holes = int(input("\nHow many holes would you like to play? (1, 9, 18): "))
            if num_holes in [1, 9, 18]:
                break
            else:
                print("Please choose 1, 9, or 18 holes.")
        except ValueError:
            print("Please enter a valid number.")
    
    scorecard = []
    
    for hole in range(1, num_holes + 1):
        print(f"\nHole {hole} setup:")
        hole_distance = random.randint(100, 500)
        print(f"The hole is {hole_distance} yards away.")
        wind_direction, wind_strength = generate_wind()
        
        current_distance = 0
        swings = 0
        
        while current_distance != hole_distance:
            on_green = abs(hole_distance - current_distance) <= 20  # Green zone
            club = choose_club(clubs, on_green)
            current_distance, success = swing(club, clubs, current_distance, hole_distance, on_green, wind_direction, wind_strength)
            swings += 1
            
            if success:
                print(f"Hole {hole} completed in {swings} swings.")
                scorecard.append(swings)
                break
        
        # Scorecard update after each hole
        print("\nCurrent Scorecard:")
        for i, score in enumerate(scorecard, 1):
            print(f"Hole {i}: {score} swings")
        print(f"Total so far: {sum(scorecard)} swings over {len(scorecard)} holes.")
        
    # Display the final scorecard
    print("\nYour Scorecard:")
    for i, score in enumerate(scorecard, 1):
        print(f"Hole {i}: {score} swings")
    total_swings = sum(scorecard)
    print(f"Total: {total_swings} swings over {num_holes} holes.")

# Run the game
golf_game()
