There were some ambiguities/queries in scraping the data. 

For website "promega", should I extract video URL along with image URL for product like i.e. https://www.promega.com/products/instruments/maxwell-instruments/maxprep-maxwell-rsc-48-bundle/
Product items with multiple product options, Do I have to extract detail of all available product options or just the selected one? And in this case, we can't retrieve the size text as it is not present in our selected tag. i.e. https://www.promega.com/products/cell-health-assays/adme-assays/p450-glo-cyp2b6-assay-and-screening-systems-2/?catNum=V8321
For product items without prices, what should I do? Should I ignore the item or just ignore the price table? 
For now, I'm placing text 'Please Enquire' in the price column if price is not there.  
i.e. - https://www.promega.com/products/instruments/maxwell-instruments/maxprep-maxwell-rsc-48-bundle/ 
- https://www.promega.com/applications/applied-and-environmental-sciences/environmental-and-water-testing/water-glo-system-tools-for-using-atp-to-detect-microbes-in-water/

For website "rndsystems", I'm assuming that description's data in product table is product summary. I'm also assuming that in the given example, data is not updated or old because I couldn't find values for attribute's 'linearity' and 'recovery'.
In this site, there are many different paths/patterns for reaching an item. I have considered those paths which are common.

I'm scraping author names from 'p' tag with a specific class name but in some cases, author names are present in simple 'p' tag without any class attribute. So it is a known issue.  
Also, I couldn't find values for 'gtin', 'vendor_sku' and 'parent_sku' for both sites.
