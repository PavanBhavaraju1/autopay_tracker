document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('saveForm');
  const statusBtns = document.querySelectorAll('.status-btn');
  let selectedStatus = 'auto';

  // Status button toggle
  statusBtns.forEach(btn => {
    btn.onclick = () => {
      statusBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedStatus = btn.dataset.status;
    };
  });

  // Pre-fill from page title
  document.getElementById('service_name').value = document.title.split(' - ')[0] || '';
  document.getElementById('next_billing_date').valueAsDate = new Date();

  form.onsubmit = async (e) => {
    e.preventDefault();
    
    const data = {
      service_name: document.getElementById('service_name').value,
      amount: parseFloat(document.getElementById('amount').value),
      card_name: document.getElementById('card_name').value,
      card_last4: document.getElementById('card_last4').value,
      next_billing_date: document.getElementById('next_billing_date').value,
      status: selectedStatus
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/popup-subscription/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        alert('✅ Saved to AutoPay Tracker!');
        window.close();
      } else {
        alert('❌ Error: Server not running or need to login first');
      }
    } catch (e) {
      alert('❌ AutoPay Tracker not running on localhost:8000');
    }
  };

  document.getElementById('cancel').onclick = () => window.close();
});
