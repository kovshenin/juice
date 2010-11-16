import datetime
import random
	
from juice.posts.models import Post
from juice.pages.models import Page
from juice.chunks.models import Chunk
from juice.navigation.models import Menu, MenuItem
from juice.taxonomy.models import Term
from juice.comments.models import Comment

from juice.core.models import OptionGroup, Option

def dummy():
	p = Post.all()
	if p.count() == 0:
		# Menus
		
		menu_topright = Menu(
			title="Top Right Short Menu",
			slug="topright"
		)
		menu_topright.put()
		
		# Taxonomy
		category = {}
		category['development'] = Term(taxonomy='category', name='Development', slug='development')
		category['personal'] = Term(taxonomy='category', name='Personal', slug='personal')
		category['design'] = Term(taxonomy='category', name='Design', slug='design')
		
		tag = {}
		tag['google'] = Term(taxonomy='tag', name='Google', slug='google')
		tag['yahoo'] = Term(taxonomy='tag', name='Yahoo', slug='yahoo')
		tag['apple'] = Term(taxonomy='tag', name='Apple', slug='apple')
		
		# Put all categories and tags
		for k in category:
			category[k].put()
		for k in tag:
			tag[k].put()
		
		# Posts
		for i in range(1, 10):
			post_title = lipsum(6)
			post_slug = slugify(post_title)
			post_excerpt = lipsum(20)
			post_content = ""
			for j in range(1, random.randrange(2, 8)):
				post_content += "<p>%s</p>" % get_paragraph()
				
			p = Post(
				title=post_title,
				slug=post_slug,
				excerpt=post_excerpt,
				content=post_content,
				published=datetime.datetime.today() - datetime.timedelta(days=i)
			)
			p.put()
		
		post_title = lipsum(6)
		post_slug = slugify(post_title)
		post_excerpt = lipsum(20)
		post_content = '<p>%s</p>[youtube url="http://www.youtube.com/watch?v=I6COwgigJ-g"]<p>%s</p><p>%s</p>' % (get_paragraph(), get_paragraph(), get_paragraph())
		p = Post(
			title=post_title,
			slug=post_slug,
			excerpt=post_excerpt,
			content=post_content
		)
		p.put()
		
		# Let's add this post to a category and tag it
		category['development'].relations.append(p.key())
		category['development'].put()
		
		tag['yahoo'].relations.append(p.key())
		tag['yahoo'].put()
		
		tag['google'].relations.append(p.key())
		tag['google'].put()
		
		# Let's add a few comments
		comment = Comment(
			name='Konstantin',
			email='kovshenin@live.com',
			url='http://kovshenin.com',
			content='Hey, this is quite an interesting post, thank you sir!',
			object_link=p.key()
		)
		comment.put()
		
		c = Comment(
			name='Konstantin',
			email='konstantin@frumatic.com',
			url='http://frumatic.com',
			content='This is a reply to a previous comment',
			parent_comment=comment.key(),
			object_link=p.key()
		)
		c.put()
		
		
		# Chunks
		c = Chunk(
			name='title',
			content='Juice Toolkit'
		)
		c.put()
		
		c = Chunk(
			name='slogan',
			content='The Power of Python, The Scalability of AppEngine'
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
			content='<p>%s</p><p>%s</p><p>%s</p><p>Don\'t forget to read my <a href="/about/bio/">biography</a>.</p>' % (get_paragraph(), get_paragraph(), get_paragraph())
		)
		p.put()
		i = MenuItem(
			caption="About",
			menu = menu_topright.key(),
			object_link = p.key()
		)
		i.put()
		
		b = Page(
			title='Bio',
			slug='bio',
			content='<p>%s</p><p>%s</p><p>%s</p>' % (get_paragraph(), get_paragraph(), get_paragraph()),
			parent_page=p.key()
		)
		b.put()
		
		p = Page(
			title='Sitemap',
			slug='sitemap',
			content='<p>%s</p><p>%s</p><p>%s</p>' % (get_paragraph(), get_paragraph(), get_paragraph()),
		)
		p.put()
		i = MenuItem(
			caption="Sitemap",
			menu = menu_topright.key(),
			object_link = p.key()
		)
		i.put()
		
		p = Page(
			title='Feedback',
			slug='feedback',
			content='<p>%s</p><p>%s</p><p>%s</p>' % (get_paragraph(), get_paragraph(), get_paragraph()),
		)
		p.put()
		i = MenuItem(
			caption="Feedback",
			menu = menu_topright.key(),
			object_link = p.key()
		)
		i.put()
		
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

def lipsum(count=50, slugify=False):
	lipsum = """
		Donec ultrices ultricies libero, et tristique dolor euismod et. Cras volutpat nulla in turpis consequat et dignissim nunc rhoncus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed sit amet odio dolor. Mauris fermentum, quam vel volutpat lobortis, tellus eros tempus est, varius elementum arcu lectus volutpat felis. Duis aliquam justo eget neque lacinia vitae dictum urna mollis. Praesent id congue ligula. Maecenas vehicula faucibus mauris, id auctor velit mattis nec. Nulla facilisi. In a mauris quis orci malesuada tempor. Etiam molestie consequat tortor, nec vestibulum enim feugiat ac. Aenean vehicula laoreet mauris, eget tristique urna ultrices vitae. Morbi enim orci, consectetur et ornare eu, sollicitudin in libero. Phasellus nisl nunc, iaculis sed scelerisque non, pretium vel mauris. Curabitur sit amet augue sit amet lacus pellentesque facilisis. Nam in ipsum nulla, eu molestie mi. Praesent eget elementum erat.
		Vivamus ornare suscipit lectus, auctor eleifend mauris congue ut. Aenean vel ullamcorper ipsum. Aliquam erat volutpat. Fusce varius mollis nibh ut vestibulum. Nullam turpis velit, luctus id bibendum eu, commodo id lacus. Maecenas libero tortor, pretium at elementum et, pellentesque vitae magna. Morbi eu nulla eu dolor fermentum faucibus eu congue dui. Etiam eu nibh vitae neque rhoncus ultricies. Nunc vitae diam ligula, sit amet mollis libero. Ut fermentum nisl non sem commodo imperdiet. Morbi in mi vitae nunc eleifend varius eget sed nulla. Ut laoreet lacinia mi rhoncus luctus. Mauris blandit pretium ipsum, interdum gravida libero porttitor ut. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.
		Proin commodo, leo elementum gravida iaculis, urna leo imperdiet elit, ac congue dolor ante ornare tortor. Proin dapibus ultricies lorem, imperdiet posuere purus scelerisque et. Morbi nulla eros, mattis nec egestas sed, imperdiet eu nibh. In hac habitasse platea dictumst. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur pellentesque urna non diam dictum adipiscing. Duis vestibulum nibh mi, ac faucibus tortor. Fusce blandit diam eu odio viverra bibendum. Morbi a nunc tortor. Donec id odio dolor, vitae pulvinar massa.
		In aliquam congue felis at varius. Sed a erat elit, quis cursus sapien. Aenean venenatis urna et tellus posuere ut tempus neque imperdiet. Mauris a adipiscing massa. Fusce in dolor sem, eu iaculis nunc. Maecenas massa neque, scelerisque pellentesque posuere in, dignissim eget est. Donec sed ligula quis erat faucibus bibendum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque neque leo, feugiat ac dapibus nec, vestibulum sed est. Vivamus porta mi a erat facilisis eleifend. Duis vel dolor arcu, non mollis risus. Aenean commodo egestas dolor, a rhoncus sapien vestibulum et. Aenean dignissim, dui nec lacinia dapibus, mauris eros pharetra mi, eu varius dui dolor id urna. Aenean vitae nisi eu risus convallis lobortis in ac erat. Integer quis risus quam, nec commodo ligula. Suspendisse sit amet nibh nulla. Ut a nisi est. Phasellus in imperdiet risus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Fusce ultrices faucibus pretium.
		Nam viverra, tortor vitae mollis adipiscing, elit nulla dapibus leo, non egestas massa lacus vel libero. Duis luctus magna eget tortor sollicitudin viverra. Donec id diam felis, sit amet bibendum metus. Sed bibendum feugiat fermentum. Sed eleifend ultricies vehicula. Nulla velit massa, sagittis eget vestibulum eu, semper sed lacus. Fusce non vehicula ipsum. Nullam ipsum orci, pharetra at aliquam sagittis, accumsan ac urna. Duis convallis luctus neque non adipiscing. Proin auctor congue arcu id cursus. Morbi nec turpis auctor neque porttitor malesuada in a ipsum. Phasellus gravida, augue non mattis suscipit, ligula arcu placerat mauris, quis consectetur erat velit sed nisi. In tincidunt, elit in scelerisque condimentum, tellus arcu pellentesque massa, a imperdiet justo leo id nibh.
		Nunc ligula lectus, rutrum non blandit nec, pellentesque et nunc. Suspendisse tellus tellus, sollicitudin eu faucibus et, mattis eget ipsum. Donec et aliquam nisl. Nulla vel felis lacus, id iaculis diam. Ut sed massa ipsum. Nulla facilisi. Donec a urna eu eros lobortis tempor vel nec mi. Maecenas rutrum sodales molestie. Curabitur consectetur condimentum nisl, id accumsan leo viverra id. Duis facilisis pellentesque ultricies. Duis a ipsum lorem, id feugiat sem. Nulla mattis lectus quis nisi sollicitudin sit amet volutpat libero tristique. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In id nunc purus. Fusce sapien ligula, pulvinar in mollis id, blandit sed elit. Sed id nunc rhoncus purus consequat aliquet. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer purus est, gravida et ornare eget, aliquam ac leo. Ut suscipit faucibus massa eget commodo. Suspendisse posuere erat id dolor tempor facilisis.
		Nunc at eleifend mi. Vestibulum a felis eu ligula sodales luctus at ac mi. Proin pellentesque convallis leo sit amet dictum. Vivamus consequat, quam ac pharetra venenatis, sapien ligula bibendum orci, quis consequat mauris ipsum ac magna. Aliquam at purus augue, consequat faucibus leo. Nulla metus lorem, interdum ut mollis a, tempor eget quam. Nulla sed tortor quis odio tempus scelerisque. Morbi consequat vestibulum erat porttitor euismod. Nullam nec tortor ante. Sed non diam non mi lacinia egestas. Nunc commodo faucibus tortor eget bibendum. Donec nec eros quam, sit amet iaculis libero. Morbi in metus nec ante malesuada semper sed ac tellus. Fusce pellentesque urna orci. Aliquam vitae diam vel nunc dictum egestas. Fusce suscipit, nibh et viverra tincidunt, diam magna interdum tellus, vitae porttitor magna arcu vitae odio. In sit amet nibh leo, ac tristique leo.
		Duis mauris ante, tempor bibendum malesuada vel, dictum quis odio. Mauris id dolor sed ligula ultricies aliquet. Donec eget quam quam, id congue neque. Nullam sit amet commodo nulla. Proin lobortis, sapien ut semper suscipit, erat nibh viverra turpis, vitae dignissim quam ipsum sed tellus. Sed pellentesque malesuada augue id aliquet. Aenean ac velit est. Praesent bibendum gravida pharetra. Integer pulvinar, lacus a pretium pellentesque, nulla dui blandit nunc, eget egestas turpis velit sed enim. Morbi laoreet neque sed eros blandit eu volutpat erat fringilla. In vitae est metus. Nulla lectus turpis, dignissim non adipiscing ut, malesuada a elit. Sed et pulvinar mi. Duis sed nibh velit. Pellentesque posuere hendrerit ligula in tempus. Maecenas sed mollis eros.
		Nulla purus velit, convallis et imperdiet sed, interdum faucibus felis. Morbi rhoncus magna a velit condimentum non consectetur leo facilisis. Sed aliquam fringilla cursus. Cras nibh libero, condimentum sit amet placerat nec, elementum eget metus. Fusce a neque purus, quis ullamcorper elit. Morbi vitae est id diam pretium ultricies. Duis nec turpis non nisl suscipit ultrices. Phasellus tristique ornare porta. Pellentesque hendrerit nisl id mauris sollicitudin id pellentesque sem sagittis. Ut libero libero, suscipit quis pulvinar a, semper sit amet metus. Morbi sit amet urna nunc, eget ullamcorper metus. Donec imperdiet tempus vulputate. Proin ornare, augue et condimentum vehicula, felis libero eleifend purus, non placerat est sapien ut sapien. Aenean a gravida lorem. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Aenean iaculis velit eget est congue et posuere risus ultrices. Cras dictum luctus turpis, quis posuere tellus hendrerit mollis. Nulla sed lacus nec mauris sodales viverra.
		Donec ligula arcu, viverra a bibendum eu, dignissim in felis. Sed consectetur erat mollis risus blandit quis ornare nisl scelerisque. Vivamus sed risus a nulla dictum euismod id et dolor. Nam id pharetra nunc. Nunc ullamcorper varius leo, nec fermentum lacus sodales vel. Duis scelerisque dapibus mi, vel eleifend eros bibendum sit amet. Cras tristique justo id justo bibendum a elementum tortor volutpat. Maecenas ligula nibh, consectetur id malesuada sit amet, suscipit non risus. Proin faucibus pellentesque vehicula. Praesent iaculis malesuada erat. Fusce ac elit nec lorem sodales hendrerit.
		Phasellus diam sapien, cursus nec mattis tempor, facilisis ut odio. Maecenas felis eros, rhoncus eget dignissim quis, vulputate ut orci. Fusce posuere fringilla odio ut cursus. Suspendisse a adipiscing justo. Donec posuere varius mollis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tempor elit eget quam euismod hendrerit feugiat a augue. Vivamus molestie consectetur urna sed condimentum. Fusce luctus consequat laoreet. Nulla facilisi. Suspendisse gravida laoreet odio, non bibendum magna facilisis et. Suspendisse at egestas metus. Nullam condimentum malesuada ultrices.
		Donec posuere hendrerit erat, non commodo lacus varius non. Sed sodales viverra sagittis. Duis congue scelerisque nunc, ut fermentum tellus adipiscing sit amet. Morbi ut eros neque. Aliquam semper, mauris ac cursus cursus, tortor sem pulvinar magna, non tristique purus mauris nec nisl. Sed eget adipiscing magna. Aliquam ullamcorper sollicitudin dolor, vitae mollis eros mattis quis. Cras gravida tristique nibh id fermentum. Sed accumsan vehicula metus, non imperdiet eros auctor sit amet. In facilisis justo et sem cursus dictum. Fusce consectetur, est nec suscipit vulputate, nisi urna sodales ante, id viverra urna ligula nec odio. Donec eu neque nulla, sed sodales augue.
		Duis eget magna elit. Vestibulum dolor lorem, fermentum ac condimentum sit amet, malesuada eget elit. Quisque justo odio, consequat ut blandit id, ullamcorper quis massa. Aliquam lectus augue, commodo eu pharetra vitae, luctus nec est. In accumsan consectetur commodo. Vivamus nec massa lacus, sed lobortis erat. Quisque non pharetra leo. In et arcu odio. Sed fringilla elementum mauris, lacinia adipiscing est accumsan a. Aliquam erat volutpat. Ut nisi massa, ultrices eu congue ut, consectetur sed mauris. Integer arcu nunc, mattis mollis imperdiet tincidunt, ultrices eget neque. Curabitur rhoncus viverra ipsum, ac iaculis dolor rutrum at. Cras ac pharetra arcu. Nulla felis justo, venenatis ut molestie id, ultricies vel ante. Nam non lacus libero.
		Nulla posuere molestie tincidunt. Nulla nec tristique justo. Pellentesque nec condimentum eros. Nulla nec turpis id urna fermentum porttitor ut ut velit. In placerat odio porta augue facilisis ut sagittis ipsum volutpat. Morbi urna quam, fringilla eu facilisis eu, aliquet rutrum ipsum. Mauris feugiat justo id tellus rhoncus sit amet mattis lacus imperdiet. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. In at nunc quis nisl interdum feugiat vel a lectus. Proin sed arcu at lectus dictum mattis vel vel mauris. Suspendisse sollicitudin rhoncus tempor. Praesent massa nunc, consectetur sit amet pellentesque vitae, faucibus quis urna. In ut metus non orci consectetur aliquam. Nullam congue, mi et egestas vulputate, nibh leo ullamcorper dui, eget fermentum diam nisl id nulla. Donec dapibus dapibus justo, in pretium magna interdum et. In vitae mi non tortor gravida pulvinar at ac arcu. In hac habitasse platea dictumst. Proin pretium, tortor placerat suscipit auctor, lacus mi vestibulum lectus, vel accumsan arcu diam nec lectus. Aenean euismod fringilla purus vel tincidunt.
		Donec dignissim posuere mollis. Pellentesque convallis ipsum et nibh facilisis interdum. Nullam velit mauris, mattis et eleifend a, molestie tempor elit. Cras hendrerit, arcu at faucibus bibendum, ante diam pulvinar sapien, non viverra purus leo sed risus. Aliquam tempor rutrum augue, in ultrices lorem ultrices quis. Donec auctor laoreet cursus. Integer non elit lorem, nec pulvinar justo. Cras sagittis eleifend semper. Cras at lobortis tortor. Nam quis mi eget purus semper lobortis posuere vel magna. Sed porta, felis ac auctor fringilla, urna magna iaculis justo, at ullamcorper libero lectus vel tortor. Praesent at nunc tortor, vel fringilla lorem. Etiam quis rhoncus magna. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Proin ac libero tortor.
		Aenean ut orci at orci rhoncus aliquet. Proin feugiat, diam sed sodales aliquam, diam sem tincidunt urna, non viverra massa orci quis urna. Quisque tincidunt felis ut elit pretium ac posuere mi cursus. Vivamus quis dapibus ligula. Suspendisse potenti. Praesent ac diam ac nisl congue posuere. Nam sit amet risus faucibus orci vulputate porta et suscipit magna. Vivamus at quam quis lectus vehicula commodo eu vitae leo. Nunc dolor purus, ornare sed congue ac, feugiat et purus. In mi lorem, ultrices non varius sed, dapibus posuere eros. Sed faucibus venenatis risus vel elementum.
		Duis eget ornare mi. Phasellus iaculis nulla eget lacus vehicula venenatis. Pellentesque non tellus quis lorem congue pellentesque. Suspendisse vestibulum, nulla sed hendrerit tincidunt, quam nunc cursus libero, a feugiat arcu enim at odio. Ut vestibulum imperdiet tellus id imperdiet. Aliquam et dolor libero, a tempor erat. Cras sagittis venenatis interdum. Mauris nec consequat diam. Etiam condimentum, odio at fermentum elementum, risus elit malesuada magna, et fringilla massa ante et tellus. Cras ut leo quis mauris imperdiet fringilla in et augue. Vivamus vestibulum metus sed enim faucibus id pharetra sem ornare. Suspendisse eget justo nibh, eu auctor mi. Aliquam accumsan egestas mollis.
		Sed semper hendrerit enim vel pellentesque. Praesent vehicula turpis at ipsum faucibus non feugiat libero volutpat. Etiam sed dolor eu arcu porttitor lobortis nec non magna. Morbi sit amet viverra orci. Mauris sagittis erat sed diam ullamcorper facilisis. Donec purus neque, vestibulum ut ullamcorper eget, placerat in est. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus id diam turpis. Sed vestibulum, felis sed venenatis tempus, libero enim molestie ante, vel luctus nibh nisl a tortor. Mauris fermentum, quam eget rutrum sodales, tortor velit fringilla leo, id cursus purus nisi sed turpis. Nulla nibh mauris, pulvinar placerat ornare id, dapibus non ante. Mauris pretium viverra quam, eu tristique nisl sodales non. Nam sit amet dolor eros. Nulla facilisi.
		Nulla facilisi. Ut ultrices hendrerit consequat. Nam ligula orci, scelerisque varius tempor vel, convallis et nunc. Proin ullamcorper tempor posuere. Aenean et mi a sapien hendrerit mollis vel ornare ante. Suspendisse porta, velit sit amet dignissim placerat, ipsum lectus semper ligula, in bibendum felis urna a tortor. Suspendisse potenti. Fusce pretium, nunc quis varius viverra, sapien sem eleifend purus, sed tempus tortor sapien ut nisl. Suspendisse posuere venenatis risus vitae facilisis. Vestibulum consectetur metus lacus. Sed aliquam augue nisl. Suspendisse non purus in erat sodales dictum. Sed condimentum pellentesque gravida. Quisque vulputate, mi quis fringilla auctor, leo tellus porttitor eros, sed commodo enim metus vel mi. Phasellus in nulla lacinia lorem aliquam pretium in et justo. Nulla ac venenatis nisi. Praesent interdum pretium velit, et pulvinar ante consectetur quis. Morbi ut elit id orci tempor semper. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
		Nam porta accumsan tempus. Duis tellus sapien, commodo ut dapibus commodo, ornare id dui. Mauris at arcu neque, nec pretium nunc. Suspendisse nec nulla et erat malesuada varius. Pellentesque varius nisi ac metus egestas vitae ultricies mi porttitor. Praesent luctus adipiscing nunc, eu ornare metus gravida eget. Sed vel justo lorem, vitae tincidunt eros. Aliquam eleifend felis ac libero lobortis nec suscipit orci facilisis. Quisque convallis, velit non sodales hendrerit, risus odio sollicitudin nisl, sed porttitor mi dolor non turpis. Sed ac est quis felis lobortis porttitor. Nulla volutpat ipsum sodales magna commodo ut commodo metus convallis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.
		Curabitur vestibulum sapien ac erat volutpat ultrices. In dignissim luctus leo sit amet mollis. Integer eget sagittis nunc. Cras felis turpis, pretium aliquet fringilla in, dapibus ut justo. Mauris sit amet pharetra leo. Nulla lectus elit, laoreet nec scelerisque eu, bibendum eget diam. Nunc vehicula blandit sem vel ultricies. Praesent sollicitudin eleifend imperdiet. Sed eget lectus vel sapien varius facilisis. Cras felis nisl, vehicula vitae feugiat nec, tincidunt a lacus. Aliquam enim neque, scelerisque et euismod non, ornare ut ipsum. Donec lectus lorem, sodales ac porta id, condimentum a metus. Nullam et lobortis augue. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum mollis tortor non diam sodales tincidunt. Mauris vestibulum lorem a lectus lobortis commodo. Sed tempor, libero ac dictum posuere, leo massa hendrerit libero, at sodales eros enim in diam. Praesent tincidunt ligula eget augue ornare sit amet vehicula tellus tristique. Etiam vel pretium felis.
		Cras aliquam auctor auctor. Duis dictum sapien non urna posuere feugiat. Aliquam rutrum sem non metus auctor placerat. Nulla laoreet, erat eu sodales imperdiet, nisl arcu condimentum augue, sed dictum nisl tortor sit amet elit. Suspendisse ullamcorper magna ac dolor convallis sed aliquet quam commodo. Pellentesque eget magna tortor, non rhoncus est. Suspendisse malesuada vestibulum commodo. Maecenas venenatis, lacus sed venenatis convallis, lectus dolor gravida libero, porttitor ultrices urna purus ut lectus. Praesent mollis vulputate nibh, nec interdum tortor elementum id. Aenean lacinia accumsan purus, nec sodales enim tempus eget. Pellentesque aliquam tempor nisl, at volutpat orci dignissim in. Fusce sit amet sapien nec justo commodo auctor id sed augue. Aliquam ultricies consectetur lorem, eu accumsan dui facilisis at. Sed tristique porttitor nunc, at auctor diam gravida sit amet. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed eget nibh odio. Nullam et ipsum eu tortor dictum viverra. Sed et mauris ante, nec commodo quam. Proin purus mi, tristique eu lacinia quis, tincidunt sit amet dolor.
		Quisque congue fermentum sem, et ultricies lorem pharetra at. Pellentesque tincidunt placerat odio tempus semper. Mauris pretium tempor diam, eget fermentum elit aliquet at. Aenean pulvinar lorem eget arcu ultrices sodales. Maecenas elementum, enim ut aliquet tincidunt, neque diam convallis felis, eu tempus justo leo a nunc. Phasellus iaculis lobortis ullamcorper. Aenean posuere faucibus porttitor. Pellentesque dapibus dictum ornare. Suspendisse quis varius ipsum. Etiam porta, ante vitae sodales elementum, dui urna dapibus tellus, vel accumsan lacus odio et lorem. Aliquam elementum accumsan purus vitae elementum. Aenean non bibendum lacus. Nunc hendrerit blandit posuere. Curabitur sed tortor et orci facilisis ullamcorper. Suspendisse et ipsum sem, ac porttitor nisl. Phasellus tempor egestas tellus, vitae dictum lorem pellentesque ac. Donec ut dictum magna. Mauris fringilla sapien a elit pulvinar et aliquam diam aliquam. Suspendisse congue imperdiet risus non hendrerit. Vestibulum tristique quam eget ipsum gravida ultricies.
		Aliquam dui tortor, elementum ut tristique vel, euismod at libero. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Aliquam est metus, euismod in condimentum eu, porttitor et nisl. Aliquam eu vestibulum massa. Ut ac aliquam mauris. Donec ultrices bibendum nunc sit amet faucibus. Sed erat lacus, rhoncus at pharetra quis, semper eget nunc. Praesent luctus ligula in urna convallis viverra. Sed et faucibus elit. Aenean eleifend, dolor vel ultricies egestas, turpis tortor pharetra purus, non malesuada dolor lectus et quam. Proin et est ligula. Suspendisse faucibus placerat tincidunt. Nulla condimentum dictum magna. Nullam dignissim, dui at vulputate vulputate, urna libero porta mauris, pharetra viverra mi odio eget enim. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per.
	"""
	
	words = lipsum.split()
	max_start = len(words) - count
	start = random.randrange(0, max_start)
	
	output = ' '.join(words[start:start+count]).capitalize()
	
	if slugify:
		return slugify(output)
	else:
		return output

def get_paragraph():
	return lipsum(count=random.randrange(random.randrange(10, 30), random.randrange(80, 180)))

# Slugify
import re

_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')
def slugify(value):
	import unicodedata
	if not isinstance(value, unicode):
		value = unicode(value)
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = unicode(_slugify_strip_re.sub('', value).strip().lower())
	return _slugify_hyphenate_re.sub('-', value)

# Run the dummy composer
dummy()
