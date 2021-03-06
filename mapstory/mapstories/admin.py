from django.contrib import admin

from mapstory.mapstories.models import StoryFrame, StoryPin


class StoryFrameAdmin(admin.ModelAdmin):
    list_display = ('id', 'map', 'title')
    list_filter = ('map',)
    search_fields = ('map__title', 'title', 'description',)


class StoryPinAdmin(admin.ModelAdmin):
    list_display = ('id', 'map', 'title')
    list_filter = ('map', 'in_map', 'in_timeline',)
    search_fields = ('map__title', 'title', 'content',)


admin.site.register(StoryFrame, StoryFrameAdmin)
admin.site.register(StoryPin, StoryPinAdmin)
