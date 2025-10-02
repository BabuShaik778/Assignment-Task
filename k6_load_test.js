

import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 200,      // virtual users per instance - scale horizontally to hit 50k RPS
  duration: '60s',
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500']
  }
};

export default function () {
  // obtain token once per VU ideally; keeping simple here
  let tokenRes = http.post('http://HOST:8000/token');
  let token = tokenRes.json('access_token');
  let headers = { Authorization: `Bearer ${token}` };
  let res = http.get('http://HOST:8000/proxy/data', { headers });
  check(res, { 'status is 200': (r) => r.status === 200 });
}
