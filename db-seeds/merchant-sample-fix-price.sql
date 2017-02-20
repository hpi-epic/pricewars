INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('uJCuCWUQb4JjREFmy5cBNV6mQ5mKrPY1XDT1LKAkGtY=', 
	 'Qi5FFXq4rEXT6xqOqCrET12VSS26DKmd2rsHPjMHxtl4rcRioJwIKyomRpsdAfHD', 
	 'http://merchant-sample-fix-price:5007', 
	 'Fix Price', 
	 'E') 
ON CONFLICT DO NOTHING;
