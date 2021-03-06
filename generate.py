#!/usr/bin/env python
import yaml
import click
import jinja2
import logging
import os

logger = logging.getLogger('default')


def load_data(file):
    with open(file, 'r') as stream:
        return yaml.load(stream, Loader=yaml.SafeLoader)


@click.command()
@click.option('--data', type=click.STRING,
              help='Data input', default='data/config.yml')
@click.option('--template', type=click.STRING,
              help='Name of the template to apply', default='actions.js')
@click.option('-o', '--output', help='Output file name', default='')
@click.option('-v', '--verbose', count=True, help='Increment verbosity')
def code_generator_app(data, template, output, verbose):
    templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    if not os.path.isfile(data):
        logger.error('Data argument invalid')
        return
    if not os.path.isfile('templates/{}'.format(template)):
        logger.error('Template argument invalid')
        return

    template_instance = templateEnv.get_template(template)

    data_content = load_data(data)
    rendered_content = template_instance.render(**data_content)

    if not os.path.exists('output'):
        os.makedirs('output')

    if not output:
        output = template

    with open('output/{0}'.format(output), 'w') as wf:
        wf.write(rendered_content)


if __name__ == '__main__':
    code_generator_app()
