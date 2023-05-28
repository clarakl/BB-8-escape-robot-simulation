from controller import Robot

robot = Robot()

timestep = int(robot.getBasicTimeStep())

# Max possible speed for the motors of the robot.
maxSpeed = 8.72

# Configuration of the main motor of the robot.
pitchMotor = robot.getDevice("body pitch motor")
pitchMotor.setPosition(float('inf'))
pitchMotor.setVelocity(0.0)

# Enable the accelerometer sensor for the body.
bodyAccel = robot.getDevice("body accelerometer")
bodyAccel.enable(timestep)

# Variables to store the previous values of the sensors for comparison.
prevBodyAccel = [0, 0, 0]

# Acceleration threshold to consider as no significant vertical acceleration.
accelThreshold = 0

# At first, we go forward.
pitchMotor.setVelocity(maxSpeed)
forward = True

while robot.step(timestep) != -1:
    # Get the current value of the accelerometer sensor.
    bodyAccelValues = bodyAccel.getValues()

    # Calculate the change in acceleration
    deltaBodyAccel = [bodyAccelValues[i] - prevBodyAccel[i] for i in range(3)]

    # Check if there is no significant vertical acceleration (Z-axis).
    if abs(deltaBodyAccel[2]) < accelThreshold:
        # If true, switch the robot to go at max speed in the opposite direction.
        forward = not forward
        if forward:
            pitchMotor.setVelocity(maxSpeed)
        else:
            pitchMotor.setVelocity(-maxSpeed)

    # Update the previous sensor values.
    prevBodyAccel = bodyAccelValues[:]
