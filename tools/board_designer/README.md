# Board Designer

`board_designer.py` is a small Tkinter tool for drafting obstacle layouts without manually counting coordinates.

Run it from the repository root:

```bash
python tools/board_designer/board_designer.py
```

1. Set the width and height.
2. Click or drag on the grid to draw obstacles. Click an existing obstacle to erase it.
3. Select **Generate Code**.
4. Copy the generated configuration into a new module in `boards/`, such as `boards/my_board.py`.
5. Update the name, win length, player count, or time limit as needed.
6. Run `python main.py` to include your board in the next tournament.

The game discovers valid board modules automatically; no registration step is required.