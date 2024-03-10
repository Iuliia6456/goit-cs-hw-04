import threading
import logging
import timeit

logging.basicConfig(level=logging.INFO, format='\n[%(threadName)s %(thread)d] %(message)s')

def search_files(keyword, file_list, result_dict, lock):
    logging.info(f"Searching for '{keyword}' in files: {file_list}")

    keyword_results = []

    for file_name in file_list:
        try:
            with open(file_name, 'r') as file:
                text = file.read()
                if keyword.lower() in text.lower():
                    keyword_results.append(file_name)
        except FileNotFoundError:
            logging.error(f"File '{file_name}' not found.")
        except Exception as e:
            logging.error(f"An error occurred while reading '{file_name}': {e}")

    with lock:
        result_dict[keyword.lower()] = keyword_results
    
def create_and_run_threads(keywords, file_list, result_dict, lock):
    threads = []

    for keyword in keywords:
        thread = threading.Thread(target=search_files, args=(keyword, file_list, result_dict, lock), name=f"Thread")
        threads.append(thread)

    for thread in threads:
        try:
            thread.start()
        except Exception as e:
            logging.error(f"Error starting thread '{thread.name}': {e}")

    for thread in threads:
        thread.join()


def main():
    file_list = ["file1.txt", "file2.txt", "file3.txt"]
    keywords = ["light", "surprise", "Happy", "XXX "]
    result_dict = {}
    lock = threading.Lock()

    create_and_run_threads(keywords, file_list, result_dict, lock)

    logging.info(f"Results: \n{result_dict}\n")


if __name__ == '__main__':
    main()
    time_threading = timeit.timeit(main, number=1)
    print(f"Execution time for threading approach: {time_threading:.5f} seconds\n")


