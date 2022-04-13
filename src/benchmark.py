#!/home/fideloper/.envs/eitn30-project/bin/python3

"""Module for producing benchmark plots of the radio link."""

from time import sleep, time_ns
from multiprocessing import Process, Queue
from numpy import random
from matplotlib import pyplot as plt
import pandas as pd

# Project packages
from radio import Radio as radio

# from server import Server as server
# import utilities as util

PIPE_ADDRESSES = [
    b"\xE7\xD3\xF0\x35\x77",
    b"\xC2\xC2\xC2\xC2\xC2",
    b"\xC2\xC2\xC2\xC2\xC3",
    b"\xC2\xC2\xC2\xC2\xC4",
    b"\xC2\xC2\xC2\xC2\xC5",
    b"\xC2\xC2\xC2\xC2\xC6",
]
X_RESOLUTION: int = 200  # Determines the amount of x axis data points, and the input rate denominator (1/X_RESOLUTION seconds)


def transmit(data: Queue, measurement_count=100, resolution=X_RESOLUTION):
    """Transmits elements from the provided queue via radio, and measures performance."""
    r = radio("NODE")
    raw_data = []
    plot_data = []

    for i in range(resolution):
        raw_data.append(_measure(r, data, measurement_count))

    # TODO: Plot and save figure
    for series in raw_data:
        plot_data.append(_calc_median(series))

    df = pd.DataFrame(
        {
            # TODO: Figure out how to differentiate sub plots
            "packet_error_rate": plot_data[0],
            "latency": plot_data[1],
            "queue_size": plot_data[2],
        }
    )

    df.plot(subplots=True, layout=(3, 1), sharex=True)


def queue_input(data_queue: Queue, resolution=X_RESOLUTION):
    """Inputs data elements into provided queue."""
    for i in range(1, resolution + 1):
        _add(data_queue, element_count=100, interval=(1 / i))


def plot(plot_data, x_resolution=X_RESOLUTION):
    pass


def _add(queue: Queue, element_count: int, interval: float):
    """Adds element_count random byte elements to a provided queue with an interval of interval seconds."""
    data = random.bytes(30)

    for i in range(element_count):
        queue.put(data)
        sleep(interval)


def _measure(
    radio: radio,
    data_queue: Queue,
    measurement_count: int,
) -> list[list]:
    "Returns outcome and execution time for the transmit, as well as input queue size."

    latency: list[int] = []
    outcome: list[bool] = []
    queue_size: list[int] = []
    time_start: int
    time_end: int

    for i in range(measurement_count):
        queue_size.append(data_queue.qsize())

        data = data_queue.get(block=True, timeout=5)

        time_start = time_ns()
        outcome.append(radio.transmit(PIPE_ADDRESSES[1], data))
        time_end = time_ns()
        latency.append(time_start - time_end)
    return [outcome, latency, queue_size]


def _calc_median(index_data: list[list[bool], list[int], list[int]]):
    """Calculates the median of each list in the provided list. Returns a 3 by 1 dataframe."""
    data = pd.DataFrame(
        {
            "outcome": index_data(0),
            "latency": index_data(1),
            "queue_size": index_data(2),
        }
    )
    return [
        data["outcome"].sum() / 100,
        data["latency"].median(),
        data["queue_size"].median(),
    ]


def main(data_queue):
    """Runs a multiprocessing main loop."""
    receiver = Process(target=transmit, args=data_queue)
    transmitter = Process(target=queue_input, args=data_queue)

    receiver.start()
    sleep(1)
    transmitter.start()

    receiver.join()
    transmitter.join()


if __name__ == "__main__":

    queue = Queue()
    main(queue)

    try:
        pass
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt\n")
