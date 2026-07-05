

class OCCService:
    def update_order_status(self, order_id, new_status, expected_version):
        with transaction.atomic():
            order = Order.objects.select_for_update().get(id=order_id)
            if order.version != expected_version:
                raise Exception("Order has been modified by another process. Please refresh and try again.")
            
            order.status = new_status
            order.version += 1
            order.save()
class PlaceOrderService:
    def placeOrder(self,user_id,order_details):
        shipping_address = order_details.get('shipping_address')

