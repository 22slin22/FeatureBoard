# FeatureBoard

This is a project by multiple students at the Gymnasium Gröbenzell. The project was to build a LED-Matrix (24 x 16).
This is the software for controlling the matrix run on a Raspberry Pi. It was created by Nils Cremer.

## Installation

Clone this repository to a Raspberry Pi with

```bash
git clone https://github.com/22slin22/FeatureBoard.git
```

in the folder of your choise.

You also need the numpy library. Use
```bash
pip3 install numpy
```
If you want to run the snake game you also need the pygame library.
```bash
pip3 install pygame
```

If you want to test the software navigate to the FeatureBoard folder and use

```bash
python3 -m scripts.test
```

If you want to create your own scripts either place them into the scripts folder or 
if you wish to work in a seperate folder clone the featureboard folder into your own folder.


## Usage

Import the Board class and create a object of this type. Replace NUM_PANELS with the number of panels you connected (either 3 or 6)

```python
from featureboard.board import Board

board = Board(NUM_PANELS)
```

To start displaying use

```python
board.start_displaying()
```

You can now change what is being shown by the board.
Use the methods available in board.matrix like

```python
board.matrix.clear()
board.matrix.set_led(row, column, color)
board.matrix.set_row(row, color)
board.matrix.set_column(column, color)

# example
board.set_led(2, 5, "red")
```

The available colors are red, blue, green, cyan, magenta, yellow, white and off.
You can also only use the first letter of the color for example "y" for yellow.

If the your program exits the transmission of data to the board will stop and thus the last data sent will be shown permanently.
To prevent this clear the matrix before your program ends.

## Executing your program

If you placed your scipt into the srcips folder use
```bash
python3 -m scripts.name_of_your_script
```
in the FeatureBoard folder.

If the folder where your script is contains the featureboard folder you can also use

```bash
python3 name_of_your_script.py
```




