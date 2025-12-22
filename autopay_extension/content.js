// AutoPay Tracker - Real checkout detector + card scraper
console.log("AutoPay content script loaded on", window.location.href);

function isCheckoutPage() {
  const url = window.location.href.toLowerCase();
  const checkoutPatterns = [
    // URL patterns
    'checkout', 'payment', 'billing', 'subscribe', 'purchase', 'order', 'cart',
    '/pay/', '/charge/', '/buy/', '/upgrade/',
    // Popular payment processors
    'stripe.com/pay', 'paypal.com/checkout', 'squareup.com/pay'
  ];
  return checkoutPatterns.some(pattern => url.includes(pattern));
}

function detectIssuer(cardNumber) {
  const firstDigit = cardNumber[0];
  if (firstDigit === '4') return 'VISA';
  if (firstDigit === '5') return 'MASTERCARD';
  if (firstDigit === '3') return 'AMEX';
  return 'UNKNOWN';
}

function detectCardDetails() {
  const selectors = {
    cardNumber: [
      'input[data-stripe="cardNumber"]',           // Stripe Elements
      '#cardNumber, #card-number, #cardnumber',    // Common IDs
      'input[name="card_number"], input[name="cardNumber"]', // Form names
      'input[placeholder*="card"], input[placeholder*="Card"]', // Placeholders
      '[data-testid="card-number"]',              // React/Testing
      '.CardNumberInput input',                   // Custom classes
      'iframe[src*="stripe"] ~ input'             // Stripe iframes
    ],
    cardholder: [
      'input[name="name"], input[name="cardholder"]',
      '#name, #cardholder-name',
      'input[placeholder*="name"], input[placeholder*="Name"]'
    ],
    amount: [
      '.total-amount, .order-total, #total',
      '[data-testid="total"], .payment-total',
      '.amount, .price'
    ]
  };

  // Try to find filled card number
  for (const selector of selectors.cardNumber) {
    const input = document.querySelector(selector);
    if (input?.value && input.value.replace(/\s/g, '').length >= 13) {
      const cardNumber = input.value.replace(/\s/g, '');
      const cardholderInput = document.querySelector(selectors.cardholder.join(','));
      
      return {
        name: cardholderInput?.value || "My Card",
        last4: cardNumber.slice(-4),
        issuer: detectIssuer(cardNumber)
      };
    }
  }
  return null;
}

function detectSubscriptionDetails() {
  const url = window.location.href;
  let serviceName = new URL(url).hostname.replace('www.', '');
  
  // Try to find service name/amount
  const title = document.title.toLowerCase();
  const amountMatch = document.querySelector('.total-amount, .order-total, #total')?.textContent.match(/\$?([\d,.]+)/);
  
  return {
    service_name: serviceName,
    service_url: url,
    amount: parseFloat(amountMatch?.[1] || '9.99'),
    frequency: title.includes('monthly') ? 'monthly' : 'yearly'
  };
}

// MAIN LOGIC - Only run on checkout pages with card details
if (isCheckoutPage()) {
  console.log("✅ Checkout page detected:", window.location.href);
  
  const cardDetails = detectCardDetails();
  if (cardDetails) {
    console.log("✅ Card found:", cardDetails);
    
    const subscriptionDetails = detectSubscriptionDetails();
    
    // Send to Django API
    Promise.all([
      fetch("http://127.0.0.1:8000/api/cards/add/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cardDetails)
      }),
      fetch("http://127.0.0.1:8000/api/subscriptions/add/", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(subscriptionDetails)
      })
    ])
    .then(([cardRes, subRes]) => {
      if (cardRes.ok && subRes.ok) {
        alert("✅ Saved to AutoPay Tracker dashboard!");
        console.log("✅ Saved to AutoPay Tracker!");
      } else {
        console.error("❌ API error:", cardRes.status, subRes.status);
      }
    })
    .catch(err => console.error("❌ Network error:", err));
  } else {
    console.log("ℹ️ No card details found yet - fill in card number and try again");
  }
} else {
  console.log("ℹ️ Not a checkout page");
}
