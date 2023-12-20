import threading

def task_foo(tasl_id):
	
	counter = 0

	for i in range(1000000):
		counter += i ** 2
	
	print(f"Worked task {tasl_id}")


tasks = [threading.Thread(target = task_foo, args= (i,)) for i in range(5)]

for task in tasks:
	task.daemon = True
	task.start()

for task in tasks:
	task.join()





