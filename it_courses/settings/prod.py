import os
import raven

RAVEN_CONFIG = {
    'dsn': 'https://ad91aa085a6e4a638cb75d1af79fb8a4:a8621045f0494a7c95cbd79206298cc5@sentry.io/1196364',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}
DEBUG = False
