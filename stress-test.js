import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '1m', target: 50 },  // Ramp-up to 50 users
    { duration: '3m', target: 100 }, // Hold at 100 users
    { duration: '1m', target: 0 },   // Ramp-down
  ],
};

export default function () {
  let payload = JSON.stringify({ long_url: "https://example.com" });

  let params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  let res = http.post('http://short.local/shorten', payload, params);

  check(res, { 'status is 200': (r) => r.status === 200 });

  sleep(1);
}
