from django.shortcuts import render, redirect
from mtunes.models import Song, Watchlater, History
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import UploadSongForm

def loginuser(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, 'mtunes/login.html')

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        try:
            User.objects.get(username=username)
            messages.error(request,"User with this username already exists.")
        except:
            if pass1 == pass2:
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name = first_name
                myuser.last_name = last_name
                myuser.save()
                return redirect('login')
            else:
                messages.error(request, "Password didn't match")
        
    return render(request, 'mtunes/signup.html')

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect("index")

def index(request):
    song = Song.objects.all()
    if request.user.is_authenticated:
        myplaylist = Watchlater.objects.filter(user=request.user)
    else:
        myplaylist = None
    context = {
        'song': song,
        'myplaylist': myplaylist
    }
    return render(request, 'index.html', context)

def songs(request):
    song = Song.objects.all()
    return render(request, 'mtunes/songs.html', {'song': song})

@login_required(login_url='login')
def uploadsong(request):
    if request.method=="POST":
        name = request.POST.get("name")
        singer = request.POST.get("singer")
        tag = request.POST.get("tag")
        image = request.FILES["image"]
        song = request.FILES["song"]
        movie = request.POST.get("movie")

        Song.objects.create(
            name=name,
            singer=singer,
            tags=tag,
            movie=movie,
            image=image,
            song=song,
            uploaded_by=request.user
        )
        return redirect('mysongs')

    return render(request, 'mtunes/uploadsong.html')

@login_required(login_url='login')
def deletesong(request, song_id):
    song = Song.objects.get(song_id=song_id)
    if song.uploaded_by == request.user:
        song.delete()
    else:
        messages.error(request, "You don't own this song so you cannot delete it.")
    return redirect('mysongs')

def songpost(request, id):
    song = Song.objects.filter(song_id = id).first()
    songs = Song.objects.all()
    nextsong = Song.objects.order_by("?").first()

    context =  {
        'song': song,
        'nextsong':nextsong,
        'songs': songs
        }
    return render(request, 'mtunes/songpost.html', context)


@login_required(login_url='login')
def mysongs(request):
    mysongs = Song.objects.filter(uploaded_by=request.user)
    context = {
        'mysongs':mysongs
    }
    return render(request, 'mtunes/mysongs.html', context)

@login_required(login_url='login')
def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        song = Song.objects.get(song_id=music_id)
        history = History(user=user, song=song)
        history.save()

        return redirect('songpost', music_id)

    history = History.objects.filter(user=request.user)

    return render(request, 'mtunes/history.html', {"history": history})

@login_required(login_url='login')
def watchlater(request):
    if request.method == "POST":
        user = request.user
        songid = request.POST['video_id']

        song = Song.objects.get(song_id=songid)
        
        try:
            watch = Watchlater.objects.get(song=song)
            messages.error(request, "Song already exists")
        except:
            watchlater = Watchlater(user=user, song=song)
            watchlater.save()
            messages.success(request, "Song Added Succesfully")

        return redirect('songpost', song.song_id)

    song = Watchlater.objects.filter(user=request.user)

    context = {
        'song':song
    }

    return render(request, "mtunes/watchlater.html", context)

@login_required(login_url='login')
def removewatchlater(request, watch_id):
    watch=Watchlater.objects.get(watch_id=watch_id)
    watch.delete()
    return redirect('watchlater')