# Todo App Plan

This document outlines the steps to create the `Todo` application.

## 1. Define the `Todo` Model

The `Todo` model will be defined in `homework_1/todos/models.py` with the following fields:

-   `title`: `models.CharField(max_length=200)`
-   `description`: `models.TextField()`
-   `completed`: `models.BooleanField(default=False)`
-   `priority`: `models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)`

## 2. Create and Run Migrations

After defining the model, we will run the following commands to update the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the `todos_todo` table in the database.
