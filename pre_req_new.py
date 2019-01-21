import urllib.request, json, sys, threading, time, math, os, platform

class myThread (threading.Thread):
   def __init__(self, name, courses):
      threading.Thread.__init__(self)
      
      self.name = name
      self.courses = courses
   def run(self):
        print ("Starting " + self.name)
        global process_counter
        for i in range(len(self.courses)):
            course_name = '{}/{}'.format(self.courses[i]['subject'],self.courses[i]['catalog_number'])

            url_service_courses_prerequisites= "courses/{}/{}/prerequisites.json?".format(self.courses[i]['subject'], self.courses[i]['catalog_number'])
            url = url_base + url_service_courses_prerequisites + url_apikey

            with urllib.request.urlopen(url) as u:
                encoding= u.info().get_content_charset('utf-8')
                prereq = json.loads(u.read().decode(encoding))
            
            sem.acquire()
            if 'prerequisites_parsed' in prereq['data'] and prereq['data']['prerequisites_parsed'] is None:
                # Edge cases
                pass
            elif 'prerequisites_parsed' in prereq['data'] and prereq['data']['prerequisites_parsed'] is not None:
                preReqDict[course_name] = prereq['data']['prerequisites_parsed']
            else:
                preReqDict[course_name] = []
            sem.release()
            
            #increase progress counter
            sem_counter.acquire()
            process_counter +=1
            sem_counter.release()

        print ("Exiting " + self.name)
        sem_exit.release()

"""
    GLOBAL VARIABLES
"""
url_base= "https://api.uwaterloo.ca/v2/"
url_apikey= "key="+os.environ['UW_API_KEY0']

num_threads = 6

sem = threading.Semaphore()                 # Semaphore for dictionary
sem_exit = threading.Semaphore()            # Semaphore for parent thread to continue
sem_counter = threading.Semaphore()         # Semaphore for progress bar

preReqDict = {}                             # Dictionary that stores the prerequisites per course

process_counter = 0                         # used for progress bar
total_process = 0                           # used for progress bar
bar_length = 100                            # length of progress bar
percent = 0                                 # used for progress bar

if platform.system() == 'Linux' or platform.system() == 'Darwin':
    clear = lambda: os.system('clear')      # clear screen linux and Mac
elif platform.system == 'Windows':
    clear = lambda: os.system('cls')        # clear screen on windows


"""
    Functions
"""
# Return a Json Object of all courses and there properties
def getCourses():
    url_service_courses= "courses.json?"
    url= url_base + url_service_courses + url_apikey

    with urllib.request.urlopen(url) as u:
        encoding= u.info().get_content_charset('utf-8')
        data = json.loads(u.read().decode(encoding))
    return data
            
"""
    Main
"""            
if __name__ == "__main__":

    #save all courses in seperate JSON file
    course_dict = getCourses()
    with open('./courses.json', 'w') as fp:
        json.dump(course_dict, fp)

    course_array = course_dict['data']
    lower_bound = 0
    upper_bound = 0
    multiplier = math.floor(len(course_array)/num_threads)
    total_process = len(course_array)

    # Creating threads. Each thread gets the same number of courses to process
    for x in range(num_threads):
        
        if x == 0:
            lower_bound = 0
        else:
            lower_bound = (x)*multiplier+1
        if x == (num_threads-1):
            upper_bound = len(course_array)
        else:
            upper_bound = (x+1)*multiplier + 1

        # print("Lower Bound: {} Upper Bound: {}".format(lower_bound, upper_bound))
        # myThread(name, courses)
        thread = myThread("Thread-{}".format(x), course_array[lower_bound:upper_bound])
        thread.start()

    """ 
        Progress Bar
    """
    while True:
        clear()
        sem_counter.acquire()
        pc = process_counter
        sem_counter.release()

        percent = round(100.0*(pc/total_process))
        # print(percent)
        print("processing...")
        print("[{}{}] {}/{}".format("="*percent, "-"*(100-percent), pc, total_process))
        
       
        time.sleep(2)
        if pc == total_process:
            clear()
            print("Finished")
            break


    # wait for all threads to finish
    for x in range(num_threads):
        sem_exit.acquire()
    # create the JSON file
    with open('./prereq.json', 'w') as fp:
        json.dump(preReqDict, fp)



