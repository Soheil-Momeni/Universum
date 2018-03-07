# -*- coding: UTF-8 -*-

from . import jenkins_driver, teamcity_driver, local_driver, utils
from .gravity import Module, Dependency

__all__ = [
    "Output",
    "needs_output"
]


def needs_output(klass):
    klass.out_factory = Dependency("Output")
    original_init = klass.__init__

    def new_init(self, *args, **kwargs):
        self.out = self.out_factory()
        original_init(self, *args, **kwargs)

    klass.__init__ = new_init

    return klass


class Output(Module):
    teamcity_driver_factory = Dependency(teamcity_driver.TeamCityOutput)
    local_driver_factory = Dependency(local_driver.LocalOutput)
    jenkins_driver_factory = Dependency(jenkins_driver.JenkinsOutput)

    @staticmethod
    def define_arguments(argument_parser):
        parser = argument_parser.get_or_create_group("Output", "Log appearance parameters")
        parser.add_argument("--out-type", "-ot", dest="type", choices=["tc", "term", "jenkins"],
                            help="Type of output to produce (tc - TeamCity, jenkins - Jenkins, term - terminal). "
                                 "TeamCity environment is detected automatically when launched on build agent.")

    def __init__(self, settings):
        self.driver = utils.create_diver(local_factory=self.local_driver_factory,
                                         teamcity_factory=self.teamcity_driver_factory,
                                         jenkins_factory=self.jenkins_driver_factory,
                                         default=settings.type)

    def log(self, line):
        self.driver.log(line)

    def log_external_command(self, command):
        self.driver.log_external_command(command)

    def open_block(self, number, name):
        self.driver.open_block(number, name)

    def close_block(self, number, name, status):
        self.driver.close_block(number, name, status)

    def report_build_status(self, status):
        self.driver.change_status(status)

    # TODO: pass build problem to the Report module
    def report_build_problem(self, problem):
        self.driver.report_error(problem)

    def report_skipped(self, message):
        self.driver.report_skipped(message)

    def log_exception(self, line):
        self.driver.log_exception(line)

    def log_stderr(self, line):
        self.driver.log_stderr(line)

    def log_shell_output(self, line):
        self.driver.log_shell_output(line)
