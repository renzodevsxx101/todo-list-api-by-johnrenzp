from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(ViewSet):
    # This is a GET method to retrieve a list of all tasks, categorized into Incoming, Today, and Overdue.
    def list(self, request):
        status_filter = request.query_params.get('status', None)

        if status_filter:
            if status_filter == 'incoming':
                tasks = Task.objects.filter(due_date__gt=date.today())
                data = {"Incoming": [TaskSerializer(task).data for task in tasks]}
            elif status_filter == 'today':
                tasks = Task.objects.filter(due_date=date.today())
                data = {"Today": [TaskSerializer(task).data for task in tasks]}
            elif status_filter == 'overdue':
                tasks = Task.objects.filter(due_date__lt=date.today())
                data = {"Overdue": [TaskSerializer(task).data for task in tasks]}
            else:
                return Response({"message": "Invalid status filter."})

            if not tasks.exists():
                return Response({"message": f"No {status_filter} tasks found."})

        else:
            tasks = Task.objects.all()
            data = {"Incoming": [], "Today": [], "Overdue": []}
            for task in tasks:
                if task.due_date > date.today():
                    data["Incoming"].append(TaskSerializer(task).data)
                elif task.due_date == date.today():
                    data["Today"].append(TaskSerializer(task).data)
                else:
                    data["Overdue"].append(TaskSerializer(task).data)

            if not any(data.values()):
                return Response({"message": "No tasks found."})

        return Response(data)
    
    # This is a  GET method to retrieve details of a specific task based on Id.
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
