from django.test import TestCase
from django.utils import timezone
from .models import Todo


class TodoModelTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="This is a test todo item",
            priority=Todo.Priority.HIGH
        )

    def test_todo_creation(self):
        """Test creating a todo with all fields."""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "This is a test todo item")
        self.assertEqual(self.todo.priority, Todo.Priority.HIGH)
        self.assertFalse(self.todo.completed)
        self.assertIsNotNone(self.todo.created_at)
        self.assertIsNotNone(self.todo.updated_at)

    def test_todo_creation_minimal(self):
        """Test creating a todo with only required fields."""
        minimal_todo = Todo.objects.create(title="Minimal Todo")
        self.assertEqual(minimal_todo.title, "Minimal Todo")
        self.assertIsNone(minimal_todo.description)  # Field is null=True, so it should be None
        self.assertEqual(minimal_todo.priority, Todo.Priority.MEDIUM)
        self.assertFalse(minimal_todo.completed)
        self.assertIsNotNone(minimal_todo.created_at)
        self.assertIsNotNone(minimal_todo.updated_at)

    def test_todo_string_representation(self):
        """Test the __str__ method returns the title."""
        self.assertEqual(str(self.todo), "Test Todo")

    def test_todo_priority_choices(self):
        """Test that priority choices are correctly defined."""
        self.assertEqual(Todo.Priority.LOW.value, 1)
        self.assertEqual(Todo.Priority.MEDIUM.value, 2)
        self.assertEqual(Todo.Priority.HIGH.value, 3)
        self.assertEqual(Todo.Priority.LOW.label, 'Low')
        self.assertEqual(Todo.Priority.MEDIUM.label, 'Medium')
        self.assertEqual(Todo.Priority.HIGH.label, 'High')

    def test_todo_ordering(self):
        """Test that todos are ordered by creation date (newest first) when using the view's ordering."""
        older_todo = Todo.objects.create(title="Older Todo")
        newer_todo = Todo.objects.create(title="Newer Todo")
        
        # The view uses order_by('-created_at'), so we test with that ordering
        todos = Todo.objects.all().order_by('-created_at')
        self.assertEqual(todos[0].title, "Newer Todo")
        self.assertEqual(todos[1].title, "Older Todo")
        self.assertEqual(todos[2].title, "Test Todo")

    def test_todo_completion(self):
        """Test marking a todo as completed."""
        self.assertFalse(self.todo.completed)
        self.todo.completed = True
        self.todo.save()
        updated_todo = Todo.objects.get(pk=self.todo.pk)
        self.assertTrue(updated_todo.completed)


class TodoViewTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="This is a test todo item",
            priority=Todo.Priority.HIGH
        )

    def test_todo_list_view(self):
        """Test the todo list view."""
        response = self.client.get('/todos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")
        self.assertContains(response, "This is a test todo item")
        self.assertContains(response, "High")

        # Test that active_todos and completed_todos are in context
        self.assertIn('active_todos', response.context)
        self.assertIn('completed_todos', response.context)

    def test_todo_list_view_separates_active_and_completed(self):
        """Test that the view separates active and completed todos."""
        # Create a completed todo
        Todo.objects.create(
            title="Completed Todo",
            description="This is completed",
            completed=True
        )

        response = self.client.get('/todos/')
        self.assertEqual(response.status_code, 200)

        # Check active todos only contains uncompleted todos
        active_todos = response.context['active_todos']
        self.assertEqual(active_todos.count(), 1)
        self.assertEqual(active_todos[0].title, "Test Todo")
        self.assertFalse(active_todos[0].completed)

        # Check completed todos only contains completed todos
        completed_todos = response.context['completed_todos']
        self.assertEqual(completed_todos.count(), 1)
        self.assertEqual(completed_todos[0].title, "Completed Todo")
        self.assertTrue(completed_todos[0].completed)

    def test_create_todo_view_get(self):
        """Test the create todo view GET request."""
        response = self.client.get('/todos/create/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Todo")

    def test_create_todo_view_post_valid(self):
        """Test the create todo view POST request with valid data."""
        response = self.client.post('/todos/create/', {
            'title': 'New Todo',
            'description': 'A new todo item',
            'priority': Todo.Priority.LOW
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertRedirects(response, '/todos/')
        
        # Check if the new todo was created
        new_todo = Todo.objects.get(title='New Todo')
        self.assertEqual(new_todo.description, 'A new todo item')
        self.assertEqual(new_todo.priority, Todo.Priority.LOW)

    def test_create_todo_view_post_invalid(self):
        """Test the create todo view POST request with invalid data."""
        response = self.client.post('/todos/create/', {
            'title': '',  # Empty title should be invalid
            'description': 'A todo without a title'
        })
        self.assertEqual(response.status_code, 200)  # Should return the form again
        self.assertContains(response, "Create Todo")
        
        # Check that no new todo was created
        self.assertEqual(Todo.objects.count(), 1)

    def test_update_todo_view_get(self):
        """Test the update todo view GET request."""
        response = self.client.get(f'/todos/update/{self.todo.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")
        self.assertContains(response, "This is a test todo item")

    def test_update_todo_view_post(self):
        """Test the update todo view POST request."""
        response = self.client.post(f'/todos/update/{self.todo.pk}/', {
            'title': 'Updated Todo',
            'description': 'Updated description',
            'priority': Todo.Priority.MEDIUM,
            'completed': 'on'  # Checkbox is 'on' when checked
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.assertRedirects(response, '/todos/')
        
        # Check if the todo was updated
        updated_todo = Todo.objects.get(pk=self.todo.pk)
        self.assertEqual(updated_todo.title, 'Updated Todo')
        self.assertEqual(updated_todo.description, 'Updated description')
        self.assertEqual(updated_todo.priority, Todo.Priority.MEDIUM)
        self.assertTrue(updated_todo.completed)

    def test_update_todo_view_nonexistent(self):
        """Test updating a non-existent todo."""
        response = self.client.get('/todos/update/999/')
        self.assertEqual(response.status_code, 404)

    def test_delete_todo_view_get(self):
        """Test the delete todo view GET request."""
        response = self.client.get(f'/todos/delete/{self.todo.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")
        self.assertContains(response, "Are you sure")

    def test_delete_todo_view_post(self):
        """Test the delete todo view POST request."""
        response = self.client.post(f'/todos/delete/{self.todo.pk}/')
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertRedirects(response, '/todos/')
        
        # Check if the todo was deleted
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())

    def test_delete_todo_view_nonexistent(self):
        """Test deleting a non-existent todo."""
        response = self.client.get('/todos/delete/999/')
        self.assertEqual(response.status_code, 404)
