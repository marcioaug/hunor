import os
import csv
import copy
import logging
import subprocess

from coloredlogs import ColoredFormatter
from collections import namedtuple

from hunor.args import arg_parser_gen, to_options_gen
from hunor.mutation.generate import _create_mutants_dir
from hunor.tools.hunor_plugin import HunorPlugin
from hunor.tools.java_factory import JavaFactory
from hunor.tools.maven_factory import MavenFactory

from hunor.utils import sort_files
from hunor.utils import get_java_files
from hunor.utils import config


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

SimpleMutant = namedtuple('SimpleMutant', [
    'mid',
    'operator',
    'line_number',
    'method',
    'transformation',
    'dir'
])


def configure_logger():
    style = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(style)
    colored = ColoredFormatter(style)
    ch = logging.StreamHandler()
    fh = logging.FileHandler(os.path.join('hunor-evaluation.log'))
    ch.setFormatter(colored)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)


def main():
    options = to_options_gen(arg_parser_gen())
    configure_logger()

    conf = config(options.config_file)
    project_dir = os.path.abspath(os.sep.join(conf['source']))

    logger.debug(project_dir)

    maven = MavenFactory.get_instance()

    maven.compile(project_dir, clean=True)
    maven.test(project_dir)

    _create_mutants_dir(options)

    options.is_enable_reduce = False
    tool = HunorPlugin(copy.deepcopy(options))

    options.is_enable_reduce = True
    tool_reduced = HunorPlugin(copy.deepcopy(options))

    files = get_java_files(options.java_src)

    include = []

    if 'include' in conf:
        include = conf['include']

    with open('time_result.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['file',
                         'full_set_time',
                         'full_set_mutants',
                         'full_set_killed',
                         'full_set_survived',
                         'full_set_stillborn',
                         'full_set_valid',
                         'full_set_score',
                         'reduced_set_time',
                         'reduced_set_mutants',
                         'reduced_set_killed',
                         'reduced_set_survived',
                         'reduced_set_stillborn',
                         'reduced_set_valid',
                         'reduced_set_score'
                         ])

    for i, file in enumerate(sort_files(files)):
        if file in include:
            full_set_result = None
            redu_set_result = None

            try:
                full_set_result = tool.gen(file, analyze=True)
            except subprocess.TimeoutExpired:
                logger.error("Timeout expired while process file {0} to "
                             "generate full set of mutants.".format(file))
            except Exception as e:
                logger.error("Don't stop me now!", e)

            try:
                redu_set_result = tool_reduced.gen(file, analyze=True)
            except subprocess.TimeoutExpired:
                logger.error("Timeout expired while process file {0} to "
                             "generate reduced set of mutants.".format(file))
            except Exception as e:
                logger.error("Don't stop me now!", e)

            if full_set_result and redu_set_result:
                print(full_set_result, redu_set_result)
                with open('time_result.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow([file,
                                     full_set_result[0],
                                     full_set_result[1][0],
                                     full_set_result[1][1],
                                     full_set_result[1][2],
                                     full_set_result[1][3],
                                     full_set_result[1][4],
                                     full_set_result[1][5],
                                     redu_set_result[0],
                                     redu_set_result[1][0],
                                     redu_set_result[1][1],
                                     redu_set_result[1][2],
                                     redu_set_result[1][3],
                                     redu_set_result[1][4],
                                     redu_set_result[1][5],
                                     ])


if __name__ == '__main__':
    main()
