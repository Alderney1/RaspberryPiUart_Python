#--------------------------------------------------------------------
#Administration Details
#--------------------------------------------------------------------
__author__ = "Mats Larsen"
__copyright__ = "Mats Larsen 2014"
__credits__ = ["Mats Larsen"]
__license__ = "GPLv3"
__maintainer__ = "Mats Larsen"
__email__ = "larsen.mats.87@gmail.com"
__status__ = "Development"
__description__ = "Module for generic class to handle uart of a given intance. It makes a conenction to transmit data and recieve data. The setup of the uart are baudrate, start bits/no start bits, length of data bits and stop bits/no stop bits."
__file__ = "uart.py"
__class__ ="Uart"
__dependencies__ = ["DisplayMsg"]
#--------------------------------------------------------------------
#Version
#--------------------------------------------------------------------
__version_stage__ = "Pre_alpha"
__version_number__ = "0.1"
__version_date__ = "20140917"
__version_risk__ = "This current version is in Pre-alpha version, which meaning that the program can crash or perform other unrespected behavoiurs."
__version_modification__ = "The development project has just been created."
__version_next_update__ = "Implementation of connection."
#--------------------------------------------------------------------
#Hardware
#--------------------------------------------------------------------
"""
The hardware for this uart project for a raspberry pi is that the GPIOs
for uart is located at GPIO14 and GPIO15 respective for the TXS(transmitter)
and RXD(reciver).
"""
#Import
#--------------------------------------------------------------------
#from msg import DisplayMsg as DM # Import library for standard display messages.
import traceback
import serial # import the serial uart module
import sys
import glob
import threading # import threading
#--------------------------------------------------------------------
#CONSTANTS
#--------------------------------------------------------------------
LOG_LEVEL = 2 # Information level
LOG_ALWAYS = 3 # Always log data
#--------------------------------------------------------------------
#METHODS
#--------------------------------------------------------------------
def log(msg, log_level=LOG_LEVEL):
    """
    Print a message, and track, where the log is invoked
    Input:
    -msg: message to be printed, ''
    -log_level: informationlevel, i
    """
    global LOG_LEVEL
    if log_level <= LOG_LEVEL:
        print(str(log_level) + ' : ' + __file__ + '.py::' + traceback.extract_stack()[-2][2] + ' : ' + msg)
        
class Uart(object):
    """
    This class for handling uart conenction.
    """
    class Receiver(threading.Thread):
        """
        Class to receive data over a existing uart connection.
        """
        def __init__(self,name=None):
            self._name = name
            #Threading
            threading.Thread.__init__(self) # initialize the thread
            self.daemon = True
            
            self.start() # start main loop

        def run(self):
            """
            Is the main loop for the thread, to listen/observer over the uart connection.
            """
            while(1):
                data = ser.read()
                print(data)
            
    class Transmitter(object):
        """
        Class to transmit data over a existing uart connection.
        """
        def __init__(self,name=None):
            """
            Initilize the transmitter instance.
            """
            self._name = name # name of the intance
            # Inter assighnment
            self._number_data = 0 # Indicate the number of sended data 

        def send_data(self,data):
            """
            Send the data that has to be transmitted.
            Inputs->
            Data : : Data is the transitted data.
            """
            bytes_written = ser.write(bytes(data,'UTF-8'))
            self._number_data += 1
            return bytes_written

        def get_numberdata(self):
            """
            Return the number of transmitted data packets.
            """
            return self._number_data
        
        def get_name(self):
            """
            Return the name of the instance.
            """
            return self._name

        def set_name(self,name):
            """
            Set the new name of the name.
            """
            self._name = name

    def __init__(self,**kwargs):
        
        r = self.serial_ports()
        print(r)
        print('rrrrr')
        self._name = kwargs.get('name','Uart') # name of this device for the connection
        self._name_rec = kwargs.get('name_rec','UNVALID') # name of the reciver for the connection

         
        self._port = kwargs.get('port','/dev/ttyAMA0') # Device name or port number number or None of the connection.
        self._baudrate = kwargs.get('baudrate',9600) # Baud rate such as 9600 or 115200 etc.
        self._bytesize = kwargs.get('bytesize',serial.EIGHTBITS) # Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS.
        self._parity = kwargs.get('parity',serial.PARITY_NONE) # Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
        self._stopbit = kwargs.get('stopbit',serial.STOPBITS_ONE) # stopbits – Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO.
        self._timeout = kwargs.get('timeout',5) # Set a read timeout value.
        self._xonxoff = kwargs.get('xonxoff',serial.XOFF) # Enable software flow control.
        self._rtscts = kwargs.get('rtscts',serial.XON) #  Enable hardware (RTS/CTS) flow control.
        self._dsrdtr = kwargs.get('dsrdtr',serial.XOFF) # Enable hardware (DSR/DTR) flow control.
        self._writetimeout = kwargs.get('writeTimeout',5) # Set a write timeout value.
        self._interchartimeout = kwargs.get('interCharTimeout',5) # Inter-character timeout, None to disable (default).
        
        global ser
        ser = serial.Serial(port=self._port,baudrate=self._baudrate,bytesize=self._bytesize,parity=self._parity,stopbits=self._stopbit,timeout=self._timeout,xonxoff=self._xonxoff,rtscts=self._rtscts,dsrdtr=self._dsrdtr, writeTimeout=self._writetimeout,interCharTimeout=self._interchartimeout)
        ser.open()
        #ser.write("aaaaaaa".encode('utf-8'))
        #a = ser.read()
        #print(a)
        self._trans = self.Transmitter(name=self._name + 'Transmitter')
        self._rev = self.Receiver(name=self._name + 'Reciver')
    def send_data(self, data):
        """
        Send Data
        """
        self._trans.send_data(data)
        
    def close_uart(self):
        """
        Close the uart connnection.
        """
        serial.close()

    
    def serial_ports(self):
        """Lists serial ports, that are in the operative system
        Raises EnvironmentError->
        :On unsupported or unknown platforms
        Returns->
        A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
