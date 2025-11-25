# Todo App Plan

This document outlines the steps to create the `Todo` application.

## 1. Define the `Todo` Model

The `Todo` model will be defined in `homework_1/todos/models.py` with the following fields:

- `title`: `models.CharField(max_length=200)`
- `description`: `models.TextField()`
- `completed`: `models.BooleanField(default=False)`
- `priority`: `models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2)`

## 2. Create and Run Migrations

After defining the model, we will run the following commands to update the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the `todos_todo` table in the database.

## 3. About the development of this app

This app was created using Visual Studio Code. The AI agents used are `kilo code` and `claude code`.

The initial implementation was using `kilo code` with `gemini pro 2.5` in architecture mode to plan for the app.

The code was generated using `kilo code` with `glm-4.6`.

`glm-4.6` generated all the django files and created the test files.

The problem came to when running the tests, where 7 of the 17 tests had failed. It failed because of wrong syntax for the html template.

I am not well versed in django and have some basic understanding of python. In any case, `glm-4.6` was not able to fix the `failed tests`.

Using `gemini pro 2.5` with `kilo code` and after 5 minutes, it was not able to.

I resorted to `claude code`, which picked up the error straight away!. This was due to improperly formatted template. I guess if I was more familiar with the language, I may have picked this up.

This demonstrates that vibe coding is only good if all goes to plan. But when errors comes up, AI can only help so much and this is also model dependent along with $$$$.
