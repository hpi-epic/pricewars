INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('sUhXcAaoweY4NmRNNrAVPDXB35boelfuH/DNb8TnrNw=', 
	 'j9Vhr9yfTihurnfIXfiiT9NqvdCsEUkxdGeVPeAsNroFgUYE9HwcQLTMygFEAzBn', 
	 'http://merchant-simple-competition-logic1:5001', 
	 'Competition Logic 1', 
	 'Simple') 
ON CONFLICT DO NOTHING;
