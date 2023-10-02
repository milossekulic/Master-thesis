import serial
import time
import subprocess
from camera_capture import main

arduino = serial.Serial(port="/dev/ttyACM0", baudrate=38400, timeout=0.1)


try:
    while True:
        # Read data from the serial port
        data = arduino.readline()
        # Print the received data (decode it assuming it's ASCII)
        # print(data.decode("utf-8"), end="")
        # Change the encoding if needed
        is_true = data.decode("utf-8")
        if is_true:
            # Specify the command to run the script
            # command = ["python", "camera_capture.py"]

            # try:
            #     # Run the script
            #     subprocess.run(command, check=True)
            #     print("Script executed successfully.")
            # except subprocess.CalledProcessError as e:
            #     print(f"Error: {e}")
            # except Exception as e:
            #     print(f"An error occurred: {e}")
            start_the_flow = main()
            if start_the_flow:
                arduino.write(b"1")
            else:
                arduino.write(b"0")
except KeyboardInterrupt:
    print("Serial reading stopped by user.")
    arduino.write(b"0")
finally:
    # Close the serial port when done
    arduino.write(b"0")
    arduino.close()
