Title: Fix Django's runserver when run under Docker or PyCharm
Date: 2016-03-14
Status: published
Tags: django, docker, pycharm

When running Django's `runserver` management command in a Docker container or under a PyCharm run configuration (in Linux at least), I very often had issues with the process not getting killed in a timely manner. The symptom is that the process doesn't die immediately after it receives a SIGTERM or SIGINT. This is very puzzling, as hitting `ctrl-c` in a terminal kills it immediately like it's supposed to. There doesn't seem to be any reason for it to not die.

When run in a Docker container, such as part of a Docker Compose service, the symptom is that doing a `docker-compose stop` takes over 10 seconds to complete. It's really annoying when you're doing a lot of iteration testing of a compose config and want to `up`/`down` a lot.

Under PyCharm, the problem is that hitting Stop on the configuration doesn't seem to work at all, and instead you have to hit the skull icon that appears when the stop fails to happen within a second or so. Not that bad, but annoying none-the-less, especially if you're switching from Run to Debug and back on a regular basis.

Either way, it's the little things that are annoying and distracting from getting your real work done. So I dug into it a little, and I think I have a fix.

## The quick fix

The quick fix is to specifically listen for `SIGINT` and `SIGTERM` in your manage.py, and `sys.kill()` when you get them. So modify your manage.py to add a signal handler:

```python
def sighandler(signum, frame):
    sys.exit(1)
```

Then install that signal handler as part of the `__main__` code:

```python
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sighandler)
    signal.signal(signal.SIGINT, sighandler)
```

So here is an example of a complete manage.py, based on the skeleton version you get from `django-admin startproject` with Django 1.9.

```python
#!/usr/bin/env python
import os
import sys
import signal


def sighandler(signum, frame):
    sys.exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sighandler)
    signal.signal(signal.SIGINT, sighandler)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
```

## The why

You know, I've looked into this a little bit, and written all kinds of test code to try to suss out exactly what is happening, but I can't really make heads or tails of it. The problem still persists if you use `--noreload` so that `runserver` doesn't use the autoreloader code, which uses threading. So it's not a clash between signals and threads, which is typically a problem. Conversely, when I try to narrow it down to issues with only the parent process getting the signal, or only the child, or it being a process group in the shell but not in Docker or PyCharm, I get conflicting results that don't seem to point to a clear explanation. I think understanding it would require a lot more time, and a lot more expertise into the bowels of CPython and the shell vs Docker's simplified environment or exactly how PyCharm execs your commands from Java. For now, having a quick fix is enough. If anyone knows what's going on, please enlighten me.
