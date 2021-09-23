#from django.contrib.auth.models import User
from applications.events.serializers import UsersSerializers
from applications.users.models import Membership, Tribes, User
from django.contrib.auth.models import Permission
from django.db.models import fields
from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers


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


class MembershipSerializer(serializers.ModelSerializer):
    #user = serializers.ReadOnlyField(source='user.id')
    user = MembersSerializer()

    class Meta:
        model = Membership
        fields = ('user', 'is_admin',)


class RetrieveMembersSerializer(serializers.ModelSerializer):
    members = MembershipSerializer(source='membership_set', many=True)

    class Meta:
        model = Tribes
        fields = (
            'id',
            'members'
        )


class TribesSerializer(serializers.ModelSerializer):
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
            'sum_members'
        )

    def get_sum_members(self, obj):
        return obj.members.count()


class ListMembersSerializer(serializers.ListField):
    """  formato para una lista de tipo serializador """

    user = serializers.IntegerField()


class ListAdminSerializer(serializers.ListField):
    """ Lista de id con permisos de admin """
    id = serializers.IntegerField()


class AdminSerializer(serializers.Serializer):
    members = ListAdminSerializer()


class CRUD_TribesSerializer(serializers.Serializer):
    """ serializador para enviar los correos """

    name = serializers.CharField()
    description = serializers.CharField(required=False)
    user = serializers.IntegerField()
    avatar = serializers.ImageField(required=False)
    members = ListMembersSerializer(required=False)


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'names',
            'last_names',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['names'],
            validated_data['last_names'],
            validated_data['password'],
        )

        return user


class ContactSerializer(serializers.Serializer):
    """ serializador para recuperar password de acceso """

    contact = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    """ serializador para recuperar password de acceso """

    token_id = serializers.CharField(required=True)


class EmailsListSerializer(serializers.ListField):
    """  formato para una lista de tipo serializador """

    emails = serializers.CharField()


class InvitationSerializer(serializers.Serializer):
    """ serializador para enviar los correos """

    idEvent = serializers.IntegerField(required=True)
    listEmails = EmailsListSerializer()


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
