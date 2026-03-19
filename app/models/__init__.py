from ..extensions import db

from sqlalchemy import event
from sqlalchemy.orm import with_loader_criteria

from .users import Users, UserProfiles
from .messages import Messages
from .exam import Questions, Results
from .game import Words


@event.listens_for(db.session, "do_orm_execute")
def _add_filtering_criteria(execute_state):
    if (execute_state.is_select and not execute_state.is_column_load and not execute_state.execution_options.get("include_deleted", False)):

        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(Users, lambda cls: cls.status == "active", include_aliases=True)
        )


# This query will ignore the global filter and show everyone

# all_users = db.session.execute(
#     db.select(Users).execution_options(include_deleted=True)
# ).scalars().all()