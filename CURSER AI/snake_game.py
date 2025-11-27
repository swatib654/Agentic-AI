"""
Simple Snake game using pygame.

Run with: python snake_game.py
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from typing import List, Tuple

import pygame

GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 22
WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * GRID_SIZE
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)


Direction = Tuple[int, int]


@dataclass
class Snake:
    body: List[pygame.Vector2]
    direction: Direction

    def head(self) -> pygame.Vector2:
        return self.body[0]

    def move(self, grow: bool = False) -> None:
        new_head = self.head() + pygame.Vector2(self.direction)
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def change_direction(self, new_direction: Direction) -> None:
        # prevent reversing into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def collides_with_self(self) -> bool:
        return any(segment == self.head() for segment in self.body[1:])


def random_food_position(snake: Snake) -> pygame.Vector2:
    while True:
        position = pygame.Vector2(
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1),
        )
        if position not in snake.body:
            return position


def draw_block(surface: pygame.Surface, position: pygame.Vector2, color: Tuple[int, int, int]) -> None:
    rect = pygame.Rect(position.x * GRID_SIZE, position.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    snake = Snake(
        body=[pygame.Vector2(GRID_WIDTH // 2, GRID_HEIGHT // 2)],
        direction=(1, 0),
    )
    food = random_food_position(snake)
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        snake.move()

        if snake.head().x < 0 or snake.head().x >= GRID_WIDTH or snake.head().y < 0 or snake.head().y >= GRID_HEIGHT:
            break

        if snake.collides_with_self():
            break

        if snake.head() == food:
            score += 1
            snake.move(grow=True)
            food = random_food_position(snake)

        screen.fill(BLACK)
        draw_block(screen, food, RED)
        for segment in snake.body:
            draw_block(screen, segment, GREEN)

        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

    game_over_screen(screen, font, score)


def game_over_screen(screen: pygame.Surface, font: pygame.font.Font, score: int) -> None:
    message = font.render(f"Game Over! Score: {score}", True, WHITE)
    info = font.render("Press any key to exit", True, WHITE)
    screen.blit(message, (WINDOW_WIDTH // 2 - message.get_width() // 2, WINDOW_HEIGHT // 3))
    screen.blit(info, (WINDOW_WIDTH // 2 - info.get_width() // 2, WINDOW_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

