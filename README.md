# Best-route
Shortest possible time to deliver concurrent food orders.

### Approach:
  1. Sort the orders based on ready time
  2. Insert each order(restaurant and customer locations) into the delivery route such that the time taken to deliver all orders in the route is shortest.
  3. The optimal positions of the restaurant and customer of an order in the existing route is obtained by trying all possible position(bruteforce)
 
