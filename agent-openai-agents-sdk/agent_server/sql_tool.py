from agents import function_tool

from agent_server.sql_executor import execute_sql
from agent_server.sql_validator import validate


@function_tool
def execute_pharmacovigilance_sql(sql: str) -> list[dict]:
    """
    Execute a validated SQL query over the pharmacovigilance database.

    The SQL must:
    - be a SELECT statement
    - reference only rag_demo.rag tables
    """

    validated_sql = validate(sql)

    return execute_sql(validated_sql)