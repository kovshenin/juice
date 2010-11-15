"""
	Usage: 
		1. {% google_analytics UA-XXXXXXX-X %}
		2. {% yandex_metrica XXXXXXX %}
		
	Outputs:
		1. The Analytics tracking code for Google Analytics
		2. The Metrica tracking code for Yandex Metrica
"""

from django import template
#from juice.taxonomy.models import Term, TermRelation

register = template.Library()

@register.tag
def google_analytics(parser, token):
	tag_name, auth = token.split_contents()
	return GoogleAnalyticsNode(auth)
	
@register.tag
def yandex_metrica(parser, token):
	tag_name, auth = token.split_contents()
	return YandexMetricaNode(auth)	
	
class GoogleAnalyticsNode(template.Node):
	def __init__(self, auth):
		self.auth = auth
	def render(self, context):		
		tracking_code = '''
			<script type="text/javascript">
			  var _gaq = _gaq || [];
			  _gaq.push(['_setAccount', '%(auth)s']);
			  _gaq.push(['_trackPageview']);
			  (function() {
				var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
				ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
				var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
			  })();
			</script>
		''' % {'auth': self.auth}
		
		return tracking_code

class YandexMetricaNode(template.Node):
	def __init__(self, auth):
		self.auth = auth
	def render(self, context):
		tracking_code = '''
			<!-- Yandex.Metrika -->
			<script src="//mc.yandex.ru/metrika/watch.js" type="text/javascript"></script>
			<div style="display:none;"><script type="text/javascript">
			try { var yaCounter%(auth)s = new Ya.Metrika(%(auth)s);
			yaCounter%(auth)s.clickmap();
			yaCounter%(auth)s.trackLinks({external: true});
			} catch(e){}
			</script></div>
			<noscript><div style="position:absolute"><img src="//mc.yandex.ru/watch/%(auth)s" alt="" /></div></noscript>
			<!-- /Yandex.Metrika -->
		''' % {'auth': self.auth}
		
		return tracking_code
