from database.db_config import db, cursor


def add_task(title, description, priority, status, due_date):

    query = """
    INSERT INTO tasks
    (title, description, priority, status, due_date)
    VALUES (?, ?, ?, ?, ?)
    """

    values = (
        title,
        description,
        priority,
        status,
        str(due_date)
    )

    cursor.execute(query, values)

    db.commit()


def get_tasks():

    query = "SELECT * FROM tasks"

    cursor.execute(query)

    return cursor.fetchall()


def delete_task(task_id):

    query = "DELETE FROM tasks WHERE id = ?"

    cursor.execute(query, (task_id,))

    db.commit()


def complete_task(task_id):

    query = "UPDATE tasks SET status = ? WHERE id = ?"

    values = ("Completed", task_id)

    cursor.execute(query, values)

    db.commit()