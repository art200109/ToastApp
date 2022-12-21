import requests
import psutil
import configparser
import threading
import os
import socket

def format_template(template_str, value):
    template_str = template_str.replace("<HOST>",socket.gethostname())
    template_str = template_str.replace("<VALUE>", str(value))
    return template_str

def time_loop(function,template,interval):
    threading.Timer(interval, lambda: time_loop(function, template, interval)).start()
    function(template)
    
def cpu(template):
    formated_template = format_template(template,psutil.cpu_percent(4))
    print(formated_template)
    with open("C:\\temp\\ToastApp\\test","a+") as file:
        file.write(formated_template+"\n")

def memory(template):
    formated_template = format_template(template,psutil.virtual_memory()[2])
    print(formated_template)

def disk(template):
    disks = psutil.disk_partitions()
    for disk in disks:
        formated_template = format_template(template,psutil.disk_usage(disk.device).percent).replace("<DISK>",disk.device)
        print(formated_template)

path_current_directory = os.path.dirname(__file__)
path_config_file = os.path.join(path_current_directory, "agent.conf")

config = configparser.ConfigParser()
config.read(path_config_file)

threading.Thread(target=time_loop(cpu,config["cpu"]["format"],int(config["cpu"]["interval"]))).start()
threading.Thread(target=time_loop(memory,config["memory"]["format"],int(config["memory"]["interval"]))).start()
threading.Thread(target=time_loop(disk,config["disk"]["format"],int(config["disk"]["interval"]))).start()