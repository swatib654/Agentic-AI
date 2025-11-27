"""
Streamlit mini carrom practice board.

Run locally with: streamlit run carrom_app.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import streamlit as st


BOARD_SIZE = 100
STRIKER_START = (50.0, 8.0)
MAX_TRAVEL = 65.0
POCKETS = [
    (5.0, 5.0),
    (95.0, 5.0),
    (5.0, 95.0),
    (95.0, 95.0),
]


@dataclass
class Coin:
    x: float
    y: float
    color: str
    value: int

    @property
    def position(self) -> Tuple[float, float]:
        return self.x, self.y

    def move(self, dx: float, dy: float) -> None:
        self.x = min(max(self.x + dx, 8.0), 92.0)
        self.y = min(max(self.y + dy, 8.0), 92.0)


def init_state() -> None:
    if "coins" in st.session_state:
        return

    coins: List[Coin] = []
    # queen
    coins.append(Coin(50.0, 50.0, "crimson", 5))
    # arrange white & black coins in a ring
    ring_r = 8.0
    for idx in range(6):
        angle = math.radians(60 * idx)
        coins.append(
            Coin(
                50.0 + ring_r * math.cos(angle),
                50.0 + ring_r * math.sin(angle),
                "white",
                2,
            )
        )
    for idx in range(6):
        angle = math.radians(60 * idx + 30)
        coins.append(
            Coin(
                50.0 + ring_r * math.cos(angle),
                50.0 + ring_r * math.sin(angle),
                "black",
                1,
            )
        )

    st.session_state.coins = coins
    st.session_state.score = 0
    st.session_state.history = []


def reset_board() -> None:
    for key in ("coins", "score", "history"):
        if key in st.session_state:
            del st.session_state[key]
    init_state()


def unit_vector_from_angle(angle_degrees: float) -> Tuple[float, float]:
    """Angle 0 shoots straight up, positive angles go right, negative go left."""
    radians = math.radians(angle_degrees)
    return math.sin(radians), math.cos(radians)


def find_hit_coin(direction: Tuple[float, float]) -> Tuple[Coin | None, float]:
    striker = STRIKER_START
    best_coin = None
    best_distance = float("inf")
    for coin in st.session_state.coins:
        vx = coin.x - striker[0]
        vy = coin.y - striker[1]
        proj = vx * direction[0] + vy * direction[1]
        if proj <= 0:
            continue
        # perpendicular distance from path
        perp_sq = (vx * vx + vy * vy) - proj * proj
        if perp_sq < 9.0 and proj < best_distance:  # threshold ~ striker diameter
            best_coin = coin
            best_distance = proj
    return best_coin, best_distance


def pocket_if_scored(coin: Coin) -> bool:
    for px, py in POCKETS:
        if (coin.x - px) ** 2 + (coin.y - py) ** 2 <= 20.0:
            return True
    return False


def handle_strike(angle: float, power: float) -> str:
    direction = unit_vector_from_angle(angle)
    coin, distance = find_hit_coin(direction)

    if not coin:
        return "Missed every coin! Adjust the angle."

    travel = min(MAX_TRAVEL * power, MAX_TRAVEL)
    coin.move(direction[0] * travel, direction[1] * travel)

    if pocket_if_scored(coin):
        st.session_state.coins.remove(coin)
        st.session_state.score += coin.value
        st.session_state.history.append(
            f"Pocketed a {coin.color} coin (+{coin.value})"
        )
        return f"Pocketed a {coin.color} coin!"
    st.session_state.history.append(
        f"Hit a {coin.color} coin but it stayed on board."
    )
    return f"Hit a {coin.color} coin but it stayed on board."


def render_board() -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, BOARD_SIZE)
    ax.set_ylim(0, BOARD_SIZE)
    ax.set_aspect("equal")
    ax.axis("off")

    # base board
    ax.add_patch(Rectangle((2, 2), 96, 96, fill=False, linewidth=3, color="#8B4513"))
    ax.add_patch(Rectangle((8, 8), 84, 84, fill=False, linewidth=1.5, color="#CD853F"))

    for px, py in POCKETS:
        ax.add_patch(Circle((px, py), radius=5, color="black"))

    ax.add_patch(Circle(STRIKER_START, radius=3, color="royalblue"))

    for coin in st.session_state.coins:
        ax.add_patch(Circle(coin.position, radius=3, color=coin.color, ec="black"))

    st.pyplot(fig)


def main() -> None:
    st.set_page_config(page_title="Carrom Practice Board", layout="centered")
    st.title("Carrom Practice Board")
    st.caption("Quick practice UI built with Streamlit and matplotlib.")

    init_state()

    with st.sidebar:
        st.header("Shot Controls")
        angle = st.slider("Aim angle (°)", -60.0, 60.0, 0.0, step=1.0)
        power = st.slider("Power", 0.2, 1.0, 0.7, step=0.05)

        if st.button("Strike!"):
            feedback = handle_strike(angle, power)
            st.toast(feedback)

        if st.button("Reset Board"):
            reset_board()
            st.toast("Board reset.")

        st.markdown(f"**Score:** {st.session_state.score}")
        st.markdown("**Recent shots:**")
        if st.session_state.history:
            for entry in reversed(st.session_state.history[-5:]):
                st.write(f"- {entry}")
        else:
            st.write("Take a shot to see history.")

    render_board()


if __name__ == "__main__":
    main()

