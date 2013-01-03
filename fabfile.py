from fabric.api import *


@task
def hello_world():
    """Says hello to the world."""
    print 'Hello, world!'
