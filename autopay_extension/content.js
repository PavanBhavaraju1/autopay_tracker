// Auto-show popup on payment confirmation pages
if (window.location.hostname.includes('netflix.com') || 
    window.location.hostname.includes('amazon.com') ||
    window.location.hostname.includes('spotify.com')) {
  
  // Look for payment confirmation signals
  const paymentSelectors = [
    '[data-uia="payment-method"]',
    '.payment-method',
    '[aria-label*="payment"]',
    '.billing-info',
    '[data-testid="payment-confirmation"]'
  ];

  paymentSelectors.forEach(selector => {
    if (document.querySelector(selector)) {
      setTimeout(() => {
        chrome.runtime.sendMessage({action: "showPopup"});
      }, 2000);
    }
  });
}
