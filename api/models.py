from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from typing import Dict, Any

#Create your models here.
class User(AbstractUser):
    '''
    Custom User model inheriting from Django's AbstractUser
    to make use of Django's authentication system while adding
    hobby and friend-related functionality
    '''
    
    id = models.AutoField(primary_key=True) 
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True)
    profile = models.OneToOneField(
        to='Profile',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    hobbies = models.ManyToManyField(
        to='Hobby',
        blank=True,
        related_name='users'
    )
    friends = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=False,
        through='Friends',
        related_name='related_to'
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'profile'):
            Profile.objects.create(user=self)

    def __str__(self) -> str:
        return self.username

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'first_name': self.first_name,  
            'last_name': self.last_name,    
            'username': self.username,
            'email': self.email,
            'date_of_birth': self.date_of_birth.strftime("%Y-%m-%d") if self.date_of_birth else None,
            'profile': self.profile.to_dict() if self.profile else None,
            'hobbies': [hobby.to_dict() for hobby in self.hobbies.all()],
            'age': self.age,
        }

    @property
    def age(self) -> int:
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < 
                (self.date_of_birth.month, self.date_of_birth.day)
            )
        return 0

    @property
    def friend_count(self) -> int:
        '''Count of confirmed friends'''
        return Friends.objects.filter(
            (models.Q(from_user=self) | models.Q(to_user=self)) &
            models.Q(status='accepted')
        ).count()

    def get_common_hobbies(self, other_user: 'User') -> int:
        '''Count number of hobbies in common with another user'''
        return self.hobbies.filter(id__in=other_user.hobbies.all()).count()


class Profile(models.Model):
    '''
    Profile model for additional user information
    '''
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )

    def __str__(self) -> str:
        return f"Profile for {self.user.username}"

    def to_dict(self) -> Dict[str, Any]:
        return {}


class Hobby(models.Model):
    '''
    Hobby model to store available hobbies
    '''
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_hobbies'
    )

    class Meta:
        verbose_name_plural = "hobbies"

    def __str__(self) -> str:
        return self.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M"),
            'created_by': self.created_by.username if self.created_by else None,
        }


class Friends(models.Model):
    '''
    Through model for managing friend relationships between users
    '''
    SENT = 'sent'    
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests',  
        null=True 
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_requests',  
        null=True
    )

    timestamp = models.DateTimeField(auto_now_add=True, null=False)  

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=SENT  
    )

    class Meta:  
        verbose_name_plural = "Friends Requests"

    def __str__(self):
        return f"Friend request from {self.from_user.username} to {self.to_user.username} ({self.status})"
    
    def to_dict(self, current_user=None) -> Dict[str, Any]:
        friend_user = self.from_user if self.to_user == current_user else self.to_user
        return {
            'id': self.id,
            'friend_username': friend_user.username,  # This will show the friend's username
            'from_user': self.from_user.username,
            'to_user': self.to_user.username,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M"),
            'status': self.status,
        }