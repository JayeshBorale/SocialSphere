from .models import *
from django.shortcuts import get_object_or_404

def base(request):
    if request.user.is_authenticated:
        try:
            
            current_user_profile = Profile.objects.get(user=request.user)
            prof=get_object_or_404(Profile,user=request.user)
            followers_count=current_user_profile.followers.count()
            following_count = prof.user.following.count()
            notify=notification.objects.filter(user=request.user)
            
            return {
                'current_user': current_user_profile,
                'followers_count':followers_count,
                'following_count':following_count,
                'prof':prof,
                'notify':notify
                
            }
        except Profile.DoesNotExist:
        
            return {
                'current_user': None
            }
    return {}
