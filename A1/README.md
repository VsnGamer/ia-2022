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

