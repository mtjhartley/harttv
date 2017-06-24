import guidebox
guidebox.api_key = "f72defc7a26302c4e2ea5e33d937e0781913c4bd"

def createShowMap(guidebox_show_id):
    showMap = {}
    show = guidebox.Show.retrieve(id=guidebox_show_id)
    showMap['name'] = show["title"]
    showMap['overview'] = show["overview"]
    showMap['fanart'] = show["fanart"]
    showMap['banner'] = show["banner"]
    showMap['guidebox_id'] = show["id"]
    showMap['first_aired'] = show["first_aired"]
    showMap['status'] = show["status"]

    return showMap

print createShowMap(1586)


