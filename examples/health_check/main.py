from http import HTTPStatus
from typing import Literal

import requests

ENVS = {
    "staging": "backend-staging.usummitapp.com",
    "dev": "backend-dev.usummitapp.com",
}

SERVICES = ["Cache", "Database", "Email"]
HEALTH_CHECK_URL_TEMPLATE = (
    "https://{domain}/api/v1/utils/health-check/?{check_params}"
)
REQUEST_TIMEOUT = 20


class NotAvailableEnvException(Exception):
    """Env is not available.

    This error is raised if some environment variable is not available.

    Args:
        env: not available variable name.

    """

    def __init__(self, env: str):
        super().__init__(f"{env} environment is not available.")


class HealthCheckError(Exception):
    """Health check error.

    This error is raised if health check went wrong.

    Args:
        errors: errors description.

    """

    def __init__(self, errors: str = "Unknown"):
        super().__init__(f"HealthCheck: {errors} errors")


def main(env: str) -> Literal["HealthCheck: ok"]:
    """Run development sites health-checks.

    This function goes to a corresponding env site, gets current health checks
    state.

    Raises:
        NotAvailableEnvException: Env is not available.
        HTTPError: HTTP Response error.
        HealthCheckError: Health check error.

    """
    print(f"Env: {env}")

    domain = ENVS.get(env)
    if domain is None:
        raise NotAvailableEnvException(env)

    check_params = "&".join(
        f"checks={service}" for service in SERVICES
    )
    health_check_url = HEALTH_CHECK_URL_TEMPLATE.format(
        domain=domain,
        check_params=check_params,
    )

    http_response = requests.get(health_check_url, timeout=REQUEST_TIMEOUT)
    status_code = http_response.status_code

    if status_code != HTTPStatus.OK:
        print(f"Env: {env} error (unknown) [{status_code}] status")
        http_response.raise_for_status()

    services_status: dict[str, str] = http_response.json()
    print(f"Health check: status {status_code}, content: {services_status}")

    errors = [
        service for service, status in services_status.items()
        if status != "OK"
    ]
    if errors:
        formatted_errors: str = ", ".join(errors)
        print(f"Env: {env} error - {formatted_errors}")
        raise HealthCheckError(formatted_errors)

    print(f"Env: {env} success - {services_status}")
    return "HealthCheck: ok"


if __name__ == "__main__":
    main("staging")
