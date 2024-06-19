from lib.client import Client
from unittest.mock import patch, MagicMock
import socket 
import pytest 
import threading 

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050 
ADDR = (SERVER, PORT)

@patch('builtins.input', return_value='George')
@patch('socket.socket')
@patch('threading.Thread')

def test_client_initialisation(mock_thread, mock_socket, mock_input):
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance

    cli = Client()

    mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
    mock_socket_instance.connect.assert_called_once_with(ADDR)

    assert cli.nickname == 'George'

    assert cli.connected == True

    assert mock_thread.call_count == 2

    mock_thread.assert_any_call(target=cli.receive)
    mock_thread.assert_any_call(daemon=True, target=cli.send_msg)




    



