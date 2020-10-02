from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views import View

from .forms import FriendForm
from .models import Friend


class FriendView(View):
    form_class = FriendForm
    template_name = "index.html"

    def get(self, *args, **kwargs):
        form = self.form_class()
        friends = Friend.objects.all()
        return render(self.request, self.template_name,
                      {"form": form, "friends": friends})

    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            form = self.form_class(self.request.POST)
            if form.is_valid():
                instance = form.save()
                ser_instance = serializers.serialize('json', [instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)

    # def get_object(self, queryset=None):
    #     obj = Friend.objects.filter(pk=self.kwargs['friend_id']).first()
    #     return obj


def find_by_nickname(request):
    # request should be ajax and method should be GET.
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        nick_name = request.GET.get("nick_name", None)
        try:
            friend = Friend.objects.get(nick_name=nick_name)
        except Friend.DoesNotExist:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"success": False}, status=404)
        data = {
            "success": True,
            "friend": {
                "nick_name": friend.nick_name,
                "first_name": friend.first_name,
                "last_name": friend.last_name,
                "likes": friend.likes,
                "lives_in": friend.lives_in,
            },
        }
        return JsonResponse(data, status=200)
