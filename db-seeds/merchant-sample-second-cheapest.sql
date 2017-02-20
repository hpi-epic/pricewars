INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('QXY044ASodJNz37NG1aXMPZiz3ZOdJerSRZ5LT2HGRk=', 
	 'Qrlo6DEkG9SXNIjCByXklvpjbkbQC4scveS2rfm8oEfCWPNhOuSAqIsS4UtGYmsU', 
	 'http://merchant-sample-second-cheapest:5004', 
	 'Second Cheapest', 
	 'B') 
ON CONFLICT DO NOTHING;
