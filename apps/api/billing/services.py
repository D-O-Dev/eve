def enabled_modules(company) -> set[str]:
    subscription = getattr(company, "subscription", None)
    if subscription is None or not subscription.is_in_effect():
        return set()
    return set(subscription.plan.modules.values_list("module_code", flat=True))