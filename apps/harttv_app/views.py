from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Show, Episode, Review, EpisodeComment, EpisodeRating, ShowRating
import datetime
import pytvmaze
import threading
import random

from ..login_registration.models import User
tvm = pytvmaze.TVMaze('mtjhartley')
# Create your views here.

def generate_rating_options():
    ratings = [1,2,3,4,5,6,7,8,9,10]
    ratings_strings = ["(1) Appalling", "(2) Atrocious", "(3) Very Bad", "(4) No Good", "(5) Alright", "(6) Good", "(7) Enjoyable", "(8) Great", "(9) Amazing", "(10) Swag Me Out!"]
    rating_options = zip(ratings, ratings_strings)
    return rating_options


def index(request):
    random_idx = random.randint(0, Show.objects.count() - 1)
    random_show = Show.objects.all()[random_idx]
    # show_average_rating = ShowRating.objects.aggregate(Avg('rating')).order_by('-rating').distinct('show')
    top_ranked_shows = ShowRating.objects.values_list('show__title', 'show__maze_id', 'show__image_link').annotate(average_rank=Avg('rating')).order_by('-average_rank')[:4]
    print top_ranked_shows[0]
    print top_ranked_shows[0][0]
    print top_ranked_shows[0][1]
    print top_ranked_shows[0][2]
    print top_ranked_shows

    # all_shows_average_rating = Show.objects.values_list('title').annotate(Avg('show_ratings'))
    # print all_shows_average_rating
    context = {
        "show": random_show,
        "top_rated": top_ranked_shows,

    }
    return render(request, 'harttv_app/index.html', context)

def view_all_shows(request):
    context = {
        "shows": Show.objects.all().order_by('title')
    }
    return render(request, 'harttv_app/all_shows.html', context)


def view_show(request, show_maze_id):
    user = User.objects.get(id=request.session['id'])
    if len(Show.objects.filter(maze_id=show_maze_id)) == 1:
        show = Show.objects.get(maze_id=show_maze_id)
        print "show is already in the database"
    else: #show is NOT in the database
        show = Show.objects.createShow(maze_id=show_maze_id)
        print "show is not in the database"
        #threading code to add episodes to db if first time visiting page
        iterate_show = tvm.get_show(maze_id=show.maze_id, embed='episodes')
        print iterate_show.name
        print iterate_show.summary
        for episode in iterate_show.episodes:
            print "threading"
            thread = threading.Thread(target=Episode.objects.createEpisode, args=(show.id, episode))
            thread.start()
            thread.join()
            print "threading complete"
        #thread.wait loop
    print "*" * 50
    print "testing seasons and episodes"
    print User.get_rating(user, show.id)

    #if show is in users favorites, context favorited : True
    #else context favorited: False
    print show.favorite.filter(id=user.id)

    #refactor toShowReview nad ShowRating
    if len(ShowRating.objects.filter(show=show, user=user)) > 0:
        rating = ShowRating.objects.get(show=show, user=user).rating
    else:
        rating = None
    
    favorited = len(show.favorite.filter(id=user.id)) > 0 
    #return true or false if favorited
    print favorited
    show_average_rating = ShowRating.objects.filter(show=show).aggregate(Avg('rating'))
    show_num_users_rated = len(ShowRating.objects.filter(show=show))
    print 'printing average_rating'
    print show_average_rating
    print 
    print "how many users have favorited this show: "
    print show.favorite.all().count()
    ratings_options = generate_rating_options()
    episodes = Episode.objects.filter(show__maze_id=show.maze_id).annotate(number_eps=Count('show__episodes')).order_by('season_number', 'episode_number')
    context = {
        "show": show,
        "episodes": episodes,
        "recent_episodes": episodes[:6],
        "num_episodes": len(episodes), #can probably do with...Episode.objects.filter(show__episodes.)
        "favorited": favorited,
        "options": ratings_options,
        "current_rating": rating,
        "show_average_rating": show_average_rating['rating__avg'],
        "show_num_users_rated": show_num_users_rated,
        "favorites": show.favorite.all().count(),
    }
    

    # code to add episodes to the database if the show doesn't exist. 
    # iterate_show = tvm.get_show(maze_id=show.maze_id, embed='episodes')
    # print iterate_show.name
    # print iterate_show.summary
    # for episode in iterate_show.episodes:
    #     print "threading"
    #     thread = threading.Thread(target=Episode.objects.createEpisode, args=(show.id, episode))
    #     thread.start()
    #     print "threading complete"

    
    return render(request, 'harttv_app/view_show.html', context)


def test_search_bar(request):
    return render(request, 'harttv_app/search.html')        

def search_results(request):
    search = request.GET['show_search']
    search_string = search.strip().lower() #check if tvmaze is case sensitive
    print "*" * 50
    print search_string
    searchShows = pytvmaze.get_show_list(search_string)
    print "shows"
    print searchShows
    print "type(shows)"
    print type(searchShows)
    print type(searchShows[0])
    print "name and id"
    print "name", searchShows[0].name
    print "id", searchShows[0].maze_id
    print "for loop"
    show_list = []
    #for some reason, can't just pass in the searchShows to context...
    for show in searchShows:
        showDict = {}
        showDict['name'] = show.name
        showDict['maze_id'] = show.maze_id
        if show.summary:
            summary_array = show.summary.split(" ")
            showDict['description'] = ' '.join([x for x in summary_array[:100]]) + '...'
        if show.premiered:
            print show.premiered
            showDict['airdate'] = datetime.datetime.strptime(show.premiered, '%Y-%m-%d').date()
        else:
            showDict['airdate'] = 'N/A'
        if show.network:
            showDict['network'] = show.network.name
        else:
            showDict['network'] = 'N/A'
        if show.image:
            showDict['image'] = show.image['original']
        show_list.append(showDict)


    context = {
        #"searchShows": searchShows,
        "contextShow": show_list,
        "search": search,
    }

    return render (request, 'harttv_app/search_results.html', context)

# def handle_update_show_rating(request, show_id):
#     user = User.objects.get(id=request.session['id'])
#     show = Show.objects.get(id=show_id)
#     existing_rating = ShowRating.objects.filter(user=user, show=show)
#     if existing_rating:
#         existing_rating[0].rating = int(request.POST['rating'])
#         existing_rating[0].save()
#     else:
#         ShowRating.objects.create(user=user, show=show, rating=int(request.POST['rating']))
#     url = reverse('harttv:view_show', kwargs={'show_maze_id': show.maze_id})
#     return HttpResponseRedirect(url)

#refactor to review.model manager later. 
def handle_add_review(request, show_id):
    if request.method == 'POST':
        show = Show.objects.get(id=show_id)
        user = User.objects.get(id=request.session['id'])
        print show
        print user
        review_title = request.POST['title']
        review_text = request.POST['review']  
        existing_rating = ShowRating.objects.filter(user=user, show=show)
        if len(review_title) == 0 and len(review_text) == 0:
            if existing_rating:
                existing_rating[0].rating = int(request.POST['rating'])
                existing_rating[0].save()
                rating = existing_rating[0]
            else:
                rating = ShowRating.objects.create(user=user, show=show, rating=int(request.POST['rating']))
            url = reverse('harttv:view_show', kwargs={'show_maze_id': show.maze_id})
            return HttpResponseRedirect(url)
        else:
            if existing_rating:
                existing_rating[0].rating = int(request.POST['rating'])
                existing_rating[0].save()
                rating = existing_rating[0]
            else:
                rating = ShowRating.objects.create(user=user, show=show, rating=int(request.POST['rating']))
            Review.objects.create(title=review_title, text=review_text,user=user, show=show, rating=rating)
            url = reverse('harttv:view_show', kwargs={'show_maze_id': show.maze_id})
            return HttpResponseRedirect(url)

            
            
            




def handle_add_favorite(request, show_id):
    if request.method == 'POST':
        show = Show.objects.get(id=show_id)
        user = User.objects.get(id=request.session['id'])

        user.users_favorites.add(show) #matches related name
        print "printing show.favorite.all()"
        print show.favorite.all()

        url = reverse('harttv:view_show', kwargs={'show_maze_id': show.maze_id})
        #redirect to users page, maybe their favorites page!
        return HttpResponseRedirect(url)

def handle_remove_favorite(request, show_id):
    if request.method == 'POST':
        show = Show.objects.get(id=show_id)
        user = User.objects.get(id=request.session['id'])

        user.users_favorites.remove(show)
        url = reverse('harttv:view_show', kwargs={'show_maze_id': show.maze_id})
        return HttpResponseRedirect(url)

def view_episode(request, episode_id):
    user = User.objects.get(id=request.session['id'])
    episode = Episode.objects.get(id=episode_id)
    show = Show.objects.get(id=episode.show.id)
    comments = EpisodeComment.objects.filter(episode=episode)
    ratings_options = generate_rating_options()
    if len(EpisodeRating.objects.filter(episode=episode, user=user)) > 0:
        episode_rating = EpisodeRating.objects.get(episode=episode, user=user).rating
    else:
        episode_rating = None
    if len(ShowRating.objects.filter(show=show, user=user)) > 0:
        show_rating = ShowRating.objects.get(show=show, user=user).rating
    else:
        show_rating = None
    print "*" * 50
    print show_rating
    episodes = Episode.objects.filter(show__maze_id=show.maze_id).annotate(number_eps=Count('show__episodes')).order_by('season_number', 'episode_number')
    print comments
    favorited = len(show.favorite.filter(id=user.id)) > 0 
    show_average_rating = ShowRating.objects.filter(show=show).aggregate(Avg('rating'))
    show_num_users_rated = len(ShowRating.objects.filter(show=show))
    episode_average_rating = EpisodeRating.objects.filter(episode=episode).aggregate(Avg('rating'))
    episode_num_users_rated = len(EpisodeRating.objects.filter(episode=episode))
    print 'printing average_rating'
    print show_average_rating
    print 
    print "how many users have favorited this show: "
    print show.favorite.all().count()
    context = {
        "show": show,
        "episode": episode,
        "num_episodes": len(episodes),    
        "comments": comments,
        "episode_rating" : episode_rating,
        "current_rating" : show_rating,
        "options": ratings_options,
        "favorited": favorited,
        "show_average_rating": show_average_rating['rating__avg'],
        "show_num_users_rated": show_num_users_rated,
        "favorites": show.favorite.all().count(),
        "episode_average_rating": episode_average_rating['rating__avg'],
        "episode_num_users_rated": episode_num_users_rated,

    }
    return render(request, 'harttv_app/view_episode.html', context)

def handle_add_episode_comment(request, episode_id):
    print "*" * 50
    print request.method
    user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        print "post is happening"
        print "request.POST"
        print request.POST
        episodeCommentObject = EpisodeComment.objects.isValidComment(request.POST, episode_id, user)
        if 'new_comment' in episodeCommentObject:
            url = reverse('harttv:view_episode', kwargs={'episode_id': episode_id})
            return HttpResponseRedirect(url)
        else:
            for error in episodeCommentObject['errors']:
                messages.warning(request, error)
            url = reverse('harttv:view_episode', kwargs={'episode_id': episode_id})
            return HttpResponseRedirect(url)
    else:
        return redirect(reverse('harttv:index'))

def handle_delete_episode_comment(request, episode_id, comment_id):
    if request.method == 'POST':
        episode = Episode.objects.get(id=episode_id)
        user = User.objects.get(id=request.session['id'])
        EpisodeComment.objects.filter(episode=episode, user=user, id=comment_id).delete()

        url = reverse('harttv:view_episode', kwargs={'episode_id': episode_id})
        return HttpResponseRedirect(url)
    

        
def handle_update_episode_rating(request, episode_id):
    user = User.objects.get(id=request.session['id'])
    episode = Episode.objects.get(id=episode_id)
    existing_rating = EpisodeRating.objects.filter(user=user, episode=episode)
    if existing_rating:
        existing_rating[0].rating = int(request.POST['rating'])
        existing_rating[0].save()
    else:
        EpisodeRating.objects.create(user=user, episode=episode, rating=int(request.POST['rating']))
    url = reverse('harttv:view_episode', kwargs={'episode_id': episode_id})
    return HttpResponseRedirect(url)
    


def about(request):
    return render(request, 'harttv_app/about.html')

def delete_all_shows(request):
    Show.objects.all().delete()
    Episode.objects.all().delete()
    return redirect(reverse('harttv:index'))