# Contributing to X-in-Line

The goal is a growing collection of fair, interesting bot challenges. Contributions should make the tournament more fun to play, easier to understand, or more reliable to run.

## Before You Start

1. Fork the repository.
2. Create a focused branch, such as `add-corner-hunter-bot` or `add-labyrinth-board`.
3. Run `python main.py` before and after your change.

## Bots

- Add one module per bot in `bots/`.
- Inherit from `BaseBot`.
- Give the class and file a descriptive, unique name.
- Return only legal coordinates from `make_a_move()`.
- Keep the strategy within the board's move time budget.
- Explain the strategy and any trade-offs in your pull request.

## Boards

- Add one module per board in `boards/`.
- Define every required constant: `BOARD_NAME`, `BOARD_WIDTH`, `BOARD_HEIGHT`, `WIN_LENGTH`, `NUM_PLAYERS`, `OBSTACLES`, and `GAME_TIME_MS`.
- Choose a unique board name and a filename that describes the map.
- Check that obstacles are inside the board bounds.
- Include a short description and explain the strategic challenge in the pull request.

You can use `python tools/board_designer/board_designer.py` to create an obstacle layout, then paste its generated code into the new board module.

## Pull Requests

- Keep each pull request focused on one bot, one board, or one improvement.
- Do not commit files in `logs/`.
- Include the command you ran and a short summary of the observed tournament behaviour.
- Be constructive when reviewing competing strategies. The point is to keep the competition alive.