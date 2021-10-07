"""
- CS2911 - 011
- Fall 2021
- Lab 5 - HTTP Client
- Names:
  - Eden Basso
  - Lucas Gral

An HTTP client

Introduction: (Describe the lab in your own words) - LG




Summary: (Summarize your experience with the lab, what you learned, what you liked, what you
   disliked, and any suggestions you have for improvement) - EB





"""

# import the "socket" module -- not using "from socket import *" in order to selectively use items
# with "socket." prefix
import socket

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
    # get_http_resource('https://www.httpvshttps.com/', 'https_index.html')

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

    socket = create_http_socket(host, port)
    #if use_https ... in future
    get_http_data(socket, resource, file_name)
    socket.close()
 
    return 500  # Replace this "server error" with the actual status code

# Define additional functions here as necessary
# Don't forget docstrings and :author: tags


def create_http_socket(host, port):
    """
    Creates client socket and connects it to the server

    :param bytes host: ASCII domain name or IP address of host
    :param int port: port number to connect to on server host
    :return: client data socket
    :rtype: socket.pyi
    :author: Eden Basso
    """
    http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_socket.connect((host, port))
    # http_socket.sendall(resource) needs to be called in http_send_request
    return http_socket


def get_http_data(socket, resource, file_name):
    """
    ...

    :param:
    :param:
    :param:
    :return:
    :rtype:
    :author: Lucas Gral
    """
    http_send_request(socket, resource)
    (resource_type, resource_data) = http_get_response(socket)
    save_resource_to_file(file_name, resource_type, resource_data)

def http_send_request(http_socket, resource):
    """
    ...

    :param:
    :param:
    :return:
    :rtype:
    :author: Lucas Gral
    """


def http_get_response(http_socket):
    """
    Parses through response to determine what protocol to use for reading its data

    :param socket.pyi http_socket: client data socket
    :return: library holding information necessary to save data
    :rtype: library
    :author: Eden Basso
    """
    response = http_socket.recv()
    # reads through status line parses through and returns status code
    # parses through header which returns body size and is_chuncked
    # parses through body using protocol for data


def save_resource_to_file(file_name, recource_type, resource_data):
    """
    Saves the body of the response to a file

    :param str file_name: name of the file the resource will be saved to
    :param str resource_type: type of body the response has
    :param bytes resource_data: data that will be saved to the file
    :return: the file containing the read-through data in it
    :rtype: file
    :author: Eden Basso
    """

main()
