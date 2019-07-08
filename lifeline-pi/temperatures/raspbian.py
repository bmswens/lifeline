import subprocess


def main(**kwargs):

    temperatures = {}

    response = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"]).decode()

    temperatures['cpu'] = float(''.join([char for char in response if char.isdigit() or char == '.']))

    return temperatures
