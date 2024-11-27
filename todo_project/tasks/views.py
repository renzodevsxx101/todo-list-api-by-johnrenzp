from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(ViewSet):
    # This is a  GET method to retrieve tasks
    def list(self, request):
        tasks = Task.objects.all()
        
        status_filter = request.query_params.get('status', None)

        # This filters tasks based on status query parameter
        if status_filter == 'incoming':
            tasks = tasks.filter(due_date__gt=date.today()) 
        elif status_filter == 'today':
            tasks = tasks.filter(due_date=date.today())
        elif status_filter == 'overdue':
            tasks = tasks.filter(due_date__lt=date.today())
            
        task_data = TaskSerializer(tasks, many=True).data
        return Response(task_data)

    def retrieve(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # This is a POST method to create tasks
    def create(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # This is a PUT method to edit or update tasks 
    def update(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

    # This is a DELETE method to delete tasks 
    def destroy(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
