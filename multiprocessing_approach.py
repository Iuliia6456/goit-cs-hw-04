import multiprocessing
import logging
import timeit


logging.basicConfig(level=logging.INFO, format='\n[%(processName)s %(process)d] %(message)s')

def search_files(keyword, file_list, result_queue):
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

    result_queue.put((keyword, keyword_results))
    

def create_and_run_processes(keywords, file_list, result_queue):
    processes = []

    for keyword in keywords:
        process = multiprocessing.Process(target=search_files, args=(keyword, file_list, result_queue), name=f"Process")
        processes.append(process)

    for process in processes:
        try:
            process.start()
        except Exception as e:
            logging.error(f"Error starting process '{process.name}': {e}")

    for process in processes:
        process.join()

def main():
    # the list of files and keywords
    file_list = ["file1.txt", "file2.txt", "file3.txt"]
    keywords = ["light", "surprise", "Happy", "XXX "]
    result_queue = multiprocessing.Queue()

    create_and_run_processes(keywords, file_list, result_queue)

    result_dict = {}
    while not result_queue.empty():
        keyword, keyword_results = result_queue.get()
        result_dict[keyword] = keyword_results
            
    logging.info(f"Results: \n{result_dict}\n") 

if __name__ == '__main__':    
    main()
    time_multiprocessing = timeit.timeit(main, number=1)
    print(f"Execution time for multiprocessing approach: {time_multiprocessing:.5f} seconds\n")