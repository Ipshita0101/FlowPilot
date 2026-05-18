from database.db_config import cursor


def get_dashboard_data():

    cursor.execute(
        "SELECT COUNT(*) FROM tasks"
    )

    total_tasks = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Completed'"
    )

    completed_tasks = cursor.fetchone()[0]


    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Pending'"
    )

    pending_tasks = cursor.fetchone()[0]


    if total_tasks > 0:

        productivity = (
            completed_tasks / total_tasks
        ) * 100

    else:

        productivity = 0


    return (
        total_tasks,
        completed_tasks,
        pending_tasks,
        productivity
    )