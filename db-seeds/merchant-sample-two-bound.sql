INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('9A3CHpwf97TY4X6F+rDKcgirVfXZQ1HebiyDQQf4LVo=', 
	 'EGkdMWbvFuVy9w7ReCExgOiyoxr6RyFfF0JbXuXmp4ly1sRf5fdl4MjsKbylbERq', 
	 'http://merchant-sample-two-bound:5006', 
	 'Two Bound', 
	 'D') 
ON CONFLICT DO NOTHING;
