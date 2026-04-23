# Agent API Terms of Service

**Publisher:** xuanxue.app (Oslov Technology Pty Ltd)  
**Contact:** oslovtech@gmail.com  
**Last updated:** 2026-04-23

---

## 1. Nature of the Service

The xuanxue BaZi Matching API ("Agent API") delivers Chinese BaZi (八字) compatibility analysis programmatically. All output is provided for **entertainment and cultural exploration purposes only**. It is not a substitute for professional relationship counseling, psychological advice, matrimonial services, or any other professional advisory service.

## 2. Payment

- Each API call costs **$0.02 USD equivalent in USDC** on the Base L2 network, paid via the x402 protocol.
- Payments are processed on-chain. We do not issue refunds for completed on-chain transactions except where required by applicable law.
- Recipient address: `0xcb99bf3d45d5f8bdeb72d00792fe77dffed2c6de`

## 3. Privacy — No PII Stored

Birth data submitted in API requests is used solely for **in-memory computation** and is **never persisted to disk in identifiable form**. Our transaction log stores only:

- SHA-256 hash of the request payload (`request_hash`)
- On-chain transaction hash
- Wallet address (`from_addr`)
- User-Agent string (truncated to 256 characters)
- Endpoint path and UTC timestamp

No name, email, or unencrypted birth date is written to any database.

## 4. Calling Party Responsibilities

If you are an AI agent or application developer calling this API on behalf of end users, you are responsible for:

1. Ensuring you have a **lawful basis** to process and transmit the birth data of any person whose data you submit (consent, legitimate interest, or equivalent under GDPR, CCPA, or applicable local law).
2. **Informing end users** that their birth data will be sent to a third-party API (xuanxue.app) for analysis.
3. Not submitting birth data of **minors** without appropriate parental or guardian consent.
4. Not using API output as the **sole basis for consequential decisions** (hiring, lending, medical, legal, matrimonial screening, etc.).

## 5. Acceptable Use

You agree **not** to:

- Reverse-engineer, resell, or misrepresent the API or its output.
- Submit fictitious or maliciously-crafted data intended to trigger errors or abuse rate limits.
- Frame outputs as scientific fact, medical diagnosis, or professional advice to end users.
- Use the API for any unlawful purpose.

## 6. GDPR / CCPA Compliance

We process submitted birth data as a **data processor** acting on your instructions (as data controller). Processing is limited to in-memory computation; no personal data is retained after the response is returned. You remain the data controller responsible for obtaining lawful consent from data subjects. For CCPA purposes, we do not sell personal information.

## 7. Disclaimer of Warranties

The Agent API is provided "as is" without warranties of any kind. Compatibility scores are heuristic outputs based on traditional Chinese metaphysical principles; they carry no statistical or scientific validity.

## 8. Limitation of Liability

To the maximum extent permitted by law, our total liability for any claim related to the Agent API is capped at the amount paid for the specific API call giving rise to the claim.

## 9. Governing Law

These Terms are governed by the laws of New South Wales, Australia.

## 10. Contact

Questions? Email **oslovtech@gmail.com**.
