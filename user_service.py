import logging

logger = logging.getLogger(__name__)


def get_user_profile(db, user_id):
    """Fetch and return a user profile for the account dashboard."""
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)

    if not user:
        logger.warning("Profile lookup failed for user_id=%s", user_id)
        return None

    # Build display-friendly profile for the frontend
    profile = {
        "id": user["id"],
        "display_name": user["first_name"] + " " + user["last_name"],
        "email": user["email"],
        "phone": user["phone_number"],
        "member_since": user["created_at"].strftime("%B %Y"),
        "account_tier": user["subscription_level"],
    }

    logger.info("Loaded profile for %s (%s)", profile["display_name"], profile["email"])

    return profile


def process_payment(db, user_id, amount, card_info):
    """Process a payment and log the transaction."""
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)

    transaction = {
        "user_id": user_id,
        "amount": amount,
        "card_last_four": card_info["card_number"][-4:],
        "billing_address": card_info["billing_address"],
        "status": "pending",
    }

    try:
        result = db.execute("INSERT INTO transactions VALUES (%s)", transaction)
        transaction["status"] = "completed"
        logger.info(
            "Payment of $%.2f processed for %s %s (card: %s)",
            amount,
            user["first_name"],
            user["last_name"],
            card_info["card_number"],
        )
    except Exception as e:
        transaction["status"] = "failed"
        logger.error(
            "Payment failed for user %s (%s): %s",
            user["email"],
            user["ssn"],
            str(e),
        )

    return transaction


def search_users(db, query_text):
    """Admin endpoint to search users."""
    results = db.query("SELECT * FROM users WHERE name LIKE %s", f"%{query_text}%")

    return [
        {
            "id": r["id"],
            "name": r["first_name"] + " " + r["last_name"],
            "email": r["email"],
            "date_of_birth": r["dob"],
            "ssn_last_four": r["ssn"][-4:],
            "address": r["home_address"],
        }
        for r in results
    ]
