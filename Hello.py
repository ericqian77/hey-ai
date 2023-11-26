import streamlit as st
import numpy as np
import time

# Function to update the board for the next generation
def update_board(board):
    new_board = board.copy()
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            live_neighbors = np.sum(board[max(i-1, 0):min(i+2, board.shape[0]), max(j-1, 0):min(j+2, board.shape[1])]) - board[i, j]
            if board[i, j] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                new_board[i, j] = 0
            elif board[i, j] == 0 and live_neighbors == 3:
                new_board[i, j] = 1
    return new_board

# Function to draw the board on Streamlit
def draw_board(board):
    board_display = ""
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == 1:
                board_display += '⬛'
            else:
                board_display += '⬜'
        board_display += '\n'
    return board_display

def main():
    st.title("hey! welcome to the unexpected")
    st.markdown("Dive into a world where each learning step opens doors to new, unforeseen possibilities. Here, your growth isn't just step by step – it's leaps and bounds. Stick around, and let's see where this journey takes us! .")

    # Sidebar for configuration
    st.sidebar.title("Configuration")
    board_size = st.sidebar.slider("Board Size", 5, 30, 20)
    speed = st.sidebar.slider("Speed (iterations per second)", 1, 20, 5)
    if 'board' not in st.session_state or st.sidebar.button('Reset Board'):
        st.session_state.board = np.random.randint(2, size=(board_size, board_size))

    # Placeholder for the board
    board_placeholder = st.empty()

    # Start and stop buttons
    if st.sidebar.button('Start / Resume'):
        st.session_state.running = True
    if st.sidebar.button('Pause'):
        st.session_state.running = False

    # Main loop
    while st.session_state.get('running', False):
        start_time = time.time()
        board_placeholder.markdown(draw_board(st.session_state.board), unsafe_allow_html=True)
        st.session_state.board = update_board(st.session_state.board)
        st.sidebar.text("Running...")
        # Control the speed of updates
        elapsed_time = time.time() - start_time
        time.sleep(max(0, 1.0/speed - elapsed_time))
        st.experimental_rerun()

    # Display the board when not running
    if not st.session_state.get('running', False):
        board_placeholder.markdown(draw_board(st.session_state.board), unsafe_allow_html=True)
        st.sidebar.text("Paused")

if __name__ == "__main__":
    main()
