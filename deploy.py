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
                '',
                'automatic_scaling:',
                '  min_instances: 1',
                '  max_instances: 1',
                '',
                'inbound_services:',
                '- warmup',
                '',
                'handlers:',
                '- url: /_ah/warmup',
                '  script: warmup.py',
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

