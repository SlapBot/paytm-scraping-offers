SELECT products.name, products.link, products.price, offers.code, offers.description
FROM products
JOIN product_offer ON products.id = product_offer.product_id
JOIN offers ON offers.id = product_offer.offer_id WHERE offers.code = "{0}"
ORDER BY products.price DESC
