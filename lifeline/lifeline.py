import datetime
import subprocess
import uuid
import time
import os

# second party
import temperatures

# third party
import yaml
import elasticsearch

NOW = datetime.datetime.utcnow().isoformat()


def get_conf(file):

    with open(file) as stream:

        conf = yaml.safe_load(stream)

    return conf


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


def get_memory(**kwargs):

    # stuff to get from kwargs
    client = kwargs['client'].get('name', 'Unknown Client')
    ip = kwargs['client'].get('ip', '127.0.0.1')

    usage = subprocess.check_output(['top', '-b', '-n', '1']).decode()
    memory_line = usage.split('\n')[3]

    # convert the line to usable info
    memory_usage = convert_line(memory_line)

    doc = {
        'client': client,
        'ip': ip,
        'total': memory_usage[0],
        'free': memory_usage[1],
        'used': memory_usage[2],
        'cached': memory_usage[3],
        'usage': (memory_usage[2] / memory_usage[0]) * 100,
        'datetime': NOW
    }

    return doc


def get_cpu(**kwargs):
    # stuff to get from kwargs
    client = kwargs['client'].get('name', 'Unknown Client')
    ip = kwargs['client'].get('ip', '127.0.0.1')

    usage = subprocess.check_output(['top', '-b', '-n', '1']).decode()
    cpu_line = usage.split('\n')[2]

    # convert to usable info
    cpu_usage = convert_line(cpu_line)

    doc = {
        'client': client,
        'ip': ip,
        'user': cpu_usage[0],
        'system': cpu_usage[1],
        'nice': cpu_usage[2],
        'idle': cpu_usage[3],
        'wait': cpu_usage[4],
        'hardware_interrupt': cpu_usage[5],
        'software_interrupt': cpu_usage[6],
        'steal': cpu_usage[7],
        'usage': 100.0 - cpu_usage[3],
        'datetime': NOW
    }

    return doc


def get_storage(**kwargs):

    # stuff to get from conf
    client = kwargs['client'].get('name', 'Unknown Client')
    ip = kwargs['client'].get('ip', '127.0.0.1')

    total_storage = 0
    used_storage = 0
    free_storage = 0

    storage = {}

    # every thing in GB for now
    response = subprocess.check_output(['df', '-BG']).decode()

    for line in response.split('\n')[1:]:

        usage = line.split()

        if not usage or line.startswith('//'):
            continue

        for index in range(1, 5):

            usage[index] = int(usage[index][:-1])

        storage[usage[0]] = {
            "total": usage[1],
            "used": usage[2],
            "free": usage[3],
            "usage": usage[4],
            "mount_point": usage[5]
        }

        total_storage += usage[1]
        used_storage += usage[2]
        free_storage += usage[3]

    doc = {
        'client': client,
        'ip': ip,
        'datetime': NOW,
        'storage': storage,
        'total_storage': total_storage,
        'used_storage': used_storage,
        'free_storage': free_storage,
        'usage': (used_storage / free_storage) * 100
    }

    return doc


def get_temps(**kwargs):

    # stuff to get from conf
    client = kwargs['client'].get('name', 'Unknown Client')
    ip = kwargs['client'].get('ip', '127.0.0.1')
    temperature_conf = kwargs['client'].get('temperatures')
    operating_system = kwargs['client'].get('os')

    temps = temperatures.get_temperatures(operating_system, **temperature_conf)

    doc = {
        'client': client,
        'ip': ip,
        'datetime': NOW
    }

    for key in temps:

        value = temps[key]
        doc[key] = value

    return doc


def get_bytes():
    rx_bytes = 0
    tx_bytes = 0

    response = subprocess.check_output(['cat', '/proc/net/dev']).decode()

    for line in response.split('\n'):
        if 'enp4s0' in line or 'eth0' in line:
            current = line.split()
            rx_bytes = int(current[1])
            tx_bytes = int(current[9])

    return rx_bytes, tx_bytes


def get_network(**kwargs):
    # stuff to get from conf
    client = kwargs['client'].get('name', 'Unknown Client')
    ip = kwargs['client'].get('ip', '127.0.0.1')

    start_rx, start_tx = get_bytes()
    time.sleep(3)
    end_rx, end_tx = get_bytes()

    # get the difference and convert to Kb/s
    rx_dif = (end_rx - start_rx) * 10 ** -3
    tx_dif = (end_tx - start_tx) * 10 ** -3

    doc = {
        "client": client,
        "ip": ip,
        "in": rx_dif,
        "out": tx_dif,
        "datetime": NOW
    }

    return doc


def main():

    directory = os.path.split(os.path.realpath(__file__))[0]

    conf_file = os.path.join(directory, 'lifeline.yml')
    conf = get_conf(conf_file)
    elastic = f"http://{conf['server']['ip']}:{conf['server']['port']}"
    database = elasticsearch.Elasticsearch([elastic])

    doc = get_temps(**conf)
    response = database.create(index='temperatures', id=uuid.uuid4(), body=doc)
    doc = get_memory(**conf)
    response = database.create(index='memory', id=uuid.uuid4(), body=doc)
    doc = get_cpu(**conf)
    response = database.create(index='cpu', id=uuid.uuid4(), body=doc)
    doc = get_storage(**conf)
    response = database.create(index='storage', id=uuid.uuid4(), body=doc)
    doc = get_network(**conf)
    response = database.create(index='network', id=uuid.uuid4(), body=doc)


if __name__ == '__main__':
    main()