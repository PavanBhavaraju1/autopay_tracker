const BASE_URL = "http://127.0.0.1:8000";  // change to Render URL in production

// Listen for messages from content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "SAVE_AUTOPAY") {
    saveToAutopay(message.payload).then(sendResponse);
    return true; // keep channel open for async response
  }
});

// Save card + subscription into Django
async function saveToAutopay(payload) {
  try {
    // 1) Create card first (if provided)
    let cardId = null;

    if (payload.card) {
      const cardResp = await fetch(`${BASE_URL}/api/cards/add/`, {
        method: "POST",
        credentials: "include",           // send cookies (for logged-in user)
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: payload.card.name,        // e.g. "Netflix Card"
          last4: payload.card.last4,      // "4242"
          issuer: payload.card.issuer,    // "VISA"
          is_active: true
        })
      });

      if (!cardResp.ok) {
        console.error("Card create failed:", await cardResp.text());
        return { ok: false, step: "card" };
      }

      const cardData = await cardResp.json();
      cardId = cardData.id;
    }

    // 2) Create subscription using that card
    const subResp = await fetch(`${BASE_URL}/api/subscriptions/add/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        service_name: payload.service_name,           // "Netflix"
        amount: payload.amount,                       // 9.99
        billing_cycle_days: payload.billing_cycle_days, // 30
        next_billing_date: payload.next_billing_date, // "2025-01-01"
        status: payload.status || "upcoming",
        card_id: cardId
      })
    });

    if (!subResp.ok) {
      console.error("Subscription create failed:", await subResp.text());
      return { ok: false, step: "subscription" };
    }

    return { ok: true };
  } catch (err) {
    console.error("Error saving to AutoPay:", err);
    return { ok: false, step: "exception" };
  }
}
