from databricks.sdk import WorkspaceClient
from databricks.sdk.service import sql

from agent_server.config import WAREHOUSE_ID

w = WorkspaceClient()


def execute_sql(sql_text: str) -> list[dict]:
    """
    Execute SQL against the configured SQL Warehouse
    and return the results as a list of dictionaries.
    """

    response = w.statement_execution.execute_statement(
        warehouse_id=WAREHOUSE_ID,
        statement=sql_text,
        wait_timeout="30s",
        disposition=sql.Disposition.INLINE,
        format=sql.Format.JSON_ARRAY,
    )

    # Check execution status
    if response.status is None or response.status.state != sql.StatementState.SUCCEEDED:
        error = (
            response.status.error.message
            if response.status and response.status.error
            else "Unknown SQL execution error."
        )
        raise RuntimeError(error)

    if response.result is None or response.manifest is None:
        return []

    # Extract column names
    columns = [
        column.name
        for column in response.manifest.schema.columns
    ]

    # Convert rows into dictionaries
    rows = []

    for row in response.result.data_array:
        rows.append(dict(zip(columns, row)))

    return rows