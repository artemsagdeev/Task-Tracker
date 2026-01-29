def apply_task_filters(queryset, filters):

    status = filters.get('status')
    if status:
        queryset = queryset.filter(status=status)

    priority = filters.get('priority')
    if priority:
        queryset = queryset.filter(priority=priority)

    return queryset
