import random
import curses
import sys

def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    if sh < 10 or sw < 20:
        stdscr.addstr(0, 0, "Terminal window too small!")
        stdscr.refresh()
        curses.napms(2000)
        return

    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], '*')  # Changed food icon to '*'

    key = curses.KEY_RIGHT
    score = 0  # Initialize score

    while True:
        # Display the score at the top-left corner
        w.addstr(0, 2, f"Score: {score} ")

        next_key = w.getch()
        if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            key = next_key

        # Check for collision with walls or self
        if (snake[0][0] in [0, sh - 1] or
            snake[0][1] in [0, sw - 1] or
            snake[0] in snake[1:]):
            w.addstr(sh // 2, sw // 2 - 5, "GAME OVER!")
            w.refresh()
            curses.napms(2000)
            break

        # Calculate new head position
        new_head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1

        snake.insert(0, new_head)

        # Check if snake eats the food
        if snake[0] == food:
            score += 1  # Increment score
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], '*')  # Changed food icon to '*'
        else:
            # Remove tail
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Draw snake
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

if __name__ == "__main__":
    curses.wrapper(main)