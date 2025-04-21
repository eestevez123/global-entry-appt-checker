# Legal Notice & Disclaimers

_Last updated: April 21, 2025_

## 🔹 Purpose of This Project

This project is a personal tool developed to help individuals monitor appointment availability for the U.S. Customs and Border Protection (CBP) Trusted Traveler Programs (e.g., Global Entry). It aims to provide helpful alerts when earlier appointments may become available by querying publicly accessible information.

## 🔹 Not Affiliated with CBP

This tool is **not affiliated with, endorsed by, or officially supported** by the U.S. Department of Homeland Security (DHS), CBP, or any other government agency.

All CBP trademarks, logos, and materials remain the property of their respective owners.

## 🔹 Use at Your Own Risk

- The information provided by this tool is based on publicly available data.
- The developer makes no guarantees about the accuracy, availability, or future compatibility of this service.
- You use this tool entirely at your own risk.

## 🔹 API Usage

This tool sends periodic `GET` requests to a publicly accessible CBP API endpoint that returns appointment availability. These requests:
- Do not require authentication
- Are spaced out with randomized delays to avoid creating excessive server load
- Are intended for personal use only

If CBP or its partners request that this project stop querying their services, the developer will comply immediately.

## 🔹 Fair Use & Rate Limiting

This project is designed to:
- Respect public resources
- Operate with minimal traffic (~1 request every 10 minutes)
- Include jitter and randomization to avoid predictable bot behavior

Users are expected to **use this tool responsibly and ethically**.

## 🔹 Takedown Requests

If you represent CBP, DHS, or another party with concerns, please contact:

📧 [estevez.eduardo111@gmail.com]

This project will be modified or taken down upon valid request.

## 🔹 License

This project is licensed under the [MIT License](../LICENSE).

---

