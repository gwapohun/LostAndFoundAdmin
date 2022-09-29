
import socket
from pickle import dumps


def send_files( data : dict, ip : str , port : int ) :
	# Turn To Bytes Object
	try :
		new_data : bytes = dumps(data)
	except Exception :
		return None
	print("Turn Tp Objects")
	# Create Socket
	client = socket.socket( socket.AF_INET , socket.SOCK_STREAM)
	try :
		client.connect( ( ip , port ) )
	except Exception :
		return None
	print("Connected To Server")
	# Send Data
	try :
		client.sendall(new_data)
	except Exception :
		return None
	print("Send To Server")
	return True
	
	