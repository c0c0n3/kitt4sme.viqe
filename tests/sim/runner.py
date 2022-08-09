from time import sleep

from fipy.docker import DockerCompose

from tests.sim.report_batch import post_inspection_batch
from tests.util.fiware import wait_on_quantumleap


docker = DockerCompose(__file__)


def bootstrap():
    docker.build_images()
    docker.start()

    wait_on_quantumleap()


def run():
    services_running = False
    try:
        bootstrap()
        services_running = True

        print('>>> sending inspection report batch to VIQE service...')

        success = post_inspection_batch()
        while not success:
            sleep(5)
            success = post_inspection_batch()

        print('>>> ...done!')
        print('>>> you can interact with the simulation environment now')
        print('>>> (hit Ctrl+C to stop simulation)')
        while True:
            sleep(5)

    except KeyboardInterrupt:
        if services_running:
            docker.stop()
