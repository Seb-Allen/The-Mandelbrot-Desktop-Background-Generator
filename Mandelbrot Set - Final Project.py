from PIL import Image
import os
import json

SCREEN_RESOLUTIONS = {
    "HD": [1280, 720],
    "FHD": [1920, 1080],
    "QHD": [2560, 1440],
    "4K": [3840, 2160],
    "8K": [7680, 4320],
    "custom": []    
}

with open("PARAMETERS.json") as f:
    PARAMETERS = json.load(f)

def main():
    # Step 1: Ask the user for the desired image resolution/size
    size = resolution()
    
    # Step 2: Generate a blank image based on the user's selection (Generate the Complex Plane)
    width, height, image = make_plane(size)

    # Step 3: choose a location and level of zoom within the Mandelbrot Set (set the x coordinate and multiply to get correct ratio size for aspect ratio)
    para_set = mandelbrot_location()

    # Step 4: Draw Mandelbrot: 
        # 1) Populate the 
        # 2) Generate C
        # 3) Iterate C
        # 4) Mark on the Complex Plane whether C belongs to the Mandelbrot Set
    draw_mandelbrot(para_set, width, height, image)

    # Step 5: Display the image
    image.show()

    # Step 6: Do you want to save the image?
    save_background(image, para_set, size)

    # Step 7: If you created a custom parameter set, do you want to save it?
    save_custom_parameter(para_set)

def resolution():
    # Select between HD, FHD, QHD, 4k, 8k, or custom
    print("Select the resolution of your monitor (or the size of the image you would like to generate)...")
    size = input("Choose between HD, FHD, QHD, 4K, 8K, or custom: ")
    
    # Ensure we enter a valid screen size
    while size not in SCREEN_RESOLUTIONS:
        size = input("Choose between HD, FHD, QHD, 4K, 8K, or custom: ")

    # Updating the screen resolutions dictionary to accept custom inputs
    if size == "custom":
        custom_resolution()

    return size

def custom_resolution():
    # Error checking the custom resolution format
    while True:
        try:
            # Ask the user to enter a resolution
            custom = input("Enter the resolution you would like, for example, 640x480: ")
            # Remove 'x' from the string and create a list
            custom = custom.split("x")
            # Convert the list of strings into integers
            custom = list(map(int, custom))
            break
        # If a ValueError occurs, prompt user to check format
        except ValueError:
            print("\nPlease match this format when entering the resolution: 640x480. ")
    
    # add the custom resolution to the dictionary
    SCREEN_RESOLUTIONS["custom"] = custom

def make_plane(size):
    # Look up the resolution from the dictionary and extract the width and height to create a blank image
    width = SCREEN_RESOLUTIONS[size][0]
    height = SCREEN_RESOLUTIONS[size][1]
    
    # Generate a blank image with the correct width and heigh
    image = Image.new("RGB", (width, height))

    return width, height, image

def mandelbrot_location():
    # Ask user if they want to generate a preset location, or enter their own custom parameters
    print("\nWould you like to generate a preconfigured area of the Mandelbrot, or create your own location and zoom parameters?")
    print("Below is a list of all the available preconfigured parameters:\n")

    # Print all the available preconfigured parameters to choose from
    for key in PARAMETERS:
        print(str(key))

    # Get answer from user
    para_set = input("\nEnter a preconfigured parameter or type 'custom': ")

    # Error checking
    while para_set not in PARAMETERS:
        para_set = input("Enter a preconfigured parameter or type 'custom': ")

    # Go to the custom parameter function if custom is selected
    if para_set == "custom":
        custom_para_set()

    return para_set

def custom_para_set():
    while True:
        # Error checking
        try:
            # Request Real axis start position
            r_s = float(input("Enter a start position for the Real axis (Mandelbrot Set lies within absolute 2): "))

            # Set the max value to absolute 5, to give the user some freedom to zoom out if desired
            while abs(r_s) > 5:
                r_s = float(input("The Real axis start position must be within absolute 5 (Mandelbrot Set lies within absolute 2): "))
            break

        except ValueError:
            print("\nTake care to enter a valid start position for the Real axis...")

    while True:
        try:
            # Request the total distance for the Real axis, representing the level of zoom
            r_d = float(input("Enter a distance for the Real axis (this represents zoom level): "))
            break

        except ValueError:
            print("\nTake care to enter a valid distance for the Real axis...")

    while True:  
        try:
            # Enter a start position for the Imaginary axis
            i_s = float(input("Enter a start position for the Imaginary axis (Mandelbrot Set lies within absolute 2): "))

            # Set the max value to absolute 5, to give the user some freedom to zoom out if desired
            while abs(i_s) > 5:
                r_s = float(input("Enter a start position for the Imaginary axis (Mandelbrot Set lies within absolute 2): "))
            break

        except ValueError:
            print("\nTake care to enter a valid position for the Imaginary axis...")

    while True:
        try:
            # Enter a value for the number of times to iterate the Mandelbrot function
            itn = int(input("Enter the number iterations for z in the Mandelbrot function: "))

            # The number of interations must be atleast 2 for the function to work
            while itn <= 2:
                itn = int(input("The number of interations must be greater than 2: "))
            break

        except ValueError:
            print("\nTake care to enter a valid integer for the number of iterations...")

    # Populate the custom parameter in PARAMETERS
    PARAMETERS["custom"]["real start"] = r_s
    PARAMETERS["custom"]["real distance"] = r_d
    PARAMETERS["custom"]["imaginary start"] = i_s
    PARAMETERS["custom"]["iterations"] = itn

def draw_mandelbrot(para_set, width, height, image):
    # 1) Extract the desired parameter set from the dictionary, and populate the equation to generate the complex number C
    r_s = PARAMETERS[para_set]["real start"]
    r_d = PARAMETERS[para_set]["real distance"]
    i_d = PARAMETERS[para_set]["real distance"] * height / width
    itn = PARAMETERS[para_set]["iterations"] 

    # If para_set is 'full set', the Real axis will always be centred vertically
    if para_set == "full set":
        i_s = PARAMETERS[para_set]["imaginary distance"] / 2
    else:
        i_s = PARAMETERS[para_set]["imaginary start"]

    # Open the blank image (our Complex Plane)
    image = image.load()

    # Nested for loop to iterate over each pixel and check whether it belongs in the Mandelbrot Set
    for x in range(width):
        for y in range(height):

            # 2) Generate the complex number C, which represents a point on the Complex Plane
            c = complex(r_s + r_d * (x/width), i_s - i_d * (y/height)) #good @150 V.GOOD

            # 3) Iterate C in the Mandelbrot Function
            n = mandelbrot(c, itn)

            # 4) Mark on the Complex Plane whether C belongs to the Mandelbrot set
            if n < itn:
                red = int(255 / itn * n)
                green = int(255 / itn * n)
                blue =  int(255 / itn * n)
            else:
                red = 0
                green = 0
                blue = 0

            pixel = (red, green, blue)
            image[x, y] = pixel

    # Images are mutable, so we don't have to return it. Changes made in this function will persist.

def mandelbrot(c, itn):
    # Where the magic happens... C is iterated in the Mandelbrot function here
    # z and n are set to 0
    z = 0
    n = 0

    # We set the limits of the function: 
    # If when we iterate, the absolute value of z is greater than 2, we presume that it will tend towards infinity
    # And we set a limit on the number of iterations, otherwise we could potentially create an infinite loop
    while abs(z) <= 2 and n < itn:
        z = z ** 2 + c
        n += 1
    return n

def save_background(image, para_set, size):
    # Ask user if they want to save the image
    save = input("Did you like this background? Enter 'y' or 'n' to save the image: ")

    # Error checking
    while save != "y" and save != "n":
        save = input("Please type 'y' or 'n': ")

    # If the user selects y, the image will be saved
    if save == "y":
        i = 1

        # Ensure that previous saves are not overwritten
        if os.path.exists(f"Mandelbrot {para_set} {size}.png"):
            while os.path.exists(f"Mandelbrot {para_set} {size}({i}).png"):
                i += 1
            else:
                image.save(f"Mandelbrot {para_set} {size}({i}).png")
        else:
            image.save(f"Mandelbrot {para_set} {size}.png")

def save_custom_parameter(para_set):
    # If a custom parameter set was created, ask the user whether they want to save it
    if para_set == "custom":
        save = input("Do you want to save your custom parameters? Type 'y' or 'n': ")

        # Error checking, only y or n can be entered
        while save != "y" and save != "n":
            save = input("Please type 'y' or 'n': ")

        # If the user selects save, prompt user for a Key to which the parameter set will be associated in the PARAMETERS dictionary
        if save == "y":
            key = input("Enter a reference key to save the parameter set as: ")

            # Ensure key is unique, and contains something
            while key in PARAMETERS or key == "":
                key = input("Please enter a key that doesn't already exist: ")

            # Pop the values of the custom parameter, and return them to user's Key
            PARAMETERS[key] = PARAMETERS.pop(para_set)

            # Open the json dictionary and enable the program to write to it
            with open("PARAMETERS.json", "r+") as f:
                new_parameter = json.load(f)
                new_parameter.update(PARAMETERS)
                f.seek(0)
                json.dump(new_parameter, f, indent=4)
                

if __name__ == '__main__':
    main()