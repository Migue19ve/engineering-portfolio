'use strict';
const $ = (id) => document.getElementById(id);
function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
async function api(path, payload) {
  const response = await fetch(path, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'The demo could not complete this request.');
  return data;
}
document.querySelectorAll('[data-demo]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-demo]').forEach(tab => {
    const selected = tab === button;
    tab.classList.toggle('active', selected);
    tab.setAttribute('aria-pressed', String(selected));
    $(tab.dataset.demo).hidden = !selected;
  });
}));
$('run-events').addEventListener('click', async () => {
  const button = $('run-events');
  button.disabled = true;
  try {
    const data = await api('/api/events', {});
    $('event-deliveries').textContent = data.deliveries;
    $('event-writes').textContent = data.writes;
    $('event-revision').textContent = data.state.revision;
    $('event-state').textContent = data.state.value + ' · one final record';
    $('event-log').replaceChildren();
    data.log.forEach((event, i) => {
      const row = el('div', undefined, 'event-row');
      row.append(el('span', String(i + 1).padStart(2, '0'), 'step'), el('span', event.event, 'event-id'), el('span', event.detail), el('span', event.status, 'badge ' + event.status));
      $('event-log').append(row);
    });
    button.replaceChildren(document.createTextNode('Replay scenario '), el('span', '↻'));
  } catch (error) { $('event-log').replaceChildren(el('p', error.message, 'error')); }
  finally { button.disabled = false; }
});
let validQuote = null;
function invalidateQuote() {
  validQuote = null;
  $('export-quote').disabled = true;
  $('quote-status').textContent = 'Input changed — validate again';
  $('quote-total').textContent = '—';
  $('quote-results').replaceChildren(el('p', 'Validate the current input to refresh this preview.', 'help'));
  $('quote-error').textContent = '';
}
$('csv-input').addEventListener('input', invalidateQuote);
$('load-clean').addEventListener('click', () => {
  $('csv-input').value = 'sku,quantity,unit_price\nKITE-01,3,49.90\nMOSS-02,2,18.75\nLUMA-03,1,79.00';
  invalidateQuote();
});
$('validate-csv').addEventListener('click', async () => {
  const button = $('validate-csv');
  const input = $('csv-input').value;
  button.disabled = true;
  invalidateQuote();
  try {
    const data = await api('/api/quote', {csv: input});
    // Never export a response belonging to input that changed in flight.
    if ($('csv-input').value !== input) return;
    $('quote-results').replaceChildren();
    $('quote-status').textContent = `${data.valid_rows} valid · ${data.invalid_rows} need review`;
    $('quote-total').textContent = '$' + data.valid_subtotal;
    data.rows.forEach(row => {
      const invalid = row.errors.length > 0;
      const wrap = el('div', undefined, 'quote-line');
      const title = el('div');
      title.append(el('span', invalid ? '!' : '✓', 'row-icon' + (invalid ? ' bad' : '')), el('b', row.name), el('span', invalid ? 'Review' : '$' + row.subtotal, 'amount'));
      wrap.append(title, el('small', `Line ${row.line} · ${row.sku} · Qty ${row.quantity}`));
      row.errors.forEach(error => wrap.append(el('small', error, 'issue')));
      $('quote-results').append(wrap);
    });
    validQuote = data.export_ready ? data : null;
    $('export-quote').disabled = !validQuote;
  } catch (error) { if ($('csv-input').value === input) $('quote-error').textContent = error.message; }
  finally { button.disabled = false; }
});
$('export-quote').addEventListener('click', () => {
  if (!validQuote) return;
  const blob = new Blob([JSON.stringify(validQuote, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const link = el('a');
  link.href = url; link.download = 'synthetic-quote.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
document.querySelectorAll('[data-prompt]').forEach(button => button.addEventListener('click', () => {
  $('question').value = button.dataset.prompt;
  $('assistant-form').requestSubmit();
}));
let queryVersion = 0;
$('question').addEventListener('input', () => {
  queryVersion++;
  $('answer').textContent = 'Question changed — run again to refresh the answer.';
  $('assistant-error').textContent = '';
  $('order-cards').replaceChildren();
  $('tool-trace').replaceChildren();
});
$('assistant-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const version = ++queryVersion;
  $('assistant-error').textContent = '';
  $('answer').textContent = 'Reading fictional records…';
  $('order-cards').replaceChildren(); $('tool-trace').replaceChildren();
  try {
    const data = await api('/api/assistant', {query: $('question').value});
    if (version !== queryVersion) return;
    $('answer').textContent = data.answer;
    data.records.forEach(record => {
      const card = el('div', undefined, 'order-card');
      const title = el('div');
      title.append(el('b', record.id), el('span', record.status, 'badge ' + record.status));
      card.append(title, el('p', `${record.customer} · ${record.items} items`));
      if (record.reason) card.append(el('p', record.reason));
      $('order-cards').append(card);
    });
    data.trace.forEach((step, i) => {
      const row = el('div', undefined, 'trace-step'); const detail = el('div');
      detail.append(el('b', step.tool), el('span', step.status, 'badge ' + step.status), el('p', step.detail));
      row.append(el('span', String(i + 1).padStart(2, '0')), detail); $('tool-trace').append(row);
    });
  } catch (error) {
    if (version === queryVersion) { $('answer').textContent = 'No answer generated.'; $('assistant-error').textContent = error.message; }
  }
});
