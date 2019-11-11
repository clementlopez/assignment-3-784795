#!/usr/bin/python3

from mysimbdpstreamingestmanager import run_manager
import paho.mqtt.client as mqtt

max_proc_time_wanted = 1
# min_proc_time_wanted = 0.01

processRunningForCustomer1 = []
processRunningForCustomer2 = []

def on_message(client, userdata, msg):
    messageTable = eval(msg.payload.decode())
    cust = messageTable[0]
    proc_time = messageTable[1]
    manage(cust, proc_time)

def manage(cust, proc_time):
    if proc_time > max_proc_time_wanted:
        scaleup(cust)
    # if proc_time < min_proc_time_wanted:
    #     scaledown(cust)
    return 0

def scaledown(customerID):
    if customerID == "customer-1" and processRunningForCustomer1:
        pid_to_kill = processRunningForCustomer1.pop(0)
    if customerID == "customer-2" and processRunningForCustomer2:
        pid_to_kill = processRunningForCustomer2.pop(0)
    if pid_to_kill:
        run_manager(customerID, "stop", int(pid_to_kill))


def scaleup(customerID):
    pid = run_manager(customerID, "start")
    if customerID == "customer-1":
        processRunningForCustomer1.append(pid)
    else:
        processRunningForCustomer2.append(pid)

if __name__ == "__main__":
    client = mqtt.Client()
    client.connect("databroker")
    client.subscribe("reportStream")
    client.on_message = on_message
    client.loop_forever()