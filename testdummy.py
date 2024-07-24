import threading
import time
import functions as func
import signatone_driver as Signatone
import siglent_driver as Siglent

stop_event = threading.Event()


def main_task(signatone, siglent_var, filename):
    siglent_var.output_on()
    siglent_var.set_volt(1)
    siglent_var.get_output()
    while not stop_event.is_set():
        time.sleep(20)
        image = func.take_image(1, filename)
        signatone.save_image(image)
    siglent_var.reset_values()
    siglent_var.output_off()


def stop_listener():
    input("Press 'e' to stop etching:")
    stop_event.set()


def main():
    filename = None
    signatone = Signatone.Signatone()
    siglent_var = Siglent.Siglent()

    # Start the main task in a separate thread
    task_thread = threading.Thread(target=main_task, args=(signatone, siglent_var, filename))
    task_thread.start()

    # Start the stop listener in the main thread
    stop_listener()

    # Wait for the task to finish
    task_thread.join()


if __name__ == '__main__':
    main()
