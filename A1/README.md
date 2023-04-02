# IART Assignment 1 - **Cohesion** puzzle 

## Summary

Cohesion is a puzzle similar to the N-puzzle sliding game. Instead of numbers there are colored blocks. When two blocks of the same color touch, they merge into a single block. The goal is to merge all the blocks of the same color into a single block, leaving the puzzle with the same number of blocks and colors.

For example if the initial state is:

```
|R G   G|
|       |
|R     G|
|       |
```

There are 2 colors R(red) and G(green) and 5 separate blocks.

If we move the green block in the top right corner to the left, we get:

```
|R G G  |
|       |
|R     G|
|       |
```

Now we have 2 blocks of color R and 2 blocks of color G. If we move the red block in the bottom left corner up, we get:

```
|R G G  |
|R      |
|      G|
|       |
```

Now we have 1 block of color R. All that's left is to move the block in the bottom right corner up twice to reach a solution:

```
|R G G G|
|R      |
|       |
|       |
```

We have reached a solution because we have 1 block of each color.

If we had another block of color B(blue) in the initial state and reached the following state:

```
|R G G G|
|R      |
|       |
|      B|
```

It would also be a solution, because we have one single block of each color.

It is possible to reach a state where it is impossible to merge any blocks, even if we can move them. For example:

```
|R G G G|
|R      |
|B B B B|
|      R|
```

In this case, we have 2 blocks of color red, but we can't merge them because they are separated by a blue block and there is no way to move the blue block out of the way or move the red blocks together. Thus this is effectively a dead end and we can't reach a solution from this state.

## Setup

Install requirements:

```bash
pip install -r requirements.txt
```

Run the program:

```bash
python3 cohesion
```

## Usage

You will be presented with a menu with the following options:

```bash
1. Play
2. Solve
```

### Play

This option will let you play the game. You will be presented with a puzzle and you can move the blocks around with the mouse. When you click on a block it will be selected and you can move it by dragging it in the desired direction.

You can also undo your moves by pressing backspace.

### Solve

This option will enter the solver demo mode.

It will generate and solve the puzzle until it finds a solution or you can press escape to cancel the search.

To generate a new puzzle just click anywhere on the screen.

#### Tweaking the solver

You can mess around with the parameters and heuristics in `__main__.py` in the `solve` function.

There is `draw_path` which takes a node(returned by the algorithm) found by the solver and animates the steps taken to reach the solution.

The `measure_search` serves only to measure the time it takes to find a solution and print it to the console, it will return the solution node found by the algorithm.


