# appengine_config.py

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" and "tools" folders.

vendor.add('lib')
vendor.add('tools')