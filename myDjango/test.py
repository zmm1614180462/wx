class A():
    def __init__(self, *args, **kwargs):
        for prop in list(kwargs):
             print(prop)
             print(isinstance(getattr(self.__class__,prop),str))


class b(A):
  name='string'


class Celsius:
    def __init__(self, temperature=0):
        self.temperature = temperature
        print(self.__class__)


    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    def get_temperature(self):
        print("Getting value")
        return self._temperature

    def set_temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        print("Setting value")
        self._temperature = value

    temperature = property(get_temperature, set_temperature)
    print(isinstance(temperature, property))


z = Celsius()
z.temperature = 100
print(z.temperature)