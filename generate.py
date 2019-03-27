#!/usr/bin/env python
import yaml
import click
import jinja2
import logging

logger = logging.getLogger('default')


def load_data(file):
    with open(file, 'r') as stream:
        return yaml.load(stream)


@click.command()
@click.option('--data', type=click.STRING,
              help='Data input', default='data.properties')
@click.option('--template', type=click.STRING,
              help='Name of the template to apply', default='example.java')
@click.option('-v', '--verbose', count=True, help='Increment verbosity')
def code_generator_app(data, template, verbose):

    templateLoader = jinja2.FileSystemLoader(searchpath="templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_instance = templateEnv.get_template(template)

    data_content = load_data(data)
    template_instance.render(**data_content)

    with open('output/{0}.out'.format(template), 'w') as wf:
        wf.write(template_instance)


if __name__ == '__main__':
    code_generator_app()
