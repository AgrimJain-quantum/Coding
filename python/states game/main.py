import turtle

# Set up the screen
screen = turtle.Screen()
screen.title("States Game")

# Provide the image path directly
image_path = r"C:\Users\Agrim Jain\Desktop\Coding\python\states game\blank_states_img.gif"

# Register the image as a turtle shape
screen.addshape(image_path)

# Create a turtle and set its shape
turtle.shape(image_path)

# Wait for user to click to close the window
screen.exitonclick()
