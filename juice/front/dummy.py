from juice.posts.models import Post
from juice.pages.models import Page
from juice.chunks.models import Chunk

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

dummy()
