#from django.contrib.auth.models import User
from applications.events.serializers import UsersSerializers
from applications.users.models import Tribes, User
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'names',
            'last_names',
            'gender',
            'date_birth',
            'avatar',
            'get_full_name'
        )


class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'avatar',
            'get_full_name',
            'get_initials'
        )


class TribesSerializer(serializers.ModelSerializer):
    #user = MembersSerializer()
    user = UsersSerializers()
    sum_members = serializers.SerializerMethodField()

    class Meta:
        model = Tribes
        fields = (
            'id',
            'name',
            'description',
            'user',
            'avatar',
            # 'members',
            'sum_members'
        )

    def get_sum_members(self, obj):
        return obj.members.count()


class RetrieveMembersSerializer(serializers.ModelSerializer):
    members = MembersSerializer(many=True)

    class Meta:
        model = Tribes
        fields = (
            'id',
            'members'
        )


class CRUD_TribesSerializer(serializers.ModelSerializer):
    # members = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=User.objects.all())

    class Meta:
        model = Tribes
        fields = (
            'id',
            'name',
            'description',
            'user',
            'avatar',
            'members'
        )


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'names',
            'last_names',
            'gender'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            validated_data['names'],
            validated_data['last_names'],
            validated_data['gender']
        )

        return user


class LoginSerializer(serializers.Serializer):
    """ serializador para recuperar password de acceso """

    token_id = serializers.CharField(required=True)


class EmailsListSerializer(serializers.ListField):
    """  formato para una lista de tipo serializador """

    emails = serializers.CharField()


class InvitationSerializer(serializers.Serializer):
    """ serializador para enviar los correos """

    idEvent = serializers.IntegerField(required=True)
    # listEmails = serializers.ListField(
    #     emails=serializers.CharField()
    # )
    listEmails = EmailsListSerializer()


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
