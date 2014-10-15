from uart import Uart
import time

uart = Uart()
uart2 = Uart()
uart.send_data("PIcalling")

time.sleep(3)
