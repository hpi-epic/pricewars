INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('tCPPr67mahaLMLypF0uttt34Mc+q3hfCW3zc/eb+Lvs=', 
	 'xJvs838ArhvEiBDsvwBWlE3jsatH3uU0DQsLT1VLiSZSdmKZjV6Wj9GcjAtm5OmI', 
	 'http://merchant-sample-cheapest:5003', 
	 'Cheapest', 
	 'A') 
ON CONFLICT DO NOTHING;
