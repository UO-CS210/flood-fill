# HOWTO flood the cavern

This week's project is an introduction to solving problems using 
_recursive functions_, which are functions that can call themselves.

The project is based on a 2011 problem in the Juilfs programming 
competition.  The problem was to determine how many distinct 
"chambers" there are in a cave like this: 

![Example cave](img/cave1.png)

The cave will be represented as a grid, implemented as a list of 
lists of characters (type `str`).
The default character choices in `config.py` represent stone by `'#'`,
air by `' '` (a space), and water by `'~'`.  With these settings, 
the same cave can be represented like this: 

```text
# # # # # # # # # #
#       #   #     #
#       #   #     #
#           #     #
#       #   #     #
#       #   #     #
#       # # # # # #
#       #         #
#       #         #
# # # # # # # # # #
```

A different choice of characters might work better with a 
screen-reader like JAWS, NVDA, or VoiceOver.  If we change 
config.py to represent 
stone by `'s'`, air by `'*'`, and water by `'w'`, then the textual 
representation will look like this: 

```
s s s s s s s s s s
s * * * s * s * * s
s * * * s * s * * s
s * * * * * s * * s
s * * * s * s * * s
s * * * s * s * * s
s * * * s s s s s s
s * * * s * * * * s
s * * * s * * * * s
s s s s s s s s s s
```

Initially the cave contains no water.  We'll add that soon. 
You will be able to determine that this cave
has three chambers, indicated 
by filling each chamber with a different color of water.

![Example cave filled](img/cave1-filled.png)

or textually 

```text
s s s s s s s s s s
s 1 1 1 s 1 s 2 2 s
s 1 1 1 s 1 s 2 2 s
s 1 1 1 1 1 s 2 2 s
s 1 1 1 s 1 s 2 2 s
s 1 1 1 s 1 s 2 2 s
s 1 1 1 s s s s s s
s 1 1 1 s 3 3 3 3 s
s 1 1 1 s 3 3 3 3 s
s s s s s s s s s s
```

Initially each cell in the grid 
will either be a wall or an empty space.  You will look for cells
containing air.  When 
you find a cell containing air, you will 
pour water into it.  As you know, water naturally spreads out into a 
chamber.  You will write a recursive function to spread it out and 
fill the whole chamber. 

## The usual start

Start building `flood.py` in the usual way, with a header comment, 
import of the `doctest` module, and a main function that will 
execute when the module is run. 

```python
"""Flood-fill to count chambers in a cave.
CS 210 project.
<Your name here>, <date>
Credits: TBD
"""
import doctest


def main():
    doctest.testmod()
    
if __name__ == "__main__":
    main()
```

As usual, this skeleton of a program runs, but it doesn't do 
anything interesting yet. 


## Build and display a cave

A cave is a rectangular grid represented as a list of lists of 
single character strings.  Each cell in the grid (each string) 
represents air, stone, or water.  Initially the open spaces in the 
cave contain air. 

Caves are constructed from cave plans that look like this: 

```
cave 50 10 
hwall 5 0  10
vwall 0 5  50
```

The first line of this specification says that the cave will be 50 
rows, with 10 columns in each row.  Rows and columns are numbered 
like the indexes of a Python list, so the valid rows are 0 to 49, 
and the valid columns are 0 to 9.  

The second line says that the cave has a horizontal wall of stone 
beginning in the cell at row 5, column 0, and extending to the right 
across 10 cells.  

The third line says that the cave has a vertical wall starting in 
the cell at row 0, column 5, and extending downward across 50 cells.

If a stone wall does not pass through a cell in the cave, that cell 
contains air. 

I have provided a module `cave` (file `cave.py`) for building caves. 
Import it. 
We can get started by building a very small cave, based on the 
specification in `data/cave-rect.txt`.  We'll need to import the 
`cave` module in the usual way.  Then we'll use the `read_cave` 
function to read `data/cave-rect.txt`, and the `text` function to 
print it.  Since `cave` is the name of a module, I'll use `cavern` 
as the name of the particular cave we will explore: 

```python
def main():
    doctest.testmod()
    cavern = cave.read_cave("data/cave.txt")
    print(cave.text(cavern))
```

Run this program. This should result in
a primitive printed version of a narrow, deep cave: 

``` 
------------
|##########|
|#   # #  #|
|#   # #  #|
|#     #  #|
|#   # #  #|
|#   # #  #|
|#   ######|
|#   #    #|
|#   #    #|
|##########|
------------
```

## Factor out the cave description path

_Hard coding_ the path `data/cave-rect.txt` into our main program 
was handy for a quick check, but only for that.  We want our program 
to be usable with descriptions of different caves, without editing 
`flood.py`.  

We could prompt the user to provide a file name, but then we'd have 
to enter a path like `data/cave.txt` every time we ran it.  We 
could make it an application that gets the file path from the 
command line.  That might be the best approach, but we haven't 
studied command-line argument parsing with the `argparse` module yet.
Or we could just create a separate small module, `config`, to 
provide this information.  Creating a configuration file seems like 
a reasonable approach for now. 

`config.py` in the same directory as `flood.py` sets a 
variable `CAVE_PATH` to `"data/cave.txt"`.  import `config` into 
`flood.py`.  Then our main function becomes:

```python
def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    print(cave.text(cavern))
```

The program behavior should be the same as before. 

## Viewing the cave

While we can make a call to `cave.text()` to get a printable
version, we may wish to see a graphical version and/or a textual 
version as the program runs.  I have provided a module `cave_view` 
to provide a graphical or textual view.  These are controlled by the 
following lines in `config.py`:

```python
GRAPHIC_DISPLAY = True  # Grid display using Tk
WIN_WIDTH = 300   # Width of graphical display in pixels
WIN_HEIGHT = 300  # Height of graphical display in pixels
TEXTUAL_DISPLAY = True  # Textual depiction of the cavern
```
Of course you can disable either view by 
setting those options to `False` instead.  
 
To support the graphic display, import `cave_view` 
into `flood.py`. 
The functions of `cave_view` that we will 
need are `display`, to create the graphical view, `redisplay` to 
 refresh it, and 
`prompt_to_close`, which we call when we are done to keep the 
graphic showing until the user presses _enter_.   Instead of 
printing `text(cavern)`, let's try displaying it.  Import 
`cave_view` and change the main function again, this time to: 

```python
def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    cave_view.display(cavern, config.WIN_WIDTH, config.WIN_HEIGHT)
    cave_view.prompt_to_close()
```

Now with the graphical display enabled you should see something 
like this: 

![Graphical display of data/cave.txt](img/cave.png)

and with the textual display enabled, with default character choices  
you should see something like 
this: 

```text
# # # # # # # # # #
#       #   #     #
#       #   #     #
#           #     #
#       #   #     #
#       #   #     #
#       # # # # # #
#       #         #
#       #         #
# # # # # # # # # #
```

## Checkpoint

At this point you should have two modules (source code files),
`flood.py` and `config.py`.  Your `flood.py` module imports
`config` as well as `cave` and `cave_view`.  

If you change `config.py` to contain a path to a different cave 
  description, you should get a diagram of a different cave.

## Scanning the cave

To count chambers, we will pour water into each chamber we find, 
while scanning every row and column of the cavern.  Every time we 
encounter air, we'll know that we've found another chamber, and then 
we'll pour water to fill that chamber up (while leaving air in other 
chambers). 

Let's do everything _except_ pouring water for now:  Scan each cell 
of the cavern and count the number of times we encounter air.  The 
header of the function should be: 

```python
def scan_cave(cavern: list[list[str]]) -> int:
    """Scan the cave for air pockets.  Return the number of
    air pockets encountered.

    >>> cavern_1 = cave.read_cave("data/tiny-cave.txt")
    >>> scan_cave(cavern_1)
    1
    >>> cavern_2 = cave.read_cave("data/cave.txt")
    >>> scan_cave(cavern_2)
    3
    """
```

Although you could write the nested `for` loops in the form
`for row in cavern:` and `for col in row:`, we will soon need the 
indexes of the cells for pouring water.  Instead, I suggest you 
write it using indexes, like `for row_i in range(len(cavern)):` and 
`for col_i in range(len(cavern[0])):`.  Then you can test whether 
you have encountered a cell containing air with the condition
`cavern[row_i][col_i] == config.AIR`.  

Note that you must _NOT_ write `if cavern[row_i][col_i] == " ":`, 
even though you can tell that `cave.AIR` is 
a single space, `" "`, and even though it will work 
correctly (at first) if you do.  Even if you did not anticipate a user 
changing 
these choices in the `config.py` file, you should write as if 
they could. 
This is the principle of _information hiding_.  Using the 
value `" "` directly, rather than refering to it 
by the symbolic name `config.AIR`, is called _hard coding_ a
[_magic number_](
https://en.wikipedia.org/wiki/Magic_number_(programming))
(even though it's a string rather than a number).  Magic numbers are 
considered a bad _code smell_.  

When you find a cell containing air, you should place water in that 
cell: 

```python
            cavern[row_i][col_i] = config.WATER
```

You should also update a count of the number of air pockets discovered.
This count is the value that `scan_cave` returns.  
In addition we would like to update the view to show the water.
This will display immediately in the graphical view, and in the textual 
display when we call `cave_view.redisplay(cavern)`.

```python
            cave_view.fill_cell(row_i, col_i)
```

The first test case should succeed, as the air pocket in
`tiny_cave.txt` is just a single cell.  The second test case 
should fail:  Although there are just three large chambers in
`cave.txt`, each of those chambers contains several cells.  If we 
count the number of times we encounter a cell that contains air, we 
will count the number of empty cells rather than the number of 
chambers.  (I got 48, which means my test case expecting three
chambers "failed", but only because I'm not done yet.)

You could test for the "magic number" code smell by changing the value 
of `cave.AIR`.  Changing it to another value like `.` should not 
change the behavior of your program. 

You will call `scan_cave` from your `main` function, which should 
display the cave before scanning and then again after: 

```python
def main():
    doctest.testmod()
    cavern = cave.read_cave(config.CAVE_PATH)
    cave_view.display(cavern,config.WIN_WIDTH, config.WIN_HEIGHT)
    chambers = scan_cave(cavern)
    print(f"Found {chambers} chambers")
    cave_view.redisplay(cavern)
    cave_view.prompt_to_close()
```

After announcing how many chambers we found, we make sure the final 
version of the cave is displayed (this will print the textual
version again) and then wait for the user to admire our beautiful 
graphics before removing the graphical version. 

## Pour it on! 

Now all we need to do is to fill each chamber with water.  When we 
encounter a cell containing air, we'll still count it as a chamber, 
but then we'll flood it so that we don't count any more cells in 
that chamber.   

So far we have filled a single cell with water by assigning
`cave.WATER` to that cell, e.g., `cavern[row_i][col_i] = cave.WATER`.
We displayed it with `cave_view.fill_cell(row_i, col_i)`.
Replace those lines with a call to a new function `pour`.
(Keep the line that increments the number of air chambers 
encountered.)  We will 
write `pour` to not 
only fill in that individual cell, but also spread it through the 
chamber.  
 To help us visualize how the 
chambers are filling, we can change the color of water each time we 
encounter air, like this: 

```python
        pour(cavern, row_i, col_i)
        cave_view.change_water()
```

Our first version of `pour` can simply put water in the one 
discovered cell of air and update the corresponding area on the 
display, like the lines we replaced in `scan_cave`: 

```python
def pour(cavern: list[list[str]], row_i: int, col_i: int):
    """Pour water into cell at row_i, col_i"""
    cavern[row_i][col_i] = config.WATER
    cave_view.fill_cell(row_i, col_i)
```

Because we have not yet made the water spread, we will still get a 
count of air cells rather than chambers, and the visualization will 
show different colors in adjacent cells: 

![Before the water spreads](img/cave-rainbow.png)

## Checkpoint

Now your `flood.py` module contains a `main` function and two other 
functions, `scan_cave` and `pour`.  Only `scan_cave` contains loops.
Your `scan_cave` functions counts the number of times it encounters
`cave.AIR`.  Currently the result should be the number of grid cells
containing `cave.AIR`; we will change that shortly. 

## Let it flow

Now just need a way to let the 
water spread to fill the whole chamber. 

Although real water spreads in all directions, it will be enough for 
our simulated water to spread in four directions: up, down, left, 
and right.  If there is water in row _r_, column _c_, we can easily 
determine the row and column of the adjacent cells in each direction. 

![Up, down, left, right as coordinates](
img/fill-directions.png
)

The cell directly above cell (r, c) is cell (r-1, c).  The cell 
directly below is cell (r+1, c).  The cell to the left is
cell (r, c-1). The cell to the right is cell (r, c+1).  

If any of 
these coordinates are not within bounds (e.g., if r is less than 0), 
that indicates that there is no cell in that direction (e.g., r less 
than 0 indicates a space "above" the grid). 

It is tempting to try to write loops to fill cells in each direction.
If we were spreading water in just one direction, a loop would work 
well.  For spreading in all four directions, recursion is much 
easier.  We'll note this intent in the function header for `pour`:


```python
def pour(cavern: list[list[str]], row_i: int, col_i: int):
    """Fill the whole chamber around cavern[row_i][col_i] with water
    """
```

Recursion can be confusing at first ... there will be _lots_ of 
recursive calls to _pour_, and it can be hard to see how they are 
related.  To make it just a little easier to understand, at least 
for small caves, we'll add some instrumentation to our `pour` 
function.  Add this in the imports section of your source file: 

`from tracer import trace`

This imports a single function, `trace`, from `tracer.py`.  Function 
`trace` is a special kind of function called a _decorator_.  Think 
of it as decorative paper to wrap around a function.  (In fact this 
kind of function is also called a _wrapper_.)  We will wrap it 
around the `pour` function this way: 

```python
@trace()
def pour(cavern: list[list[str]], row_i: int, col_i: int):
    """Fill the whole chamber around cavern[row_i][col_i] with water
    """
```

<aside class="notice">
The `trace()` decorator is only useful for very small caves.  For a 
large cave, it produces too much output.  I suggest using it to 
understand small examples, then commenting it out while working with 
larger caves. 

We will just _use_ the `trace()` decorator for now. You are welcome to 
look through `tracer.py`, but I think you will find it a bit complex.
(A function that returns a function that takes a function and 
returns another function ... phew.)
Learning to _write_ decorators is a good thing to put on your bucket 
list if you continue to work in Python and want to develop more 
advanced professional skills. 
</aside>

### Base and recursive cases 

Recall that when we design a recursive function, we always
distinguish one or more _base_ cases and one or more _recursive_ 
cases.  A _base case_ is a problem that we can solve directly, 
without further recursion.  A _recursive case_ will make calls on 
the same function, but not on the same problem ... it must make the 
problem "smaller" or "simpler" in a way that, if repeated, leads 
inevitably to the base cases.  

What  can we identify as base cases 
and recursive cases for filling a chamber with water?

Sometimes the base case or cases are easy to identify, and provide 
the hints we need to design the recursive cases.  Sometimes it is 
the other way ... the recursive cases may be straightforward, and 
the base case(s) less obvious.  

For flood-fill, the recursive case seems to be the easier starting 
point.  We have already sketched it:  We fill one cell with water, 
and recursively call `pour` with the row and column of four 
neighboring cells.  But the recursive case must make _progress_ in 
the sense of making recursive calls only on "smaller" or "simpler" 
problems.  In what sense is the problem "smaller" or "simpler" when 
we make a recursive call to flood-fill from a neighboring cell?

We might also be worried about all the conditions under which we 
cannot fill a neighboring cell.  We can't pour water where there is 
a stone wall, and we can't pour water outside the cavern, for example 
in a row or column with a negative index. We might be worried about 
how complicated our code will be if we consider all the relevant 
conditions before each of the recursive calls. 

Intuitively, each time we call `pour`, there should be fewer cells 
holding air than there were before.  This is a useful hint about the 
base cases.  We might initially think of checking, before each 
recursive call, that we are spreading into an air pocket.  For 
example, we might imagine that "spread the water upward" would be 
something like: 

```python
    row_up_i = row_i - 1
    if (row_up_i >= 0 and row_up_i < len(cavern)
        and cavern[row_up_i][col_i] == cave.AIR):
        pour(cavern, row_up_i, col_i)
```

We could imagine variations on this complicated check for all four 
directions, so that we only spread water into cells containing air. 
But if the "progress" condition is that we have reduced the number 
of cells containing air, then the guarantee that recursion must 
eventually stop is that we must run out of cells containing air.  
This suggests that the base case could be "this is not a cell 
containing air".  In other words, we don't need to make _four_ tests 
to see whether we can spread up, down, left, and right.  We can make 
just _one_ test at the beginning of function. 

Not this pseudocode: 

```
    fill this cell with water
    if there is an air cell above: 
        recursively call fill on the cell above
    if there is an air cell below: 
        recursively call fill on the cell below
    if there is an air cell to the left: 
        recursively call fill on the cell left
    if there is an air cell to the right: 
        recursively call fill on the cell right
```

but this simpler, shorter pseudocode: 

```
    if this a cell in the grid, and it contains air: 
        fill this cell with water
        recursively call pour on the cell above
        recursively call pour on the cell below
        recursively call pour on the cell left
        recursively call pour on the cell right
    else:
        just return without doing anything
```



Now we just need to write one condition that checks both whether the 
row and column are within the proper range and, if they are, whether 
the current content of the cell at that row and column contain air. 
Opportunities for error are fewer, and if we _do_ make a mistake, it 
will be easier to debug.  The code is simpler to read and understand,
and easier to write.  

Don't forget the "this is a cell on the grid" check, or you might
get this error: 

```text
IndexError: list index out of range
```

I find it simplest to write `if` statements that check for the 
reasons we might _not_ spread water to this cell.  In pseudocode: 

```text
if row is out of range: 
    return
if column is out of range: 
    return
if the cell at (row, col) does not contain AIR: 
    return
# Now I know this is a cell to fill .,.
fill this cell
# ... and water should spread out from here
make recursive calls for up, down, left, right
```

If you can turn that pseudocode into Python, you will have a program 
that properly counts chambers and fills each chamber with a different 
color of water: 

![Final display from `cave.txt`](img/cave-final.png)

Textually we use digits instead of colors: 

```text
# # # # # # # # # #
# 1 1 1 # 1 # 2 2 #
# 1 1 1 # 1 # 2 2 #
# 1 1 1 1 1 # 2 2 #
# 1 1 1 # 1 # 2 2 #
# 1 1 1 # 1 # 2 2 #
# 1 1 1 # # # # # #
# 1 1 1 # 3 3 3 3 #
# 1 1 1 # 3 3 3 3 #
# # # # # # # # # #
```

You can try with some of the other cave specifications in the `data` 
directory, or create some of your own. The twisty cave 
(`data/twisty-cave.txt`) checks that water can spread along more 
complicated routes: 

![The twisty cave](img/twisty-cave.png)

In addition to the expected visualization, the `scan_cave` function 
should now be returning the correct count of cave chambers and 
passing its test cases.  Check that it finds 7 chambers in the 
twisty cave. 

## Checkpoint

Your program now contains the same functions as at the last 
checkpoint, but function `fill` has been changed to recursively 
spread water up, down, left, and right.   Function fill should be 
simple.  Mine is 10 lines, including an `if` condition that
I broke into three lines for readability.  It does _not_ contain any 
`for` or `while` loops, only recursive calls.  

Although we haven't changed `scan_cave` at all, it should now be 
returning the number of air _chambers_ in the cave, rather than the 
number of cave cells containing air. 

If this describes your program, you have completed the assignment 
and can turn in `flood.py`. 

## Challenge yourself 1: Improve the graphical visualization

Your program is already complete. 
Read on if you are interested in using graphics and other user 
interface techniques to make programs more useful and usable. 

There is a `FIXME` comment in `graphics/grid.py`: 

``` 
FIXME: The color wheel should produce colors of contrasting brightness
as well as hue, to maximize distinctness for dichromats (people with 
"color blindness").  Maybe generating a good color wheel can be part 
of a project later in CS 210.   (This is not a required or expected
change for the week 5 project.)
```

The current palette of colors is defined using 
intensity of red, green, and blue channels (the "RGB" color space):

```python
color_wheel = [
    color_rgb(255,0,0), color_rgb(0,255,0), color_rgb(0,0,255),
    color_rgb(255,255,0), color_rgb(255,0,255), color_rgb(0,255,255),
    color_rgb(127,255,0), color_rgb(0,127,255), color_rgb(127,0,255),
    color_rgb(255,127,0), color_rgb(0,255,127), color_rgb(255,0,127),
    color_rgb(127,127,0), color_rgb(127,0,127), color_rgb(0,127,127),
    color_rgb(255,255,127), color_rgb(255,127,255), color_rgb(127,255,255) ]
```

If you are familiar with color spaces, you might consider how to 
design the color wheel in HSB (hue, saturation, and brightness) 
color space to get sufficient contrast in saturation and brightness 
for people who cannot distinguish by hue.  If you are not familiar 
with color spaces, you can think of brightness as the sum of the red,
green, and blue components, and saturation as their difference. 

For a better, more systematic adaptation to common differences in 
visual perception, we need to understand those 
differences. Designing usable interfaces requires understanding the 
ways people use those interfaces, so specialists in usability often 
study psychology as well as computing.  You can find some notes on 
designing for variations in color perception in
[this article by a usability specialist](
https://www.uxmatters.com/mt/archives/2007/02/ensuring-accessibility-for-people-with-color-deficient-vision.php).

[Accessibility standards for the world wide web](
https://www.w3.org/standards/webdesign/accessibility)
are maintained by the W3 Consortium.  They are useful reading also 
for developers of other kinds of application. 

## Challenge yourself 2: Improve the non-visual display

If you want to really challenge yourself in thinking about interface 
design, consider how you would rework the "visualization" to work 
for people with limited vision.  Many people with blindness or 
limited vision use audio interfaces, including screen readers like
[JAWS](https://www.freedomscientific.com/products/software/jaws/)
or
[VoiceOver](https://www.apple.com/voiceover/info/guide/_1121.html).
Can you imagine substituting an audio interface for the 
visualization?  What considerations would go into its design?  How 
would you evaluate it?

We don't yet have the programming techniques for making it easy to 
attach different or varied user interfaces for the same 
functionality.  We will study program structures for more dynamic 
connection of user interface with functionality in the next term.

The simple textual display was added in fall 2023 to work 
with screen readers like JAWS and NVDA.  I'm certain it could be 
improved.  I am not sure yet whether or how an audio interface could 
help.  One lesson I learned is that a visual interface often reduces 
the memory load for sighted users, who can glance at the display 
instead of remembering details.  A non-visual display (including a 
text display accessed through a screen reader) is not very 
"glanceable", so one must be careful to include examples that do not 
put an excessive load on short-term memory. If you have an interest in 
perception or cognitive psychology 
as well as computing, designing effective non-visual interfaces is a 
rich area for further work.  

In addition to being essential for 
users with limited vision, there are many contexts in which 
non-visual interfaces are better even for sighted users.  Consider, 
for example, the control panel of an automobile. Traditional knobs 
on the car radio, and various levers and buttons to control heat, 
temperature, etc, were originally designed to be operable by feel, 
without looking.  Migrating controls to touch panels that 
require 
visual attention is a step backward in automobile safety.  I hope 
some of you will design user interface techniques of the future that 
will both make computing more widely accessible and avoid visual 
distractions. 



