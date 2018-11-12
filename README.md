# WikiSurf
Scrapper/ Crawler sampler. It surfs the Wikipedia jumping from article to article, sampling frequencies for a selected word, with a sampling pace of: GAP = Population_of_articles / sample_size + randomSmallIntegerCoefficient . Prints and saves the selected links and the frequencies of the word. It doesnt samples frequencies from random pagees on wikipedia, but it avoids "neighbourhoods" of wikipedia links so it has a more clear sample and cover a bigger range. It is as fast as it can be and it is already very slow. you can change the population = 5,749,362 and samplesize=16593 if you have the guts!


############################

Description of Implementation:

############################

There are 5,749,362 articles in the English Wikipedia as of the 10th of November 2018 (based on this site: http://wikicount.net/) so in that case a good sample size for our population would be:
1. 9588 for confidence level 95% and confidence interval 1 
2. 16593  for confidence level 99% and confidence interval 1 
Based on this calculator: https://www.surveysystem.com/sscalc.htm

(If we raise confidence interval the sample size is reduced but I don't exactly understand how is used and how much it should be. In the site above there is also a calculator for it but I don't know how to use it)

Of course I am not sure if the sample articles a crawler can fetch, would be good enough, because the crawler will crawl a network of connected articles, with relative meanings and terms so we maybe cover a partial view. 
(Like sampling only some countries for a hypothetical experiment on humans, instead of a scattered sampling with a variety of kind-of random/ scattered countries from all around the world)

In that case I propose to divide the population/sample_size so we have a good quantization of the whole range of the population.  (GAP= population/sample_size +/- aSmallRandomIntegerCoefficient )  Then if we count the frequency of the word "human" in the page A, we should then sample from one of the the A+GAP pages,so we cover decently, the whole network. The pages wich will be retrieved each time, should be the least listed or never listed before, so we secure that we are going ahaid to the network of pages and not making cycles to the same "neighbourhoods", like shown in the images below
