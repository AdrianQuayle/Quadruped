import tkinter as tk
from tkinter import simpledialog
import json
import serial

class Servo:
    """Represents a servo motor in the GUI."""

    def __init__(self, parent, name, x, y, min_val=0, max_val=180, orient='horizontal'):
        """Initialize a servo control in the GUI at specific pixel coordinates."""
        self.name = name
        self.slider = tk.Scale(parent, from_=min_val, to=max_val, orient=orient)
        self.slider.set(90)  # Default position
        self.slider.place(x=x, y=y)
        self.label = tk.Label(parent, text=name)
        self.label.place(x=x, y=y - 20)

    def get_value(self):
        """Get the current value of the servo."""
        return self.slider.get()

    def set_value(self, value):
        """Set the value of the servo."""
        self.slider.set(value)


class Leg:
    """Represents a leg of the quadruped, composed of a hip and a knee servo."""

    def __init__(self, parent, leg_id, x, y):
        """Initialize a leg with hip and knee servos at specific positions."""
        self.hip = Servo(parent, f'Leg {leg_id + 1} Hip', x, y)
        self.knee = Servo(parent, f'Leg {leg_id + 1} Knee', x + 20, y + 100, orient='vertical')


class Quadruped:
    """Represents the entire quadruped robot."""

    def __init__(self, parent):
        """Initialize the quadruped with four legs."""
        self.legs = []
        for i in range(4):
            leg = Leg(parent, i, 50 + i * 200, 50)
            self.legs.append(leg)

    def get_all_positions(self):
        """Get positions of all servos in the quadruped."""
        positions = []
        for leg in self.legs:
            positions.append(leg.knee.get_value())
            positions.append(leg.hip.get_value())
        return positions

    def set_all_positions(self, positions):
        """Set positions of all servos in the quadruped."""
        for i in range(len(self.legs)):
            self.legs[i].knee.set_value(positions[i])
            self.legs[i].hip.set_value(positions[i])


class StateManager:
    """Manages saving and loading of robot states."""

    def __init__(self):
        """Initialize the state manager."""
        self.states = {}

    def load_states(self, filename):
        """Load states from a file."""
        try:
            with open(filename, 'r') as file:
                self.states = json.load(file)
        except FileNotFoundError:
            self.states = {}

    def save_states(self, filename):
        """Save states to a file."""
        with open(filename, 'w') as file:
            json.dump(self.states, file)

    def get_state(self, name):
        """Get a specific state by name."""
        return self.states.get(name)

    def set_state(self, name, state):
        """Set a specific state by name."""
        self.states[name] = state

    def delete_state(self, name):
        """Delete a specific state by name."""
        if name in self.states:
            del self.states[name]


class SerialCommunicator:
    """Handles serial communication with the Pico."""

    def __init__(self, port='COM7', baud_rate=115200):
        """Initialize the serial connection."""
        self.ser = serial.Serial(port, baud_rate)

    def send_command(self, command):
        """Send a command to the Pico."""
        self.ser.write(f'{command}\n'.encode('utf-8'))

    def receive_data(self):
        """Receive data from the Pico."""
        return self.ser.readline().decode('utf-8')


class QuadrupedGUI:
    """Main GUI class for controlling the quadruped robot."""

    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Quadruped Servo Control")
        self.quadruped = Quadruped(root)
        self.state_manager = StateManager()
        self.serial_comm = SerialCommunicator()
        self.state_manager.load_states("states.json")
        self.create_gui()

    def create_gui(self):
        """Create the GUI elements."""
        save_button = tk.Button(self.root, text="Save State", command=self.save_state)
        save_button.place(x=50, y=300)
        load_button = tk.Button(self.root, text="Load State", command=self.load_state)
        load_button.place(x=150, y=300)
        update_button = tk.Button(self.root, text="Update Pico", command=self.update_pico)
        update_button.place(x=250, y=300)
        self.update_label = tk.Label(self.root, text="", fg="blue")
        self.update_label.place(x=350, y=300)

    def update_pico(self):
        """Send updated positions to the Pico."""
        positions = self.quadruped.get_all_positions()
        command = ""
        for position in positions:
            command += str(position) + ","
        command = command.rstrip(",")
        self.serial_comm.send_command(command)
        print(command)

    def save_state(self):
        """Save the current state of the robot with a given name."""
        name = tk.simpledialog.askstring("Save State", "Enter the state name:")
        if name:
            self.state_manager.set_state(name, self.quadruped.get_all_positions())
            self.state_manager.save_states("states.json")
            self.update_label.config(text=f"'{name}' saved.")

    def load_state(self):
        """Load a state of the robot by name."""
        name = tk.simpledialog.askstring("Load State", "Enter the state name:")
        if name:
            state = self.state_manager.get_state(name)
            if state:
                self.quadruped.set_all_positions(state)
                self.update_label.config(text=f"'{name}' loaded.")
            else:
                self.update_label.config(text=f"'{name}' not found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuadrupedGUI(root)
    root.geometry("900x400")
    root.mainloop()
