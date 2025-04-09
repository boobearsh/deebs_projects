# # Please note, this program was created in reference to Codedex's tutorial.

# The line shown is a terminal command to install the imageio package, not Python code. To use imageio in your program,
# follow these steps:

# 1. Open your terminal and run:
# bash
# pip3 install imageio

# 2. In your Python script(gif_maker_main.py), import imageio:
# python
# Your code that uses imageio follows...
# This ensures that imageio is installed on your system and available to your program when you run it.

# ============= Creating the program =============

import imageio.v3 as iio  # Gives the library a shorter name for convenience
import os

# Ensure that the images being used are within the same folder as this program
print("Current working directory:", os.getcwd())
# Line 21: This will help confirm where the program is looking for the files
# Debugging Tip: Add a print statement to check the current working directory of the program.


# Create a list that contains the locations of the image files.
# Create an empty list that will be used to store the actual image data from these files.
filenames = [
    'team-pic1.png',
    'team-pic2.png']
images = []

# Next, let's use a for loop to go through the file paths
# This will read the images using the imageio library's .imread() method
for filename in filenames:
    images.append(iio.imread(filename))

# .imread() method: loads an image based on the file path.

# So now, our images variable (the empty list) has all the images stored
# Let's use the .imwrite() method
# This method will turn the images into a GIF
iio.imwrite('team.gif', images, duration=500, loop=0)

# Line 33: This line of code takes four arguments:
# 'team.gif': This is the name you want to give to your new GIF file.
# images: The (empty and initialized variable) list containing the image data
# duration: 500 "How long each picture should show in the GIF, in milli-seconds"
# loop = 0: "How many times the GIF should repeat (0 means it keeps looping forever)"

# ============= Running the program =============

# In the terminal, navigate to the folder with the Python file, using cd "Change Directory"
# If your file is located in your desktop.
# Ex: ----->  cd Desktop
# Run python3 and the file name: python3 gif_maker_main.py

# If you are using VSCode, simply run the program by clicking the play button.
# Or, if you are using another IDE or Interpreter, simply run the program
# After running the program, a new file.
# For example: team.gif ------> should appear within the same folder

# ============= End =============
