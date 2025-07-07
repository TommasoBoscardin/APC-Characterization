import serial
import serial.tools.list_ports


class OZOpticsEPC400:
    """
    A class to interface with the OZ Optics EPC-400-OEM device via USB.
    """

    def __init__(self, port=None, baudrate=9600):
        """
        Initializes the connection to the EPC-400-OEM.

        Args:
            port (str): The COM port to which the device is connected (e.g., 'COM3').
            baudrate (int): The baud rate for serial communication (default: 9600).
        """
        self.baudrate = baudrate
        self.ser = None
        
        if port:
            self.port = port
            self.ser = serial.Serial(port, baudrate, timeout=0.01)
        else:
            self.autoconnect()  # Try to auto-connect if no port is specified

    def autoconnect(self):
        """
        Automatically detects and connects to the EPC-400-OEM device.
        Searches for serial devices matching "CP210" (common for OZ Optics devices).
        """
        devices = serial.tools.list_ports.comports()  # Get available serial ports
        for d in devices:
            if "CP210" in d.description:  # Match by device description (e.g., CP210 USB)
                try:
                    self.ser = serial.Serial(d.device, self.baudrate, timeout=0.03)
                    # Try sending a test command to confirm the device is responding
                    if self.send_command('SN?'):  # Sending a serial number request
                        self.port = d.device
                        return True
                    else:
                        self.ser.close()
                except (serial.SerialException, UnicodeDecodeError):
                    continue
        return False  # No suitable device found

    def send_command(self, command):
        """
        Sends a command to the EPC-400-OEM and reads the full multiline response.

        Args:
            command (str): The command string to send.

        Returns:
            str: The full response from the device.
        """
        if not self.ser:
            return "Not connected."

        full_command = f"{command}\r\n"  # Append CR and LF
        self.ser.write(full_command.encode())  # Send the command

        # Read the response in a loop
        response = ""
        while True:
            chunk = self.ser.read(self.ser.in_waiting or 1).decode()
            response += chunk
            if not chunk:  # Exit loop if no more data is coming
                break

        return response.strip()  # Return the complete response

    def list_commands(self):
        """
        Fetches and returns the list of available commands from the device.

        Returns:
            str: The list of available commands.
        """
        return self.send_command("?")

    def get_baud_rate(self):
        """
        Reads the current baud rate of the device.

        Returns:
            str: The current baud rate setting.
        """
        return self.send_command("BR?")

    def set_baud_rate(self, b):
        """
        Sets the baud rate of the device.

        Args:
            b (int): The baud rate index (0~3).

        Returns:
            str: The device response.
        """
        return self.send_command(f"BR{b}")

    def get_frequencies(self):
        """
        Reads the current scrambling frequencies of the device.

        Returns:
            str: The current frequencies for all channels.
        """
        return self.send_command("F?")

    def set_frequency(self, n, f):
        """
        Sets the frequency for a specific channel.

        Args:
            n (int): The channel number (1~4).
            f (int): The frequency in Hz (0~100).

        Returns:
            str: The device response.
        """
        return self.send_command(f"F{n},{f}")

    def get_mode(self):
        """
        Reads the current operating mode (AC/DC) of the device.

        Returns:
            str: The current operating mode.
        """
        return self.send_command("M?")

    def set_mode_ac(self):
        """
        Sets the operating mode to AC.

        Returns:
            str: The device response.
        """
        return self.send_command("MAC")

    def set_mode_dc(self):
        """
        Sets the operating mode to DC.

        Returns:
            str: The device response.
        """
        return self.send_command("MDC")

    def get_voltages(self):
        """
        Reads the current voltages for all channels.

        Returns:
            str: The current voltages.
        """
        return self.send_command("V?")

    def set_voltage(self, n, v):
        """
        Sets the voltage for a specific channel.

        Args:
            n (int): The channel number (1~4).
            v (int): The voltage in mV (-5000~+5000).

        Returns:
            str: The device response.
        """
        return self.send_command(f"V{n},{v}")

    def set_voltage_max(self, n):
        """
        Sets the voltage for a specific channel to the maximum.

        Args:
            n (int): The channel number (1~4).

        Returns:
            str: The device response.
        """
        return self.send_command(f"VH{n}")

    def set_voltage_min(self, n):
        """
        Sets the voltage for a specific channel to the minimum.

        Args:
            n (int): The channel number (1~4).

        Returns:
            str: The device response.
        """
        return self.send_command(f"VL{n}")

    def set_voltage_zero(self, n):
        """
        Sets the voltage for a specific channel to 0 mV.

        Args:
            n (int): The channel number (1~4).

        Returns:
            str: The device response.
        """
        return self.send_command(f"VZ{n}")

    def enable_output(self, i):
        """
        Enables or disables the output of the driver.

        Args:
            i (int): 1 to enable, 0 to disable.

        Returns:
            str: The device response.
        """
        return self.send_command(f"ENABLE{i}")

    def enable_mode_switching(self, i):
        """
        Enables or disables frequency-to-voltage switching.

        Args:
            i (int): 1 to enable, 0 to disable.

        Returns:
            str: The device response.
        """
        return self.send_command(f"ENVF{i}")

    def toggle_output_mode(self, n):
        """
        Toggles the output mode of a specific channel between AC and DC.

        Args:
            n (int): The channel number (1~4).

        Returns:
            str: The device response.
        """
        return self.send_command(f"VF{n}")

    def get_ac_dc_status(self):
        """
        Reads the AC/DC status of the device.

        Returns:
            str: The AC/DC status.
        """
        return self.send_command("VF?")

    def reset_device(self):
        """
        Performs a soft reset of the device.

        Returns:
            str: The device response.
        """
        return self.send_command("RESET")

    def save_settings(self):
        """
        Saves the current settings to flash memory.

        Returns:
            str: The device response.
        """
        return self.send_command("SAVE")

    def get_serial_number(self):
        """
        Reads the serial number of the device.

        Returns:
            str: The serial number.
        """
        return self.send_command("SN?")

    def get_version(self):
        """
        Reads the hardware and software version of the device.

        Returns:
            str: The hardware and software version.
        """
        return self.send_command("VER?")

    def get_waveform_type(self):
        """
        Reads the current waveform type (Sine or Triangle).

        Returns:
            str: The waveform type.
        """
        return self.send_command("WF?")

    def set_waveform_sine(self):
        """
        Sets the waveform type to Sine.

        Returns:
            str: The device response.
        """
        return self.send_command("WF1")

    def set_waveform_triangle(self):
        """
        Sets the waveform type to Triangle.

        Returns:
            str: The device response.
        """
        return self.send_command("WF2")

    def close(self):
        """
        Closes the serial connection.
        """
        self.ser.close()

