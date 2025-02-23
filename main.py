import urllib.request
import json
import sys


def getUserActivity(username, filter):
    try:
        with urllib.request.urlopen(f"https://api.github.com/users/{username}/events") as resp:
            events = json.load(resp)
    except Exception as err:
        print(f"Error occured: {err}")
        return

    for event in events:
        event_type = event["type"]
        repo_name = event["repo"]["name"]

        if not events:
            print(f"Нет недавней активности у {username}.")
            return

        if filter == "all":
            if event_type == "PushEvent":
                commits = len(event["payload"]["commits"])
                print(f"{username} pushed {commits} commit(s) to {repo_name}")

            elif event_type == "PullRequestEvent":
                action = event["payload"]["action"]
                print(f"{username} {action} a pull request in {repo_name}")

            elif event_type == "ForkEvent":
                print(f"{username} forked {repo_name}")

            elif event_type == "IssuesEvent":
                action = event["payload"]["action"]
                issue_number = event["payload"]["issue"]["number"]
                print(f"{username} {action} issue #{issue_number} in {repo_name}")

            elif event_type == "WatchEvent":
                print(f"{username} starred {repo_name}")

            else:
                print(f"{username} did {event_type} in {repo_name}")

        elif filter == "push":
            if not ("type", "PushEvent") in event.items():
                print("No such user activity")
                return
            if event_type == "PushEvent":
                commits = len(event["payload"]["commits"])
                print(f"{username} pushed {commits} commit(s) to {repo_name}")

        elif filter == "pull":
            if not ("type", "PullRequestEvent") in event.items():
                print("No such user activity")
                return
            if event_type == "PullRequestEvent":
                action = event["payload"]["action"]
                print(f"{username} {action} a pull request in {repo_name}")

        elif filter == "fork":
            if not ("type", "ForkEvent") in event.items():
                print("No such user activity")
                return
            if event_type == "ForkEvent":
                print(f"{username} forked {repo_name}")

        elif filter == "issue":
            if not ("type", "IssuesEvent") in event.items():
                print("No such user activity")
                return
            if event_type == "IssuesEvent":
                action = event["payload"]["action"]
                issue_number = event["payload"]["issue"]["number"]
                print(f"{username} {action} issue #{issue_number} in {repo_name}")

        elif filter == "watch":
            if not ("type", "WatchEvent") in event.items():
                print("No such user activity")
                return
            if event_type == "WatchEvent":
                print(f"{username} starred {repo_name}")

        else:
            print("Incorrect filter")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <github_username> <filter>")
    else:
        getUserActivity(sys.argv[1], sys.argv[2])
