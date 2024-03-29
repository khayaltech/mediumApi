from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, response, status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from apps.common.tasks import send_email

from .exceptions import CantFollowYourself, NotYourProfile
from .models import Profile
from .paginations import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, ProfileUpdateSerializer

# Create your views here.

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination


class ProfileDetailApiView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        serializer = self.serializer_class(profile, context={"request": request})

        return response.Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = ProfileUpdateSerializer

    @swagger_auto_schema(request_body=ProfileUpdateSerializer)
    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = ProfileUpdateSerializer(
            instance=request.user.profile, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class GetProfileFollower(generics.RetrieveAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")

    def retrieve(self, request, username, *args, **kwargs):
        try:
            userprofile = self.queryset.get(user__username=username)

        except User.DoesNotExist:
            raise NotFound("Profile with that username does not exist")

        user_followers = userprofile.followed_by.all()
        serializer = FollowingSerializer(user_followers, many=True)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "followers": serializer.data,
            "num_of_followers": len(serializer.data),
        }
        return response.Response(formatted_response, status=status.HTTP_200_OK)


class FollowUnfollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    def get(self, request, username):
        try:
            userprofile = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("Profile with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=userprofile.pkid)
        my_following_list = userprofile_instance.following_list()
        serializer = FollowingSerializer(my_following_list, many=True)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "users_i_follow": serializer.data,
            "num_following": len(serializer.data),
        }
        return response.Response(formatted_response, status=status.HTTP_200_OK)

    def post(self, request, username):
        try:
            userprofile = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("Profile with that username does not exist")

        if userprofile == request.user:
            raise CantFollowYourself

        userprofile_instance = Profile.objects.get(user__pkid=userprofile.pkid)
        current_user_profile = request.user.profile

        if current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You already follow {userprofile.username}",
            }
            return response.Response(
                formatted_response, status=status.HTTP_400_BAD_REQUEST
            )

        current_user_profile.follow(userprofile_instance)
        data = {
            "email_body": f"Hi there {userprofile.username}!!,the user {current_user_profile.user.username} now follows you",
            "to_email": userprofile.email,
            "email_subject": "A new user follows you",
        }
        send_email.delay(data)
        return response.Response(
            {
                "status_code": status.HTTP_200_OK,
                "detail": f"You now follow {userprofile.username}",
            }
        )

    def delete(self, request, username):
        try:
            userprofile = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=userprofile.pkid)
        current_user_profile = request.user.profile

        if not current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You do not follow {userprofile.username}",
            }
            return response.Response(
                formatted_response, status=status.HTTP_400_BAD_REQUEST
            )

        current_user_profile.unfollow(userprofile_instance)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "detail": f"You have unfollowed {userprofile.username}",
        }
        return response.Response(formatted_response, status=status.HTTP_200_OK)


##########
profileListView = ProfileListAPIView.as_view()
profilDetailView = ProfileDetailApiView.as_view()
profileUpdateView = ProfileUpdateView.as_view()
getFollowerView = GetProfileFollower.as_view()
followunfollowView = FollowUnfollowApiView.as_view()
