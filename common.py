import simplejson as json
import traceback

def coroutine(func):
	def start(*args,**kwargs):
		cr = func(*args,**kwargs)
		cr.next()
		return cr
	return start

@coroutine
def grep(pattern,target):
	while True:
		line = (yield) # Receive a line
		if pattern in line:
			target.send(line) # Send to next stage


def print_exception(prefix, e):
    print(prefix, str(e))
    print(traceback.format_exc())

@coroutine
def printer(log_filename):
	logfile = open(log_filename, 'w')
	print(log_filename + ' opened!')
	try:
		while True:
			res = (yield)
			logfile.write(str(res))
	finally:
		logfile.close()

@coroutine
def response_filter(pattern, target):
	while True:
		flow = (yield) # Receive a line
		if pattern in flow.request.data.path:
			print('CHAT ---------------' + flow.request.data.path)
			target.send(flow.response.content) # Send to next stage

@coroutine
def decode_json(target):
    while True:
        text = (yield)
        try:
            target.send(json.loads(text))
        except Exception as e:
            print_exception('JSON exception', e)
            raise StopIteration()