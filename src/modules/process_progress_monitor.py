import time
def monitor_process_progress(status_queue,progress_callback):
    current_progress=0
    while current_progress<100:
        print('asd')
        if not status_queue.empty():
            current_progress=status_queue.get()
            progress_callback.emit(current_progress)
            # if isinstance(current_progress,int):
            #     progress_callback.emit(current_progress)
            # else:
            #     progress_callback.emit(str(current_progress[1]))
            #     return
            if not isinstance(current_progress,int):
                return
        time.sleep(2)
    progress_callback.emit(100)