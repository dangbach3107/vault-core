from backend.demo_case import DOCUMENTS, LABEL, Demo, make_pdf


def test_full_case_runs_through_the_api_one_role_at_a_time(client):
    demo = Demo(client, "vault-demo")
    result = demo.run()
    deal = demo.call("admin", "GET", f'/deals/{result["deal"]}')
    state = deal["state"]
    assert all(state["steps"].values()) and state["signing"]["status"] == "SIGNED" and state["closing"]["status"] == "CLOSED"
    assert LABEL in deal["title"] and state["is_sample"] is False  # labelled by name; never via the sample shortcut
    assert {fee["status"] for fee in state["fees"]} == {"PARTIALLY_PAID", "OVERDUE", "INVOICED"}
    assert [f["status"] for f in state["tech_dd"]["findings"]] == ["ACCEPTED_RISK", "RESOLVED"]
    assert state["tech_dd"]["signed_off_by"] == "tech" and state["handoff"]["status"] == "HANDED_OFF"

    # Each role sees only its own part of the same deal.
    buyer = demo.call("buyer", "GET", f'/deals/{result["deal"]}')["state"]
    assert "fees" not in buyer and "tech_dd" not in buyer and buyer["nda"]["reference"].startswith("NDA-")
    assert demo.call("buyer2", "GET", "/deals") == []
    files = demo.call("buyer", "GET", f'/deals/{result["deal"]}/documents')
    assert sorted(item["title"] for item in files) == sorted(f"{title} ({LABEL})" for _, title, _, _ in DOCUMENTS if title in {"Báo cáo tài chính 2025", "Kiến trúc hệ thống"})
    assert all(item["can_download"] is False for item in files)
    evidence = demo.call("finance", "GET", f'/deals/{result["deal"]}/closing-evidence')
    assert {item["action"] for item in evidence} == {"legalClosingChecklist", "spaSigned"}
    assert "tech_dd" not in demo.call("finance", "GET", f'/deals/{result["deal"]}')["state"]

    # Verification came from the reviewer, with evidence, and shows in the profile and the teaser counts.
    company = demo.call("seller", "GET", f'/companies/{result["company"]}')
    assert company["profile"]["tax_id"]["verification"] == "DOCUMENT_VERIFIED" and company["profile"]["tax_id"]["reviewed_by"] == "legal"
    summary = next(row for row in demo.call("seller", "GET", "/companies") if row["id"] == result["company"])
    assert summary["verified_facts_count"] == 2


def test_demo_documents_have_distinct_content():
    contents = {make_pdf(title, lines) for _, title, _, lines in DOCUMENTS}
    assert len(contents) == len(DOCUMENTS)
