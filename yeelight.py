class Bulb:

    def __init__(self, ip):
        self.ip = ip

    def turn_on(self):
        print("Turning on light\n")

    def turn_off(self):
        print("Turning off light\n")

    def set_brightness(self, val):
        print(f'Setting light to {val} \n')

    