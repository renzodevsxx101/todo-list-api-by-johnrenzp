from rest_framework import serializers
from .models import Task
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'created_at', 'completed']

    # This method determines if the task is incoming, today, or overdue based on due_date.
    def get_completed(self, obj):
        today = date.today()
        if obj.due_date > today:
            return "Incoming"
        elif obj.due_date == today:
            return "Today"
        else:
            return "Overdue"
