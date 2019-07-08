import re
import subprocess


def convert_line(line):

    new_line = []

    line = line[line.find(':') + 1:]
    line = line.split(',')

    for item in line:
        new_item = ''.join([char for char in item if char.isdigit() or char == '.'])
        if '.' in new_item:
            new_item = float(new_item)
        else:
            new_item = int(new_item)
        new_line.append(new_item)

    return new_line


def main(**temperature_conf):
    temperature_regex = re.compile(r'\+.*?°C')

    current_sensor = None
    current_sensor_conf = {}
    temperatures = {}

    # sensors provided by lm-sensors
    sensors = subprocess.check_output('sensors').decode().split('\n')

    for line in sensors:

        if line in temperature_conf:
            current_sensor = line
            current_sensor_conf = temperature_conf[current_sensor]

        match = temperature_regex.findall(line)

        if match and current_sensor:

            temp = convert_line(match[0])[0]
            temp += current_sensor_conf['offset']

            if current_sensor_conf['type'] not in temperatures:
                temperatures[current_sensor_conf['type']] = []

            temperatures[current_sensor_conf['type']].append(temp)

    return temperatures
