import razorpay
client = razorpay.Client(auth=("rzp_test_zom8T8cjwIhanK", "gjthfAGvWmgX96teePZvNi5X"))

data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
payment = client.order.create(data=data)