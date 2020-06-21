from django.http import HttpResponse
from django.shortcuts import render
import redis

# Create your views here.
r = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

def index(request):
    movieKeys = r.keys("movie:*")
    movies = []
    for key in movieKeys:
        movies.append(key[6:] + ': ' + r.get(key))
    return render(request, 'movies/index.html', {'movies': movies})

def loadmovies(request):
    file = open('movies.txt')
    movies = file.readlines()
    counter = 0
    for movie in movies:
        movieSplit = movie.split(' : ')
        title = movieSplit[0]
        actors = movieSplit[1]
        r.set('movie:' + title, actors)
        counter += 1
    return HttpResponse('Movies succesfully loaded into redis')

def search(request):
    if(request.method == "POST"):
        redisKeys = r.keys('movie:' + request.POST['search'] + "*")
        movies = []
        for movie in redisKeys:
            movies.append(r.get(movie))
        return render(request, 'movies/index.html', {'movies': movies})
    return render(request, 'movies/search.html')