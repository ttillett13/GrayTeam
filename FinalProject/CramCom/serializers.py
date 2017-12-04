from rest_framework import serializers

"""
example to serialize db data into JSON data when pulling.
Is necessary to be able to use the db data in React.

"""


class ExampleSerializer(serializers.ModelSerializer):
    model = None  # change to equal a desired model class
