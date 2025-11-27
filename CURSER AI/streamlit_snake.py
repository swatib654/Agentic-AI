"""
Streamlit-based Snake game.

Run with: streamlit run streamlit_snake.py
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import streamlit as st


GRID_WIDTH = 20
GRID_HEIGHT = 20

Direction = Tuple[int, int]


@dataclass
class GameState:
    snake: List[Tuple[int, int]]
    direction: Direction
    food: Tuple[int, int]
    alive: bool
    score: int


def init_game() -> None:
    if "snake_state" in st.session_state:
        return

    start = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    st.session_state.snake_state = GameState(
        snake=[start, (start[0] - 1, start[1])],
        direction=(1, 0),
        food=random_food({start, (start[0] - 1, start[1])}),
        alive=True,
        score=0,
    )


def reset_game() -> None:
    if "snake_state" in st.session_state:
        del st.session_state.snake_state
    init_game()


def random_food(occupied: set[Tuple[int, int]]) -> Tuple[int, int]:
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in occupied:
            return position


def change_direction(new_direction: Direction) -> None:
    state = st.session_state.snake_state
    opposite = (-state.direction[0], -state.direction[1])
    if new_direction != opposite:
        state.direction = new_direction


def advance_snake() -> None:
    state = st.session_state.snake_state
    if not state.alive:
        return

    head_x, head_y = state.snake[0]
    dx, dy = state.direction
    new_head = (head_x + dx, head_y + dy)

    hit_wall = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
    hit_self = new_head in state.snake
    if hit_wall or hit_self:
        state.alive = False
        return

    state.snake.insert(0, new_head)
    if new_head == state.food:
        state.score += 1
        state.food = random_food(set(state.snake))
    else:
        state.snake.pop()


def render_board(state: GameState) -> None:
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, GRID_WIDTH)
    ax.set_ylim(0, GRID_HEIGHT)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.set_aspect("equal")

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            ax.add_patch(Rectangle((x, y), 1, 1, fill=False, linewidth=0.1, edgecolor="#DDDDDD"))

    for idx, (x, y) in enumerate(state.snake):
        color = "#2E8B57" if idx == 0 else "#66CDAA"
        ax.add_patch(Rectangle((x, y), 1, 1, color=color))

    fx, fy = state.food
    ax.add_patch(Rectangle((fx, fy), 1, 1, color="#CD5C5C"))

    st.pyplot(fig)


def main() -> None:
    st.set_page_config(page_title="Streamlit Snake", layout="wide")
    st.title("Snake Game (Streamlit)")

    init_game()
    state = st.session_state.snake_state

    with st.sidebar:
        st.subheader("Controls")
        st.write("Use direction buttons before advancing to set the heading.")
        col_up = st.columns([1, 1, 1])
        with col_up[1]:
            if st.button("Up"):
                change_direction((0, -1))
        col_mid = st.columns([1, 1, 1])
        with col_mid[0]:
            if st.button("Left"):
                change_direction((-1, 0))
        with col_mid[2]:
            if st.button("Right"):
                change_direction((1, 0))
        col_down = st.columns([1, 1, 1])
        with col_down[1]:
            if st.button("Down"):
                change_direction((0, 1))

        st.divider()
        if st.button("Advance Step"):
            advance_snake()
        if st.button("New Game"):
            reset_game()
            st.rerun()

        st.markdown(f"**Score:** {state.score}")
        st.markdown(f"**Status:** {'Alive' if state.alive else 'Game over'}")

    render_board(state)
    if not state.alive:
        st.info("Snake crashed! Start a new game to try again.")


if __name__ == "__main__":
    main()

