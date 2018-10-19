from peewee import *
from playhouse.sqlite_ext import JSONField

from hunor.models.database import BaseModel


class Target(BaseModel):
    tid = IntegerField(null=False)
    ignore = BooleanField(null=False, default=False)
    clazz = CharField(null=False)
    method = CharField(null=False)
    type_method = CharField(null=True)
    line = IntegerField(null=False)
    column = IntegerField(null=False)
    statement = CharField(null=True)
    statement_nodes = CharField(null=True)
    context = JSONField()
    context_full = JSONField()
    method_ast = JSONField()
    operand_nodes = CharField(null=True)
    operator_kind = CharField(null=True)
    operator = CharField(null=True)
    coverage = IntegerField(null=False)

    @staticmethod
    def find_all(coverage=0):
        return Target.select(Target.coverage >= coverage)

    @staticmethod
    def find_all_by_statement(statement, coverage=0):
        return Target.select().where(
            (Target.statement.contains(statement))
            & (Target.coverage >= coverage)
        )

    @staticmethod
    def find_all_by_statement_nodes(statement_nodes, coverage=0):
        return Target.select().where(
            (Target.statement_nodes.contains(statement_nodes))
            & (Target.coverage >= coverage)
        )

    @staticmethod
    def find_all_by_operator(operator, coverage=0):
        return Target.select().where(
            (Target.operator == operator)
            & (Target.coverage >= coverage)
        )

    @staticmethod
    def find_all_by_operator_kind(operator_kind, coverage=0):
        return Target.select().where(
            (Target.operator_kind == operator_kind)
            & (Target.coverage >= coverage)
        )


def dict_to_target(d):
    target = Target()

    target.tid = d['id']
    target.ignore = d['ignore']
    target.clazz = d['class']
    target.method = d['method']
    target.type_method = d['type_method']
    target.line = d['line']
    target.column = d['column']
    target.statement = d['statement']
    target.statement_nodes = d['statement_nodes']
    target.context = d['context']
    target.context_full = d['context_full']
    target.method_ast = d['method_ast']
    target.operand_nodes = d['operand_nodes']
    target.operator_kind = d['operator_kind']
    target.operator = d['operator']

    return target
