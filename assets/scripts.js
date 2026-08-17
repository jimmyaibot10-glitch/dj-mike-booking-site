const bookingForm = document.querySelector('#bookingForm');
const inquiryOutput = document.querySelector('#inquiryOutput');

const eventTierLabels = {
  'Backyard / house party': 'Starter tier — lower-budget casual setup',
  'Birthday / private party': 'Standard tier — private party setup',
  Wedding: 'Premium tier — timeline and MC support',
  'Corporate / formal event': 'Custom tier — professional event quote',
  Other: 'Custom tier — details required'
};

function formatInquiry(formData) {
  const eventType = formData.get('eventType');
  return [
    'DJ Mike booking inquiry',
    '------------------------',
    `Name: ${formData.get('name')}`,
    `Contact: ${formData.get('contact')}`,
    `Event type: ${eventType}`,
    `Suggested tier: ${eventTierLabels[eventType] || 'Custom tier'}`,
    `Date: ${formData.get('date')}`,
    `Start time: ${formData.get('time')}`,
    `Location: ${formData.get('location') || 'Not provided'}`,
    '',
    'Details:',
    formData.get('details') || 'No extra details provided yet.',
    '',
    'Next step: connect this form to email, Google Calendar, Calendly/TidyCal, or a small backend.'
  ].join('\n');
}

function storeInquiry(summary) {
  const saved = JSON.parse(localStorage.getItem('dj_mike_booking_inquiries') || '[]');
  saved.unshift({ createdAt: new Date().toISOString(), summary });
  localStorage.setItem('dj_mike_booking_inquiries', JSON.stringify(saved.slice(0, 20)));
}

bookingForm?.addEventListener('submit', event => {
  event.preventDefault();
  const formData = new FormData(bookingForm);
  const summary = formatInquiry(formData);
  storeInquiry(summary);
  inquiryOutput.hidden = false;
  inquiryOutput.textContent = summary;
  inquiryOutput.scrollIntoView({ behavior: 'smooth', block: 'center' });
});
