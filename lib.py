import os
import io
import re
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

posts = {}
gets = {}

def find_get(path):
    """ [Internal] - Used by the Handler class to try and
        find the correct handler for a GET request.
    """
    try:
        return gets[path]()
    except Exception as e:
        print(type(e), e)
        return "404"


def find_post(path, request):
    """ [Internal] - Used by the Handler class to try and
        find the correct handler for a POST request.
    """
    try:
        return posts[path](request)
    except Exception as e:
        print(type(e), e)
        return "404"

def get_relative_path():
    return os.path.dirname(os.path.abspath(__file__))


def read_html(relative_file_path):
    """ Reads the html file on the file location provided
        and injects any external files (marked with {{file_path}} )
        that may be present. Returns the html content as a string.

        Example:
        >>> html_string = read_html('templates/index.html')
    """
    dir_path = get_relative_path()
    file_path = os.path.join(dir_path, relative_file_path)
    with open(file_path) as file:
        html_content = file.read()
        html_content = inject_external_files(html_content)
    return html_content

def inject_external_files(html_content):
    """ [Internal] - Replaces {{ 'file_path' }} with the file content of that file
        path. Useful for seperation of javascript and css files.
        Uses regex to capture the pattern. Here is a link to see how it
        works: https://regex101.com/r/v917NK/2
    """
    # https://regex101.com/
    pattern = r'{{([^}]+)}}'
    external_files = re.findall(pattern, html_content)
    new_html_content = html_content
    for match in external_files:
        external_file_path = match.replace(' ', '')
        external_file = open(os.path.join(get_relative_path(), external_file_path))
        file_content = external_file.read()
        external_file.close()

        if match.find('.css') != -1:
            file_content = '<style>\n' + file_content + '</style>'
        elif match.find('.js') != -1:
            file_content = '<script>\n' + file_content + '</script>'

        to_be_replaced = '{{' + match + '}}'
        new_html_content = new_html_content.replace(to_be_replaced, file_content)
    return new_html_content


def post(route = '/'):
    """ A decorator that takes in the route path as argument, and then
    puts the post handler in the dictionary, with the route as a key.
    The handler will receive one `str` argument called 'body',
    where the body of the post request will exist. """

    def decorator(handler_function):
        posts[route] = handler_function
        return handler_function

    return decorator

def get(route = '/'):
    """ A decorator that takes in the route path as argument, and then
    puts the get handler in the dictionary, with the route as a key.
    The handler function should return either `bytes` or `str`. """

    def decorator(handler_function):
        gets[route] = handler_function
        return handler_function

    return decorator


# Explanation: https://blog.anvileight.com/posts/simple-python-http-server/

class Handler(BaseHTTPRequestHandler):
    """ [Internal] - The class responsible for handling all the
        different requests made to our server.
    """

    def _set_headers(self):
        """ Sets the headers for a response. This is to tell the browser
            the status of the request that was sent. '200' means that everything
            went fine.
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """ Tries to find the handler for this GET request. The handler can
            return either `bytes` or `str`.
        """
        self._set_headers()
        res = find_get(self.path)
        if hasattr(res, 'encode'):
            self.wfile.write(res.encode())
        else:
            self.wfile.write(res)


    def do_POST(self):
        """ Tries to find the handler for this POST request. The handler
            will get the 'body' of the request as the argument. The body
            is a `str`, formatted in JSON.
        """
        self.send_response(200)
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        res = find_post(self.path, body.decode('utf-8'))
        self.wfile.write(res.encode())


def run_server (port = 8314):
    server_adress = ('', port) # Should make the port a command line argument
    server = HTTPServer(server_adress, Handler)
    print('Starting server on port: {}.'.format(port))
    server.serve_forever()
