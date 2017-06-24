import pytvmaze
import datetime
tvm = pytvmaze.TVMaze('mtjhartley')
# '''
# show = tvm.get_show(show_name='dexter')

# print show
# print "this is everything a show has"
# print type(show)
# print dir(show)

# # print show.cast
# # print show.episodes
# # print show.genres

# # print show.id
# print type(show.image)
# print show.image 
# print show.image['original']
# # print show.language

# # print show.links
# print 'printing id and type '
# print show.maze_id #int
# print type(show.maze_id)
# print "print show summary"
# print show.summary


# # print show.name
# # print show.network

# print "show premiered and type"
# print show.premiered
# print type(show.premiered)
# new_date = datetime.datetime.strptime(show.premiered, '%Y-%m-%d').date()
# print new_date
# print type(new_date)
# '''

# # print show.rating 
# # print show.runtime 
# # print show.seasons 
# # print show.status 

# show = tvm.get_show(maze_id=161, embed='episodes')# to get seasons
# for season in show:
#     for episode in season:
#         print dir(episode)
#         print "*" * 50
#         print episode.airdate
#         print episode.episode_number 
#         print episode.airtime 
#         print episode.image
#         print episode.maze_id
#         print episode.runtime 
#         print episode.season_number 
#         print episode.summary 
#         print episode.title 
#         print episode.special
#         print episode.writer
#         print episode.director
#         print "*" * 50


        

# # for episode in show[2]:
# #     print (episode.title)

# # print show.summary
# # print show.type 
# # print show.updated 
# # print show.url 
# # print show.web_channel

# #search by title! 
# shows = pytvmaze.get_show_list('lost')
# for show in shows:
#     print show
#     print show.maze_id


show = tvm.get_show(maze_id=161, embed='episodes')# to get seasons

for episode in show.episodes:
    print episode.title