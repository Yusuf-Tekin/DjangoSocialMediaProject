from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login as dj_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from .models import Post,Likes,Comments,SavePost,Notification,Follow
import json,random



def login(request):

    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == "POST":
            username = request.POST.get('user-username')
            password = request.POST.get('user-password')
            user = authenticate(request,username=username, password=password)        
            if user is not None:
                dj_login(request,user)
                return redirect('/home/')
            else:
                messages.error(request,"Giriş Başarısız")
        return render(request,"login.html")

def register(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == "POST":
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            newUser = User.objects.create_user(username,email,password)
            newUser.first_name = name
            newUser.last_name = surname
            newUser.save()
            return HttpResponse('')
        return render(request,"register.html")

@login_required(login_url= '/login/')
def home(request):
    if request.user.is_authenticated:
        # Tüm veriler
        PostData = Post.objects.all().order_by('Time').reverse()
        CommentsData = Comments.objects.all().order_by('CommentTime').reverse()
        SaveData = SavePost.objects.filter(SaveOwnerId = request.user.id)
        LikeData = Likes.objects.filter(OwnerId = request.user.id)
        NotificationData = Notification.objects.filter(NotificationOwner = request.user.username).order_by('NotificationTime').reverse()
        
        Peoples = User.objects.all()[0:5]
        likelist = []
        savelist =[]

        for x in SaveData:
            savelist.append(x.SavePostId)

        for i in LikeData:
            likelist.append(i.PostId)
        context =  {
            'data'  : PostData,
            'comments' : CommentsData,
            'clientlikedata' : likelist,
            'clientsavedata' : savelist,
            'Notification' : NotificationData,
            'Peoples' : Peoples
        }

        return render(request,"home.html",context)
    else:
        return redirect('/login/')

@login_required(login_url= '/login/')
def Category(request,categoryname):
    CommentsData = Comments.objects.all().order_by('CommentTime').reverse()
    SaveData = SavePost.objects.filter(SaveOwnerId = request.user.id)
    LikeData = Likes.objects.filter(OwnerId = request.user.id)

    likelist = []
    savelist = []
    if categoryname == 'genc':
        PostData = Post.objects.filter(Category = 'Genç').order_by('Time').reverse()

    if categoryname == 'tekno':
        PostData = Post.objects.filter(Category = 'Teknoloji').order_by('Time').reverse()

    if categoryname == 'spor':
        PostData = Post.objects.filter(Category = 'Spor').order_by('Time').reverse()

    if categoryname == 'haber':
        PostData = Post.objects.filter(Category = 'Haber').order_by('Time').reverse()

    if categoryname == 'magazin':
        PostData = Post.objects.filter(Category = 'Magazin').order_by('Time').reverse()

    if categoryname == 'muzik':
        PostData = Post.objects.filter(Category = 'Müzik').order_by('Time').reverse()

    if categoryname == 'egitim':
        PostData = Post.objects.filter(Category = 'Eğitim').order_by('Time').reverse()

    if categoryname == 'astro':
        PostData = Post.objects.filter(Category = 'Astro').order_by('Time').reverse()
    
    for save in SaveData:
        savelist.append(save.SavePostId)
    
    for like in LikeData:
        likelist.append(like.PostId)

    data = {'data' : PostData,'comments' : CommentsData,'clientlikedata' : likelist,'clientsavedata' : savelist}

    return render(request,"categorypage.html",data)

@login_required(login_url= '/login/')
def Logout(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url = '/login/')
def newpost(request):
    if request.method == "POST":
        response = {}
        category = request.POST.get('category')
        content = request.POST.get('content')
        isComment = request.POST.get('isComment')
        if isComment == 'true':
            yorumdeger = True
        else:
            yorumdeger = False

        newpost = Post.objects.create(Category = category,Content = content,IsComment = yorumdeger,OwnerUsername = request.user.username,OwnerName = request.user.first_name,OwnerSurname = request.user.last_name,OwnerId = request.user.id)

        response['name'] = request.user.first_name
        response['surname'] = request.user.last_name
        response['username'] = request.user.username
        response['category'] = category
        response['content'] = content
        response['comments'] = isComment
        response['postid'] = newpost.id
        return JsonResponse(response)

    return HttpResponse('')    

def deletepost(request,id):
    if request.method == "POST":
        DeletePost = Post.objects.get(id = id)
        DeleteLike = Likes.objects.filter(PostId = id)
        DeleteComment = Comments.objects.filter(PostId = id)

        DeleteComment.delete()
        DeleteLike.delete()
        DeletePost.delete()
    elif request.method == "GET":
    
        return redirect('/home/')     
    return HttpResponse('')


def likepost(request,id):
    if request.method == "POST":
        isLikeControl = Likes.objects.filter(PostId = id,OwnerId = request.user.id)

        if len(isLikeControl)>0:
            havelikedata = Likes.objects.get(OwnerId = request.user.id,PostId = id)
            Len = havelikedata.LikeStatus
            havelikedata.save()

        else:
            like = Likes.objects.create(OwnerId = request.user.id,PostId = id,LikeStatus = True)
            like.save()

        return HttpResponse('')
    else:
        return redirect('/home/')


def dislikepost(request,id):
    if request.method == "POST":
        isDislike = Likes.objects.filter(PostId = id,OwnerId = request.user.id)
        if len(isDislike) > 0:
            havelikedata = Likes.objects.filter(OwnerId = request.user.id,PostId = id)
            havelikedata.delete()

        else:
            newlike = Likes.objects.create(OwnerId = request.user.id,PostId = id,LikeStatus = False)
            newlike.delete()
        return HttpResponse('')
    else:
        return redirect('/home/')


def save(request,id):
    if request.method == "POST":
        isSaveControl = SavePost.objects.filter(SaveOwnerId = request.user.id,SavePostId = id);
        if len(isSaveControl) > 0:
            havedata = SavePost.objects.get(SaveOwnerId = request.user.id,SavePostId = id)
            havedata.SaveStatus = True
            havedata.save()
        else:
            SavePost.objects.create(SaveOwnerId = request.user.id,SavePostId = id,SaveStatus = True)

        return HttpResponse('')
    else:
        return redirect('/home/')

def savedelete(request,id):
    if request.method == "POST":
        saveupdate = SavePost.objects.filter(SaveOwnerId = request.user.id,SavePostId = id);
        if len(saveupdate):
            havedata = SavePost.objects.filter(SaveOwnerId = request.user.id,SavePostId = id)
            havedata.delete()
        else:
            newsave = SavePost.objects.create(SaveOwnerId = request.user.id,SavePostId = id,SaveStatus = False)
            newsave.delete()
        return HttpResponse('')
    else:
        return redirect('/home/')


def comment(request,id):
    if request.method == "POST":
        responsecomment = {}
        GetComment = request.POST.get('comment') 
        NewComment = Comments.objects.create(CommentsOwner = request.user.username,CommentsOwnerId = request.user.id,Comment = GetComment,PostId = id)
        responsecomment['Owner'] = request.user.username
        responsecomment['Comment'] = GetComment
        responsecomment['commentid'] = NewComment.id

        return JsonResponse(responsecomment)
    else:
        return redirect('/home/')
        
def commentdelete(request,id):
    if request.method == "POST":
        CommentDel = Comments.objects.get(id = id)
        CommentDel.delete()
        return HttpResponse('')
    else:
        return redirect('/home/')




@login_required(login_url= "/login/")
def profile(request):
    return render(request,"profile.html")


@login_required(login_url= "/login/")

def saves(request):
    
    savesdata = []
    SaveData = SavePost.objects.filter(SaveOwnerId = request.user.id)
    
    for x in SaveData:
            data = Post.objects.get(id = x.SavePostId)
            savesdata.append(data)
    
    return render(request,"saves.html",{'data' : savesdata})

@login_required(login_url= "/login/")

def favorite(request):

    likelist = []

    LikeData = Likes.objects.filter(OwnerId = request.user.id)
    if len(LikeData) > 0:

        for y in LikeData:
            data = Post.objects.get(id = y.PostId)
            likelist.append(data)

    context = {
        'data' : likelist
    }
    return render(request,"favorite.html",context)


@login_required(login_url= "/login/")

def updateprofile(request):
    if request.method == "POST":
        data = request.POST.get('newusername')
        update = User.objects.get(username = request.user.username)
        update.username = data
        update.save()
    return HttpResponse('')

@login_required(login_url= "/login/")

def userprofile(request,id):
    followinglist = []

    userdata = User.objects.filter(id = id)
    followdata = Follow.objects.filter(FollowSentById = request.user.id)

    for follow in followdata:
        followinglist.append(follow.FollowOwnerId)

    print(followinglist)
    data = {
        'data' : userdata,
        'followdata' : followinglist
    }
    return render(request,"userprofile.html",data)



@login_required(login_url= "/login/")

def notification(request,type):
    if request.method =="POST":
        NotificationOwner = request.POST.get('NotificationOwner')
        NotificationOwnerId = request.POST.get('NotificationOwnerId')
        NotificationType = type
        NotificationSentBy = request.POST.get('NotificationSentBy')
        NotificationPostId = request.POST.get('NotificationPostId')

        print('NotOwner -> ' ,NotificationOwner, '\nSentBy -> ' + NotificationSentBy)
        newnotification = Notification.objects.create(
                NotificationOwner = NotificationOwner,
                NotificationOwnerId = NotificationOwnerId,
                NotificationType = NotificationType,
                NotificationSentBy = NotificationSentBy,
                NotificationPostId = NotificationPostId,
                NotificationStatus = False
        )
    
    return HttpResponse('')
@login_required(login_url= "/login/")

def deletenotification(request):
    if request.method =="POST":
        NotificationOwner = request.POST.get('NotificationOwner')
        NotificationOwnerId = request.POST.get('NotificationOwnerId')
        NotificationType = request.POST.get('NotificationType')
        NotificationSentBy = request.POST.get('NotificationSentBy')
        NotificationPostId = request.POST.get('NotificationPostId')

        delnotification = Notification.objects.get(
            NotificationOwner = NotificationOwner,
            NotificationOwnerId = NotificationOwnerId,
            NotificationType = NotificationType,
            NotificationSentBy = NotificationSentBy,
            NotificationPostId  = NotificationPostId
        )
        delnotification.delete()

    return HttpResponse('')

@login_required(login_url= "/login/")
def readNotification(request,id):
    data = Notification.objects.get(id = id)
    data.NotificationStatus = 1
    data.save()
    return HttpResponse('')

def follow(request,id):
    if request.method == "POST":
        FollowOwner = request.POST.get('FollowOwner')
        FollowOwnerId = request.POST.get('FollowOwnerId')
        FollowSentByOwner = request.POST.get('FollowSentByOwner')
        FollowSentByOwnerId = request.POST.get('FollowSentByOwnerId')

        newfollow = Follow.objects.create(FollowOwner = FollowOwner,FollowOwnerId = FollowOwnerId,FollowSentBy = FollowSentByOwner,FollowSentById = FollowSentByOwnerId )


    return HttpResponse('')

def followdelete(request,id):
    if request.method == "POST":
        FollowOwner = request.POST.get('FollowOwner')
        FollowOwnerId = request.POST.get('FollowOwnerId')
        FollowSentByOwner = request.POST.get('FollowSentByOwner')
        FollowSentByOwnerId = request.POST.get('FollowSentByOwnerId')

        FollowDel = Follow.objects.get(FollowOwnerId = FollowOwnerId,FollowSentById = FollowSentByOwnerId)
        FollowDel.delete()

        #print('Bilgiler-> \nOwner =' , FollowOwner , '\nId -> ' ,FollowOwnerId ,'\nFollowSentOwner = ' , FollowSentByOwner , '\nFollowSentId = ' , FollowSentByOwnerId)
    return HttpResponse('')