from enum import StrEnum


class InternalRole(StrEnum):
    CONTRACT_MANAGER = "Contract Manager"
    SUPER_USER = "Super User"


class ExternalRole(StrEnum):
    CASE_WORKER = "Case Worker"
    OPERATOR_MANAGER = "Operator Manager"


# Internal roles set for easy access in auth
INTERNAL_ROLES = {role.value for role in InternalRole}
ALLOWED_OFFICE_CODE = ["001"]
