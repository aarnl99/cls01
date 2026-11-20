// Posts every new website form entry (quotes, government requests, job applications)
// to the CLS Slack channel through an incoming webhook.
// The webhook URL lives only in the SLACK_WEBHOOK_URL environment variable in Netlify.

const TITLES = {
  'corporate-quote': 'Corporate quote',
  'charter-quote': 'Charter quote',
  'government-request': 'Government request',
  'job-application': 'Job application',
};

const LABELS = {
  name: 'Name', first_name: 'First name', last_name: 'Last name', role: 'Role',
  email: 'Email', phone: 'Phone', company: 'Company', company_size: 'Company size',
  need: 'Needs', office_location: 'Office location', riders: 'Riders / group size',
  start_date: 'Start date', occasion: 'Occasion', event_date: 'Event date',
  group_size: 'Group size', pickup: 'Pickup', dropoff: 'Drop-off', vehicle: 'Vehicle',
  agency: 'Agency', program_type: 'Program type', position: 'Position',
  location: 'Preferred location', license_class: 'License class',
  notes: 'Notes', message: 'Message', about: 'About them',
};

const SKIP = new Set(['form-name', 'form_label', 'bot-field', 'ip', 'user_agent', 'referrer', 'subject']);

const esc = (v) => String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function buildMessage(data, formName) {
  const title = data.form_label || TITLES[formName] || 'Website form';
  const lines = [];
  for (const [key, value] of Object.entries(data)) {
    if (SKIP.has(key) || value == null || String(value).trim() === '') continue;
    const label = LABELS[key] || key.replace(/_/g, ' ');
    lines.push(`*${esc(label)}:* ${esc(String(value).trim())}`);
  }
  const who = data.company || data.agency || [data.first_name, data.last_name].filter(Boolean).join(' ') || data.name || '';
  const header = `:inbox_tray: *New ${esc(title)}*${who ? ` from ${esc(who)}` : ''}`;
  return {
    text: `New ${esc(title)}${who ? ` from ${esc(who)}` : ''}`,
    blocks: [
      { type: 'section', text: { type: 'mrkdwn', text: header } },
      { type: 'section', text: { type: 'mrkdwn', text: lines.join('\n').slice(0, 2900) || '_No details filled in_' } },
    ],
  };
}

export default {
  async formSubmitted(event) {
    const url = (globalThis.Netlify?.env?.get('SLACK_WEBHOOK_URL')) || process.env.SLACK_WEBHOOK_URL;
    if (!url) {
      console.log('SLACK_WEBHOOK_URL is not set, skipping Slack post');
      return;
    }
    const data = event?.data || {};
    const formName = data['form-name'] || event?.form?.name || event?.formName || '';
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildMessage(data, formName)),
    });
    if (!res.ok) console.log('Slack post failed', res.status, await res.text());
  },
};
