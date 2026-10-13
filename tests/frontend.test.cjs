// Execute the actual UI handlers with a minimal DOM and controlled network timing.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');

class Element {
  constructor() { this.value = ''; this.textContent = ''; this.children = []; this.handlers = {}; }
  addEventListener(type, fn) { this.handlers[type] = fn; }
  replaceChildren(...nodes) { this.children = nodes; }
  append(...nodes) { this.children.push(...nodes); }
}
function app() {
  const elements = new Map();
  const get = id => {
    if (!elements.has(id)) elements.set(id, new Element());
    return elements.get(id);
  };
  const pending = [];
  const context = {
    document: {getElementById: get, querySelectorAll: () => [], createElement: () => new Element()},
    fetch: () => new Promise(resolve => pending.push(data => resolve({ok: true, json: async () => data}))),
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../static/app.js'), 'utf8'), context);
  return {get, pending, submit: () => get('assistant-form').handlers.submit({preventDefault() {}})};
}
const response = answer => ({answer, records: [{id: 'DEMO-1001', status: 'ready', customer: 'Fictional', items: 1}], trace: []});

test('editing an in-flight question prevents its old answer and evidence from rendering', async () => {
  const {get, pending, submit} = app();
  get('question').value = 'Show DEMO-1001';
  const request = submit();
  get('question').value = 'Which orders are blocked?';
  get('question').handlers.input();
  pending[0](response('Old answer'));
  await request;
  assert.match(get('answer').textContent, /Question changed/);
  assert.equal(get('order-cards').children.length, 0);
  assert.equal(get('tool-trace').children.length, 0);
});

test('a slower earlier submission cannot replace a newer result', async () => {
  const {get, pending, submit} = app();
  get('question').value = 'First question'; const first = submit();
  get('question').value = 'Second question'; const second = submit();
  pending[1](response('New answer')); await second;
  pending[0](response('Old answer')); await first;
  assert.equal(get('answer').textContent, 'New answer');
  assert.equal(get('order-cards').children.length, 1);
});
