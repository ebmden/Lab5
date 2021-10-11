"""
- CS2911 - 011
- Fall 2021
- Lab 5 - HTTP Client
- Names:
  - Eden Basso
  - Lucas Gral

An HTTP client

Introduction: (Describe the lab in your own words) - LG
The goal of this lab was to impliment an HTTP client; a program that makes HTTP requests, parses the responses, and saves the response data to a file,
just like a web browser (albiet without the graphics). The program should send a valid HTTP request (via TCP) to the host provided
to the http_do_exchange function. After making the request, out progam has to receive the HTTP TCP response, and successfully decode it
to save the HTTP body contents to a file. The result of running the program should be newly created files that contain the data received by
the HTTP response(s).

Summary: (Summarize your experience with the lab, what you learned, what you liked, what you
   disliked, and any suggestions you have for improvement) - EB





"""

# import the "socket" module -- not using "from socket import *" in order to selectively use items
# with "socket." prefix
import socket
import ssl

# import the "regular expressions" module
import re


def main():
    """
    Tests the client on a variety of resources
    """

    # These resource request should result in "Content-Length" data transfer
    get_http_resource('http://www.httpvshttps.com/check.png', 'check.png')

    # this resource request should result in "chunked" data transfer
    get_http_resource('http://www.httpvshttps.com/',
                      'index.html')
    
    # HTTPS example. (Just for fun.)
    get_http_resource('https://www.httpvshttps.com/', 'https_index.html')

    get_http_resource('https://www.google.com/', 'google.html')

    get_http_resource('https://www.youtube.com/', 'youtube.html')

    # If you find fun examples of chunked or Content-Length pages, please share them with us!



def get_http_resource(url, file_name):
    """
    Get an HTTP resource from a server
           Parse the URL and call function to actually make the request.

    :param url: full URL of the resource to get
    :param file_name: name of file in which to store the retrieved resource

    (do not modify this function)
    """

    # Parse the URL into its component parts using a regular expression.
    if url.startswith('https://'):
        use_https = True
        protocol = 'https'
        default_port = 443
    else:
        use_https = False
        protocol = 'http'
        default_port = 80
    url_match = re.search(protocol+'://([^/:]*)(:\d*)?(/.*)', url)
    url_match_groups = url_match.groups() if url_match else []
    #    print 'url_match_groups=',url_match_groups
    if len(url_match_groups) == 3:
        host_name = url_match_groups[0]
        host_port = int(url_match_groups[1][1:]) if url_match_groups[1] else default_port
        host_resource = url_match_groups[2]
        print('host name = {0}, port = {1}, resource = {2}'.
                format(host_name, host_port, host_resource))
        status_string = do_http_exchange(use_https, host_name.encode(), host_port,
                                         host_resource.encode(), file_name)
        print('get_http_resource: URL="{0}", status="{1}"'.format(url, status_string))
    else:
        print('get_http_resource: URL parse failed, request not sent')


def do_http_exchange(use_https, host, port, resource, file_name):
    """
    Get an HTTP resource from a server

    :param use_https: True if HTTPS should be used. False if just HTTP should be used.
           You can ignore this argument unless you choose to implement the just-for-fun part of the
           lab.
    :param bytes host: the ASCII domain name or IP address of the server machine (i.e., host) to
           connect to
    :param int port: port number to connect to on server host
    :param bytes resource: the ASCII path/name of resource to get. This is everything in the URL
           after the domain name, including the first /.
    :param file_name: string (str) containing name of file in which to store the retrieved resource
    :return: the status code
    :rtype: int
    :author: Lucas Gral
    """

    http_client_socket = create_http_socket(host, port, use_https)
    status = get_http_data(http_client_socket, host, resource, file_name)
    http_client_socket.close()
 
    return status  # Replace this "server error" with the actual status code

# Define additional functions here as necessary
# Don't forget docstrings and :author: tags


def create_http_socket(host, port, use_https):
    """
    Creates client socket and connects it to the server

    :param bytes host: ASCII domain name or IP address of host
    :param int port: port number to connect to on server host
    :return: client data socket
    :rtype: socket.pyi
    :author: Eden Basso
    """
    http_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_client_socket.connect((host, port))

    if use_https:
        context = ssl.create_default_context()
        ssl_socket = context.wrap_socket(http_client_socket, server_hostname=host)
        return ssl_socket

    return http_client_socket


def get_http_data(http_client_socket, host, resource, file_name):
    """
    Sends HTTP request to receive data from socket and saves the appropriately parsed body to a file

    :param socket.pyi http_client_socket: the client data socket used to collect the resource of the URL
    :param bytes resource: the ASCII path/name of resource to get. This is everything in the URL
           after the domain name, including the first /.
    :param file_name: string (str) containing name of file in which to store the retrieved resource
    :return: status
    :rtype: int
    :author: Lucas Gral
    """
    http_send_request(http_client_socket, host, resource)
    (status, resource_data, resource_type) = http_get_response(http_client_socket)  # http_client_socket may need to return a Dictionary at somepoint once method is complete
    save_resource_to_file(file_name, resource_data, resource_type)
    return status

def http_send_request(http_client_socket, host, resource):
    """
    ...

    :param:
    :param:
    :return:
    :rtype:
    :author: Lucas Gral
    """

    request = b'GET ' + resource + b' HTTP/1.1\r\n'
    request += b'host: ' + host + b'\r\n'
    request += b'\r\n'
    print("requesting", request, "from", host)
    http_client_socket.sendall(request)
    print("sent request")

def http_get_word(http_client_socket):
    """
    Gets the next string of characters surounded by space or ending in \r\n
    Returns the string, and also whether it's the end of the line.

    This could be used instead of next_byte or socket.recv

    :param socket.pyi http_client_socket: client data socket
    :return: (word, endOfLine)
    :rtype: tuple
    :author: Eden Basso
    """

    lastByte = b''
    word = b''
    while (lastByte := http_client_socket.recv(1)) != b' ':
        if(lastByte == b'\r'):
            if((lastByte := http_client_socket.recv(1)) == b'\n'):
                return (word, True)
            else:
                word += b'\r'+lastByte
        else:
            word += lastByte
    return (word, False)

def http_get_response(http_client_socket):
    """
    Parses through response to determine what protocol to use for reading its data

    :param socket.pyi http_client_socket: client data socket
    :return: library holding information necessary to save data
    :rtype: library
    :author: Eden Basso
    """

    """
    #FOR TESTING http_get_word
    while True:
        print(http_get_word(http_client_socket))
        input()
    """

    status = http_get_status_code(http_client_socket) #Added this just to see if everything so far is working

    resource_info = http_read_header(http_client_socket)  # parses through header which returns body size and is_chuncked

    print(resource_info)

    resource_data = read_response_data(http_client_socket, resource_info) # uses resource type to get resource data in response body

    return (status, resource_data, resource_info[b'Content-Type:'] if (b'Content-Type:' in resource_info) else b'text/html;charset=utf-8')

def http_get_status_code(http_client_socket):
    """
    Gets the status code from the first http response line

    :param socket.pyi http_client_socket: client data socket
    :return: status code
    :rtype: int
    :author: Lucas Gral
    """

    version = http_get_word(http_client_socket)  # expecting HTTP/1.1
    status = http_get_word(http_client_socket)
    print("Status", status[0], http_get_word(http_client_socket)[0])
    while http_get_word(http_client_socket)[1] == False:
        pass
    return status[0]


def http_read_header(http_client_socket):
    """
    Parses through the status line to determine the size of the body and if the data is chunked or content length

    :param socket http_client_socket: the client socket to receive from
    :return: dictionary of all header fields
    :rtype: Dictionary
    :author: Eden Basso:
    """
    resource_info = dict()

    latest_word = b''

    while (latest_word := http_get_word(http_client_socket))[0] != b'':
        key = latest_word[0]
        value = b''
        while (latest_word := http_get_word(http_client_socket))[1] != True:
            value += latest_word[0]
        value += latest_word[0]

        resource_info[key] = value

    return resource_info

def read_response_data(http_client_socket, resource_type):
    """
    Gets the body of the response, and interprets it via resource_type

    :param socket http_client_socket: the client socket to receive from
    :param dictionary resource_type: key value pairs for the resource fields
    :return: the resource data
    :rtype: bytes
    :author: Lucas Gral
    """

    if b'Content-Length:' in resource_type:
        return read_length_response_data(http_client_socket, resource_type)
    elif (b'Transfer-Encoding:' in resource_type) and (resource_type[b'Transfer-Encoding:'] == b'chunked'):
        return read_chunked_response_data(http_client_socket, resource_type)

def read_chunked_response_data(http_client_socket, resource_type):
    """
    Interprets body of response as chuncked

    :param socket http_client_socket: the client socket to receive from
    :param dictionary resource_type: key value pairs for the resource fields
    :return: the resource data
    :rtype: bytes
    :author: Lucas Gral
    """

    data = b''

    while (chunkSize := http_get_word(http_client_socket)[0]) != b'0':
        if(chunkSize == b''):
            continue
        print("Chunk of", chunkSize, "bytes")
        for i in range(0, int(chunkSize.decode('ASCII'), 16)):
            data += http_client_socket.recv(1)

    return data

def read_length_response_data(http_client_socket, resource_type):
    """
    Interprets body of response as one stream of length content-length

    :param socket http_client_socket: the client socket to receive from
    :param dictionary resource_type: key value pairs for the resource fields
    :return: the resource data
    :rtype: bytes
    :author: Lucas Gral
    """

    data = b''
    content_length = int(resource_type[b'Content-Length:'].decode('ASCII'))

    for i in range(0, content_length):
        data += http_client_socket.recv(1)

    return data

def save_resource_to_file(file_name, resource_data, resource_type):
    """
    Saves the body of the response to a file

    :param str file_name: name of the file the resource will be saved to
    :param str resource_type: type of body the response has
    :param bytes resource_data: data that will be saved to the file
    :return: the file containing the read-through data in it
    :rtype: file
    :author: Eden Basso
    """
    with open(file_name, 'wb') as file:
        file.write(resource_data)

#  invokes main() function
main()

