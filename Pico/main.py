from machine import Pin, PWM
import utime
import sys
import select

# Define the servos
servo_pins = [0, 1, 2, 3, 4, 5, 6, 7]
servos = [PWM(Pin(pin)) for pin in servo_pins]

# Set frequency to 50Hz for all servos
for servo in servos:
    servo.freq(50)

def degrees_to_duty(degrees):
    """Convert degrees to PWM duty cycle for a 50Hz signal."""
    min_pulse_width = 500  # Minimum pulse width in microseconds
    max_pulse_width = 2400  # Maximum pulse width in microseconds
    pulse_width = min_pulse_width + (degrees / 180.0) * (max_pulse_width - min_pulse_width)
    return int((pulse_width / 20000.0) * 65535)

def set_servo_angles(angles):
    """Set the angles for all servos based on a list of angles."""
    for i in range(len(servos)):
        if i < len(angles):
            angle = int(angles[i])
            servos[i].duty_u16(degrees_to_duty(angle))
            print(f"Servo {i} set to {angle} degrees")
    
def read_command():
    """Read a command from the serial input."""
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.readline().strip()
    return None

def parse_command(command):
    """Parse and apply a command string received over serial."""
    angles = command.split(',')
    set_servo_angles(angles)

while True:
    command = read_command()
    if command:
        parse_command(command)
    utime.sleep(0.1)
