from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import pytvmaze
import datetime
from ..login_registration.models import User
tvm = pytvmaze.TVMaze('mtjhartley')

# Create your models here.

class ShowManager(models.Manager):
    def createShow(self, maze_id):
        showMap = {}
        show = tvm.get_show(maze_id=maze_id, embed='episodes')
        showMap['title'] = show.name
        showMap['maze_id'] = show.maze_id
        if show.summary:
            showMap['description'] = show.summary
        else:
            showMap['description'] = "No description available."
        showMap['status'] = show.status
        showMap['premiered'] = datetime.datetime.strptime(show.premiered, '%Y-%m-%d').date()
        try:
            showMap['network'] = show.network.name
        except AttributeError:
            showMap['network'] = ""
        try:
            showMap['image_link'] = show.image['original']
            new_show = Show.objects.create(title = showMap['title'], description=showMap['description'], status=showMap['status'], premiered=showMap['premiered'], network=showMap['network'], image_link=showMap['image_link'], maze_id=showMap['maze_id'])
        except:
            new_show = Show.objects.create(title = showMap['title'], description=showMap['description'], status=showMap['status'], premiered=showMap['premiered'], network=showMap['network'], maze_id=showMap['maze_id'])
        
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
    favorite = models.ManyToManyField(User, related_name='users_favorites')
    #let's add a many to many field here for FAVORITES 1 user many favorite shows, 1 show can be favorited bym any users. 
    #this will be distinct from currently watching/watched, while will require it's own separate table.
    

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
        #check if airdate is given
        episodeMap['airdate'] = datetime.datetime.strptime(episode.airdate, '%Y-%m-%d').date()
        episodeMap['maze_id'] = episode.maze_id
        episodeMap['episode_number'] = episode.episode_number
        episodeMap['season_number'] = episode.season_number
        if episode.image:
            episodeMap['image_link'] = episode.image['original']
            new_episode = Episode.objects.create(title=episodeMap['title'], show=episodeMap['show'], summary=episodeMap['summary'], runtime=episodeMap['runtime'], airdate=episodeMap['airdate'], image_link=episodeMap['image_link'],maze_id=episodeMap['maze_id'], episode_number=episodeMap['episode_number'], season_number=episodeMap['season_number'])
        else:
            new_episode = Episode.objects.create(title=episodeMap['title'], show=episodeMap['show'], summary=episodeMap['summary'], runtime=episodeMap['runtime'], airdate=episodeMap['airdate'],maze_id=episode['maze_id'], episode_number=episodeMap['episode_number'], season_number=episodeMap['season_number'])

        

class Episode(models.Model):
    title = models.CharField(max_length=255)
    show = models.ForeignKey(Show, related_name='episodes')
    summary = models.TextField()
    runtime = models.IntegerField()
    airdate = models.DateField()
    maze_id = models.IntegerField()
    episode_number = models.IntegerField() 
    season_number = models.IntegerField()
    image_link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #favorites should be many to many. 1 user can fav many episodes, 1 ep can be faved by many users!
    watched = models.ManyToManyField(User, related_name='watched_episodes')
    #watched could also be many to many, ez on or off switch for this one.


    objects = EpisodeManager()

#let's do reviews for Shows, and comments/ratings for episodes? sounds good. 


class ShowRating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    show = models.ForeignKey(Show, related_name='show_ratings')
    user = models.ForeignKey(User, related_name='user_show_ratings')
# class ReviewManager(models.Manager):
#     def isValidReview(self)
    
class Review(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    show = models.ForeignKey(Show, related_name="reviews")
    user = models.ForeignKey(User, related_name='reviews')
    rating = models.ForeignKey(ShowRating, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # objects = ReviewManager()
#Show Comments are what users leave on episode pages

class RecentlyViewedShow(models.Model):
    user = models.ForeignKey(User, related_name="recently_viewed_user")
    show = models.ForeignKey(Show, related_name="recently_viewed_show")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EpisodeCommentManager(models.Manager):
    def isValidComment(self, commentInfo, episode_id, user):
        episode = Episode.objects.get(id=episode_id)
        validComment = True
        commentObject = {
            'errors': [],
        }
        if len(commentInfo['comment']) < 10:
            commentObject['errors'].append("Comment must be at least 10 characters.")
            validComment = False
        if validComment:
            new_comment = EpisodeComment.objects.create(comment=commentInfo['comment'], episode=episode, user=user)
            commentObject['new_comment'] = new_comment
        return commentObject
        
class EpisodeComment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    episode = models.ForeignKey(Episode, related_name='episode_comments')
    user = models.ForeignKey(User, related_name='users_episode_comments')

    objects = EpisodeCommentManager()

class EpisodeRating(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    episode = models.ForeignKey(Episode, related_name='episode_ratings')
    user = models.ForeignKey(User, related_name='user_episode_ratings')

