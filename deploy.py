import os
import pathlib


class AppYaml:
    def __init__(self, token: str):
        self.token = token

    def __enter__(self):
        self.path = pathlib.Path(__file__).parent.resolve() / 'app.yaml'

        with open(self.path, 'w') as file:
            lines = [
                'runtime: python310',
                '',
                'env_variables:',
                f'   DISCORD_BOT_TOKEN: "{self.token}"',
                f'   BUDBOT_PROJECT_ID: "{os.getenv("BUDBOT_PROJECT_ID")}"',
                f'   GOOGLE_APPLICATION_CREDENTIALS: "{os.getenv("GOOGLE_APPLICATION_CREDENTIALS")}"',
                '',
                'automatic_scaling:',
                '  max_instances: 1',
                '',
                '',
                'entrypoint: python3 main.py'
            ]
            file.write('\n'.join(lines))
        return self

    def __exit__(self, *args):
        os.remove(self.path)


if __name__ == '__main__':
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    with AppYaml(bot_token) as ay:
        os.system(r"gcloud app deploy --quiet")

