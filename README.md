# python-requests-proxy-API
This project will collect the products in the shops around the user location having as target the Bershka website.

The following project is very similar to the previous one with River Island, but as they removed their APIs I had to find another shop. 

Berhska has not removed their apis and the link "find in store" is still there. 

The software shows which products are near the user location; in fact, the user is able to enter its current location (postcode or city) and its preferred shoe size.

After some testing, Bershka has decide to block my IP address. I have solved the problem by using a Proxy server (https://www.scraperapi.com/documentation).

Althoug, this process changes the IP address every requests, which reaaaaally slows down the whole software.
