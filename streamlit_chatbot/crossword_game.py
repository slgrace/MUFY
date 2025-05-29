import streamlit as st
import random
import time

# Initialize session state
if 'coins' not in st.session_state:
    st.session_state.coins = 100  # Starting coins
if 'current_level' not in st.session_state:
    st.session_state.current_level = "Easy"
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "Animals"
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
word_databases = {
    "Animals": {
        "Easy": ["CAT", "DOG", "OWL", "BAT"],
        "Medium": ["TIGER", "ZEBRA", "PANDA", "KOALA"],
        "Hard": ["ELEPHANT", "KANGAROO", "RHINOCEROS"]
    },
    "Countries": {
        "Easy": ["USA", "UK", "JPN", "GER"],
        "Medium": ["BRAZIL", "CANADA", "FRANCE"],
        "Hard": ["AUSTRALIA", "ARGENTINA", "INDONESIA"]
    },
    # Add more themes...
}
def display_puzzle():
    theme = st.session_state.current_theme
    level = st.session_state.current_level
    
    # Select random word
    word = random.choice(word_databases[theme][level])
    word = word.upper()
    length = len(word)
    
    # Determine which letters to reveal (about 30%)
    reveal_count = max(1, int(length * 0.3))
    reveal_positions = sorted(random.sample(range(length), reveal_count))
    
    # Display puzzle
    st.subheader(f"Theme: {theme} | Level: {level}")
    st.write(f"Word length: {length} letters")
    
    # Show revealed letters
    cols = st.columns(length)
    for i in range(length):
        if i in reveal_positions:
            cols[i].write(f"**{word[i]}**")
        else:
            cols[i].write("_")
    
    # User input
    guess = st.text_input("Enter your guess:").upper()
    
    if st.button("Submit Guess"):
        if guess == word:
            time_taken = time.time() - st.session_state.start_time
            coins_earned = calculate_reward(time_taken, level)
            st.session_state.coins += coins_earned
            st.success(f"Correct! You earned {coins_earned} coins!")
            st.session_state.game_active = False
        else:
            st.error("Incorrect! Try again.")
    
    # Clue purchase option
    if st.session_state.coins >= 20:
        if st.button("Buy Clue (20 coins)"):
            st.session_state.coins -= 20
            # Reveal one additional letter
            hidden_positions = [i for i in range(length) if i not in reveal_positions]
            if hidden_positions:
                reveal_positions.append(random.choice(hidden_positions))
                st.experimental_rerun()
def calculate_reward(time_taken, level):
    base_rewards = {"Easy": 50, "Medium": 100, "Hard": 200}
    time_bonus = max(0, (60 - time_taken) * 2)  # Bonus for speed
    
    # Penalty for using clues
    clue_penalty = st.session_state.get('clues_used', 0) * 10
    
    total = base_rewards[level] + time_bonus - clue_penalty
    return max(10, total)  # Ensure minimum reward  
def main():
    st.title("🧩 Crossword Puzzle Challenge")
    
    # Display player stats
    st.sidebar.header("Player Stats")
    st.sidebar.write(f"💰 Gold Coins: {st.session_state.coins}")
    
    # Level and theme selection
    st.session_state.current_level = st.sidebar.selectbox(
        "Select Level", ["Easy", "Medium", "Hard"])
    st.session_state.current_theme = st.sidebar.selectbox(
        "Select Theme", list(word_databases.keys()))
    
    if not st.session_state.game_active:
        if st.button("Start New Puzzle"):
            st.session_state.game_active = True
            st.session_state.start_time = time.time()
            st.session_state.clues_used = 0
            st.experimental_rerun()
    else:
        display_puzzle()
    
    # Shop section
    st.sidebar.header("Shop")
    st.sidebar.write("Coming soon: More power-ups and avatars!")

if __name__ == "__main__":
    main()                  