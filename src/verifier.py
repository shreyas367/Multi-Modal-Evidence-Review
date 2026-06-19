def determine_status(
    claim_issue,
    image_issue,
    evidence_met
):
    if not evidence_met:
        return (
            "not_enough_information",
            "claimed part not visible"
        )

    if image_issue == "none":
        return (
            "contradicted",
            "no visible damage found"
        )

    if image_issue == "unknown":
        return (
            "not_enough_information",
            "unable to determine visible damage"
        )

    if (
        image_issue == claim_issue
        and image_issue != "unknown"
    ):
        return (
            "supported",
            "image evidence matches claim"
        )

    return (
        "contradicted",
        "visible damage differs from claim"
    )

def build_risk_flags(history_row):
    flags = []
    try:
        if history_row["rejected_claim"] >= 3:
            flags.append(
                "user_history_risk"
            )
        if history_row["manual_review_claim"] >= 2:
            flags.append(
                "manual_review_required"
            )
    except:
        pass

    if not flags:
        return "none"

    return ";".join(flags)
