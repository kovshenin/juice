from juice.posts.models import Post
from juice.pages.models import Page
from juice.chunks.models import Chunk

from juice.core.models import OptionGroup, Option

def dummy():
	p = Post.all()
	if p.count() == 0:
		# Posts
		for i in range(1, 10):
			p = Post(
				title="Post Title %s" % i,
				slug="post-title-%s" % i,
				excerpt="Here goes a post excerpt",
				content="<p>Lorem ipsum dolor sit amet.</p>"
			)
			p.put()
			
		p = Post(
			title='Lorem Ipsum Dolor Sit Amet',
			slug='lorem-ipsum',
			excerpt = 'Lipsum excerpt',
			content = '<p>Lorem ipsum content: [youtube url="http://www.youtube.com/watch?v=Mk3qkQROb_k"] Yes</p><p>Here is a chunk: <strong>[chunk name="some-chunk"]</strong></p>'
		)
		p.put()
		
		# Chunks
		c = Chunk(
			name='title',
			content='Juice Toolkit'
		)
		c.put()
		
		c = Chunk(
			name='slogan',
			content='Why reinvent the web?'
		)
		c.put()
		
		c = Chunk(
			name='some-chunk',
			content='This is the content of some chunk'
		)
		c.put()
		
		c = Chunk(
			name='short-bio',
			content='<a href="/about/"><img alt="Konstantin Kovshenin" src="/static/images/me.jpg" /></a><p>Hi! I\'m Konstantin, a web developer from Moscow, Russia. CTO at <a href="http://frumatic.com">Frumatic</a><br /><a href="/about/">More</a> &raquo;</p>'
		)
		c.put()
		
		# Pages
		p = Page(
			title='About',
			slug='about',
			content='<p>About me, also check out my <a href="/about/bio/">biography</a>.</p>'
		)
		p.put()
		
		b = Page(
			title='Bio',
			slug='bio',
			content='<p>Biography</p>',
			parent_page=p.key()
		)
		b.put()
		
		p = Page(
			title='Sitemap',
			slug='sitemap',
			content='<p>Sitemap</p>'
		)
		p.put()
		
		p = Page(
			title='Feedback',
			slug='feedback',
			content='<p>Feedback</p>'
		)
		p.put()
		
		# Options
		
		g = OptionGroup(title='Juice Social Share Widgets', slug='juice-social-share')
		g.put()
		
		o = Option(group=g.key(), name='Twitter', value='<a href=\"http://twitter.com/?status={{ title|urlencode }}{{ " "|urlencode }}{{ permalink_abs|urlencode }}\"><img src=\"/static/images/social/share/twitter.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Digg', value='<a href=\"http://digg.com/submit?url={{ permalink_abs|urlencode }}&amp;title={{ title|urlencode }}\"><img src=\"/static/images/social/share/digg.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Delicious', value='<a href=\"http://www.delicious.com/save\" onclick=\"window.open(\'http://www.delicious.com/save?v=5&noui&jump=close&url={{ permalink_abs|urlencode }}&amp;title={{ title|urlencode }}\', \'delicious\',\'toolbar=no,width=550,height=550\'); return false;\"><img src=\"/static/images/social/share/delicious.png\" alt=\"Delicious\" /></a>')
		o.put()
		
		g = OptionGroup(title='Juice Social Profiles Widgets', slug='juice-social-profiles')
		g.put()
		
		o = Option(group=g.key(), name='Twitter', value='<a href=\"http://twitter.com/kovshenin\"><img src=\"/static/images/social/profiles/twitter.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Facebook', value='<a href=\"http://facebook.com/kovshenin\"><img src=\"/static/images/social/profiles/facebook.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='LinkedIn', value='<a href=\"http://www.linkedin.com/in/kovshenin\"><img src=\"/static/images/social/profiles/linkedin.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Digg', value='<a href=\"http://digg.com/users/kovshenin\"><img src=\"/static/images/social/profiles/digg.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Delicious', value='<a href=\"#\"><img src=\"/static/images/social/profiles/delicious.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='DeviantArt', value='<a href=\"#\"><img src=\"/static/images/social/profiles/deviantart.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Flickr', value='<a href=\"#\"><img src=\"/static/images/social/profiles/flickr.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Google', value='<a href=\"#\"><img src=\"/static/images/social/profiles/google.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Last.fm', value='<a href=\"#\"><img src=\"/static/images/social/profiles/lastfm.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='YouTube', value='<a href=\"#\"><img src=\"/static/images/social/profiles/youtube.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Technorati', value='<a href=\"#\"><img src=\"/static/images/social/profiles/technorati.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='StumpleUpon', value='<a href=\"#\"><img src=\"/static/images/social/profiles/stumbleupon.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='Reddit', value='<a href=\"#\"><img src=\"/static/images/social/profiles/reddit.png\" /></a>')
		o.put()
		
		o = Option(group=g.key(), name='MySpace', value='<a href=\"#\"><img src=\"/static/images/social/profiles/myspace.png\" /></a>')
		o.put()
		
dummy()
