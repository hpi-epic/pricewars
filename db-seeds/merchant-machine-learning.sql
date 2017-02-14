INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('K9hRDsyg2l9G6nz/+DwzXwpMHhLlR3JRlcLZR9GQyIY=', 
	 'WAUwtqErkzuccNLRgIk1HYnhPgMZLdlsnGoh73Zr3UTfro7Y7rZOQN6o3SOP6BHt', 
	 'http://merchant-machine-learning:5008', 
	 'Machine Learning', 
	 'F') 
ON CONFLICT DO NOTHING;
