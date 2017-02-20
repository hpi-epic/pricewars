INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('1u1yKThClnz/YhCO25bOgs2TPfsZ+Mdd8SA9EIZVSS0=', 
	 'mNq3VfVIs5gNES1EB6MsKhiNCL7h32zpPqsvWNDPStmhNnvYtIRE0BbCViuYktOA', 
	 'http://merchant-simple-competition-logic2:5002', 
	 'Competition Logic 2', 
	 'Simple') 
ON CONFLICT DO NOTHING;
