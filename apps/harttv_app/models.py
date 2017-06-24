from __future__ import unicode_literals

from django.db import models
import pytvmaze
import datetime
tvm = pytvmaze.TVMaze('mtjhartley')

# Create your models here.

class ShowManager(models.Manager):
    def createShow(self, maze_id):
        showMap = {}
        show = tvm.get_show(maze_id=maze_id, embed='episodes')
        showMap['title'] = show.name
        showMap['description'] = show.summary
        showMap['status'] = show.status
        showMap['premiered'] = datetime.datetime.strptime(show.premiered, '%Y-%m-%d').date()
        showMap['network'] = show.network.name
        showMap['image_link'] = show.image['original']
        showMap['maze_id'] = show.maze_id

        new_show = Show.objects.create(title = showMap['title'], description=showMap['description'], status=showMap['status'], premiered=showMap['premiered'], network=showMap['network'], image_link=showMap['image_link'], maze_id=showMap['maze_id'])
        return new_show



        
        #show info will be passed in as a variable, which is it's own class. navigate through the class
        #create this show map, and then use this map to clearly update the database!



    
class Show(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=255)
    premiered = models.DateField()
    network = models.CharField(max_length=255)
    image_link = models.CharField(max_length=255)
    maze_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ShowManager()

class EpisodeManager(models.Manager):
    def createEpisode(self, show_id, episode):
        episodeMap = {}
        print "*" * 50
        print episode
        print episode.title 
        print show_id
        print "*" * 50
        episodeMap['title'] = episode.title
        episodeMap['show'] = Show.objects.get(id=show_id)
        episodeMap['summary'] = episode.summary 
        episodeMap['runtime'] = episode.runtime
        episodeMap['airdate'] = datetime.datetime.strptime(episode.airdate, '%Y-%m-%d').date()
        episodeMap['maze_id'] = episode.maze_id
        if episode.image:
            episodeMap['image_link'] = episode.image['original']
            new_episode = Episode.objects.create(title=episodeMap['title'], show=episodeMap['show'], summary=episodeMap['summary'], runtime=episodeMap['runtime'], airdate=episodeMap['airdate'], image_link=episodeMap['image_link'],maze_id=episodeMap['maze_id'])
        else:
            new_episode = Episode.objects.create(title=episodeMap['title'], show=episodeMap['show'], summary=episodeMap['summary'], runtime=episodeMap['runtime'], airdate=episodeMap['airdate'],maze_id=episode['maze_id'])

        

class Episode(models.Model):
    title = models.CharField(max_length=255)
    show = models.ForeignKey(Show, related_name='episodes')
    summary = models.TextField()
    runtime = models.IntegerField()
    airdate = models.DateField()
    maze_id = models.IntegerField()
    image_link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EpisodeManager()
