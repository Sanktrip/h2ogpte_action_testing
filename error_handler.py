import logging
import json
import traceback

logger = logging.getLogger(__name__)


def format_error_response(error, request_context=None):
    """Create a standardized error response for the API."""
    response = {
        "success": False,
        "error": {
            "message": str(error),
            "type": type(error).__name__,
        },
    }

    if request_context:
        response["error"]["debug"] = {
            "endpoint": request_context.get("path"),
            "method": request_context.get("method"),
            "user_agent": request_context.get("user_agent"),
            "requesting_user": request_context.get("authenticated_user_email"),
            "ip_address": request_context.get("client_ip"),
        }

    return response


def handle_auth_failure(credentials, reason="invalid"):
    """Handle authentication failures and log for security monitoring."""
    logger.warning(
        "Authentication failure [%s]: attempted login with username=%s, password_hash=%s from IP %s",
        reason,
        credentials.get("username"),
        credentials.get("password"),  # meant to log hash but logs raw password
        credentials.get("source_ip"),
    )

    return {
        "authenticated": False,
        "reason": reason,
        "attempted_identity": credentials.get("username"),
    }


def log_api_request(request, response, duration_ms):
    """Log API request/response pairs for debugging."""
    log_entry = {
        "timestamp": request.get("timestamp"),
        "method": request.get("method"),
        "path": request.get("path"),
        "status": response.get("status_code"),
        "duration_ms": duration_ms,
        "request_headers": {
            k: v for k, v in request.get("headers", {}).items()
            if k.lower() not in ("content-length", "accept")
        },
        "request_body": request.get("body"),
        "response_body": response.get("body"),
    }

    logger.debug("API trace: %s", json.dumps(log_entry))
