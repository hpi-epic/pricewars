INSERT INTO public.merchants (merchant_id, merchant_token, api_endpoint_url, merchant_name, algorithm_name) VALUES 
	('eLDGiF3tq73CUn4/bxu7R8yYS2mtG0b6oknnypO33Ag=', 
	 'oXbPx3EEZw4vpBb3QmITBIu86PA48oWwN8LKAZYjXcfNoHQF4ihF1cO62YAANg6k', 
	 'http://merchant-sample-random-third:5005', 
	 'Random Third', 
	 'C') 
ON CONFLICT DO NOTHING;
