from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Show, Episode
import threading
import pytvmaze
from django.urls import reverse
tvm = pytvmaze.TVMaze('mtjhartley')
# Create your views here.
def harttv_index(request):
    context = {}
    return render(request, 'harttv_app/index.html', context)

def view_show(request, show_maze_id):
    if len(Show.objects.filter(maze_id=show_maze_id)) == 1:
        show = Show.objects.get(maze_id=show_maze_id)
    else: #show is NOT in the database
        show = Show.objects.createShow(maze_id=show_maze_id)
        #threading code to add episodes to db if first time visiting page
        iterate_show = tvm.get_show(maze_id=show.maze_id, embed='episodes')
        print iterate_show.name
        print iterate_show.summary
        for episode in iterate_show.episodes:
            print "threading"
            thread = threading.Thread(target=Episode.objects.createEpisode, args=(show.id, episode))
            thread.start()
            print "threading complete"
    print "*" * 50
    print "testing seasons and episodes"
    context = {
        "show": show
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
    search_string = request.GET['show_search'].strip().lower() #check if tvmaze is case sensitive
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
        showDict['description'] = show.summary
        if show.image:
            showDict['image'] = show.image['original']
        show_list.append(showDict)


    context = {
        #"searchShows": searchShows,
        "contextShow": show_list,
    }

    return render (request, 'harttv_app/search_results.html', context)
    

def delete_all_shows(request):
    Show.objects.all().delete()
    Episode.objects.all().delete()
    return redirect(reverse('harttv_index'))