from gpiozero import CPUTemperature

temp = CPUTemperature()
cpu_temp = round(temp.temperature,1)

print("CPU temperature is " + str(cpu_temp) + " degrees C")

