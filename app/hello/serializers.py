from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.serializers import IntegerField, BooleanField, CharField
from hello.models import Page, User, Notification, Category, Item


class PageSerializer(ModelSerializer):

    class Meta:
        model = Page
        fields = ('id', 'user', 'title', 'description')


class MyUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_admin', 'is_moderator')
        read_only_fields = ('id', 'is_admin', 'is_moderator')


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ('requester', 'title', 'invoke_on')


class UserReportSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_admin', 'is_moderator', 'count_pages')
        read_only_fields = ('id', 'is_admin', 'is_moderator', 'count_pages')

    def build_unknown_field(self, field_name, model_class):
        if field_name == 'count_pages':
            return IntegerField, {}
        super().build_unknown_field(field_name, model_class)


class UserReportSerializer2(Serializer):
    id = IntegerField()
    email = CharField()
    is_admin = BooleanField()
    is_moderator = BooleanField()
    count_pages = IntegerField()


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'value')


class SimpleCategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('name',)


class CategorySerializer(ModelSerializer):
    items = ItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        category = Category.objects.create(**validated_data)
        self._create_items(category, items_data)

        return category

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.items.all().delete()
        self._create_items(instance, items_data)
        return super().update(instance, validated_data)

    def _create_items(self, category, items_data):
        Item.objects.bulk_create(
            Item(category=category, **data)
            for data in items_data
        )

    class Meta:
        model = Category
        fields = ('id', 'name', 'items')
