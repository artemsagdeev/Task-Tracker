from api.enums import TaskStatus, UserRole

ALLOWED_TRANSITIONS = {
    UserRole.MANAGER: {
        TaskStatus.OPEN: [
            TaskStatus.SELECTED,
            TaskStatus.CLOSED,
        ],
        TaskStatus.SELECTED: [
            TaskStatus.CLOSED,
        ],
        TaskStatus.IN_PROGRESS: [
            TaskStatus.SELECTED,
            TaskStatus.CLOSED,
        ],
        TaskStatus.READY_TO_ACCEPTANCE: [
            TaskStatus.IN_PROGRESS,
            TaskStatus.CLOSED,
        ],
    },
    UserRole.DEVELOPER: {
        TaskStatus.SELECTED: [
            TaskStatus.IN_PROGRESS,
        ],
        TaskStatus.IN_PROGRESS: [
            TaskStatus.READY_TO_ACCEPTANCE,
            TaskStatus.SELECTED,
        ],
        TaskStatus.READY_TO_ACCEPTANCE: [
            TaskStatus.IN_PROGRESS,
        ],
    },
}

def can_change_status(*, role, from_status, to_status):
    return to_status in ALLOWED_TRANSITIONS.get(role, {}).get(from_status, [])