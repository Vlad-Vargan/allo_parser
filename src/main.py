from multiprocessing import cpu_count
from itertools import combinations
import threading
import requests
import json
import time

from database import DbInterface

url = "https://allo.ua/ua/catalogsearch/ajax/suggest/?currentTheme=main&currentLocale=uk_UA"

def get_permutations():
    # return all possible 1-3 letter permutaions
    permutations = []
    rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    eng = "abcdefghijklmnopqrstuvwxyz"
    for lang in [rus, eng]:
        for i in [1,2,3]:
            permutations+= ["".join(comb)for comb in combinations(lang,i)]
    return permutations

def get_products(bunch):
    thread, permutations, db = bunch
    for perm in permutations:
        res = requests.post(url, data={"q": perm})
        # in case of server overload wait
        try:
            res = res.json()
            if "query" in res:
                print(thread, perm, len(res["query"]))
                try:
                    # append products in case they exist
                    db.add_products(perm, res["query"])
                except:
                    print(f"Trouble with DB {thread}")
            else:
                print(f"no products for {perm}")
                db.add_no_products(perm)
        except Exception as e:
            print(f"ERROR {e}")
            print(f"Thread{thread}", perm, res)
            time.sleep(5)
    print(f"Thread {thread} done with {permutations} promts")

def chunks(lst, n):
    # Yield successive n-sized chunks from lst.
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main():
    permutations = get_permutations()
    db_path = "products.db"
    # get already checked promts
    already_exist = DbInterface(db_path).check_products()
    # find promts we didn't check
    do_not_exist = sorted(list(set(permutations)^set(already_exist)))
    
    if do_not_exist == []:
        print("No promt to check")
        exit()
    print(f"\nRemoved {len(already_exist)} collisions")
    # i don't know why but only using treads in number 
    # of available cpus is enough to not let server lock
    num_threads = cpu_count() if cpu_count() == 1 else cpu_count()-1

    # calculate number of promts for each thread
    thread_mass = (len(do_not_exist)//num_threads)+1
    print(f"Launching {num_threads} threads, {thread_mass} promts each\n")

    # split promts by threads
    splitted_promts = list(
        # giving a unique db object to each thread to avoid db access recursion
        map(
            lambda el: list(el) + [DbInterface(db_path)],list(
                # giving each thread a unique number
                enumerate(
                    list(
                        chunks(do_not_exist, thread_mass)
                        )
                    )
                )
            )
        )

    # launching threads
    threads = []
    for promt in splitted_promts:
        t = threading.Thread(target=get_products, args=[promt])
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()