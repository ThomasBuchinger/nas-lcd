class FakeLcd():
  def display_string(self, string, line):
    print("{}: {}".format(line, string))

  def clear(self):
    print("Clear!")

  def backlight_off(self):
    print("Backlight OFF")

  def display_off(self):
    print("Display OFF")

  def display_on(self):
    print("Display ON")