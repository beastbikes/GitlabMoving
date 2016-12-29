import os
import gitlab

FROM_GITLAB_HOST = os.environ['FROM_GITLAB_HOST']
FROM_GITLAB_TOKEN = os.environ['FROM_GITLAB_TOKEN']
TO_GITLAB_HOST = os.environ['TO_GITLAB_HOST']
TO_GITLAB_TOKEN = os.environ['TO_GITLAB_TOKEN']
DEFAULT_NEW_USER_PASSWORD = os.environ['DEFAULT_NEW_USER_PASSWORD']

# private token authentication
from_gl = gitlab.Gitlab(FROM_GITLAB_HOST, FROM_GITLAB_TOKEN)
from_gl.auth()

# private token authentication
to_gl = gitlab.Gitlab(TO_GITLAB_HOST, TO_GITLAB_TOKEN)
to_gl.auth()


def merge_user():
    # list all the projects
    users = from_gl.users.list(all=True)
    for user in users:
        user_data = {
            'email': user.email,
            'username': user.username,
            'name': user.name,
            'password': DEFAULT_NEW_USER_PASSWORD
        }
        print(user_data)
        try:
            user = to_gl.users.create(user_data)
            print(user)
        except Exception as e:
            print(e)


def merge_group():
    groups = from_gl.groups.list()
    for group in groups:
        data = {
            "name": group.name,
            "path": group.path,
            "description": group.description,
        }
        print(data)
        try:
            group = to_gl.groups.create(data)
            print(group)
        except Exception as e:
            print(e)


def to_user_mapping():
    to_users = to_gl.users.list(all=True)

    user_data = {}
    for to_user in to_users:
        user_data[to_user.username] = to_user.id

    return user_data


def merge_issues(from_project_id, to_project_id):
    issues = from_gl.projects.get(from_project_id).issues.list(all=True)
    project = to_gl.projects.get(to_project_id)
    user_data = to_user_mapping()
    for issue in issues:
        data = {
            "id": to_project_id,
            "title": issue.title,
            "description": issue.description,
            "due_date": issue.due_date,
            "created_at": issue.created_at,
            "labels": issue.labels,
        }

        if issue.assignee:
            user_id = user_data.get(issue.assignee.username)
            if user_id:
                data["assignee_id"] = user_id

        print(data)
        try:
            new_issue = project.issues.create(data)
            if issue.state == 'closed':
                new_issue.state_event = 'close'
                new_issue.save()
            print(new_issue)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    merge_issues(39, 4)
