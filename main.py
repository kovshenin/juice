import logging, os, sys

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Remove the standard version of Django.
for k in [k for k in sys.modules if k.startswith('django')]:
    del sys.modules[k]

# Force sys.path to have our own directory first, in case we want to import
# from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + '/django.zip')

# Must set this env var *before* importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

def log_exception(*args, **kwds):
   logging.exception('Exception in request:')

# Log errors.
django.core.signals.got_request_exception.connect(log_exception)

# Unregister the rollback event handler.
django.core.signals.got_request_exception.disconnect(django.db._rollback_on_exception)

# Fill with dummy data
#if django.conf.settings.DEBUG:
#	import juice.front.dummy
def real_main():
    # Create a Django application for WSGI.
    application = django.core.handlers.wsgi.WSGIHandler()

    # Run the WSGI CGI handler with that application.
    util.run_wsgi_app(application)
    
def profile_main():
	# This is the main function for profiling
	# We've renamed our original main() above to real_main()
	import cProfile, pstats
	from google.appengine.api import memcache

	prof = cProfile.Profile()
	prof = prof.runctx("real_main()", globals(), locals())
	print "<!-- Profiling"
	stats = pstats.Stats(prof)
	stats.sort_stats("time")  # Or cumulative
	stats.print_stats(80)  # 80 = how many to print
	
	mc = memcache.get_stats()
	print "Memcache hits: %s, misses: %s" % (mc['hits'], mc['misses'])
	# The rest is optional.
	# stats.print_callees()
	# stats.print_callers()
	print "-->"

main = profile_main

if __name__ == '__main__':
    main()
